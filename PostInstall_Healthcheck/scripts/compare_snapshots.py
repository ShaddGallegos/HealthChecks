#!/usr/bin/env python3
"""Compare two healthcheck snapshot JSON files and produce a report.

Usage: compare_snapshots.py before.json after.json [--output report.json]
"""
import argparse
import json
import os
import glob
import difflib
from datetime import datetime


def pick_file(path_pattern):
    # If path contains glob, pick the newest match
    matches = glob.glob(path_pattern)
    if not matches:
        raise FileNotFoundError(path_pattern)
    if len(matches) == 1:
        return matches[0]
    # pick newest
    matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return matches[0]


def load(path):
    with open(path) as f:
        return json.load(f)


def to_set(obj):
    if obj is None:
        return set()
    if isinstance(obj, list):
        return set(obj)
    if isinstance(obj, str):
        return set([obj])
    return set(obj)


def diff_lists(before, after):
    b = to_set(before)
    a = to_set(after)
    return sorted(list(a - b)), sorted(list(b - a))


def unified(a, b, fromfile='before', tofile='after'):
    a_lines = (a or '').splitlines(keepends=True)
    b_lines = (b or '').splitlines(keepends=True)
    return ''.join(difflib.unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile))


def build_report(before, after):
    report = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'summary': {},
        'details': {}
    }

    keys = [
        'rpm_packages', 'enabled_services', 'running_services',
        'listening_tcp', 'listening_udp', 'users', 'groups'
    ]

    for k in keys:
        added, removed = diff_lists(before.get(k), after.get(k))
        report['summary'][k] = {'added': len(added), 'removed': len(removed)}
        report['details'][k] = {'added': added, 'removed': removed}

    # text diffs
    for k in ['sudoers', 'firewall', 'selinux']:
        before_text = before.get(k, '')
        after_text = after.get(k, '')
        if before_text != after_text:
            report['details'][k] = unified(before_text, after_text, fromfile='before_'+k, tofile='after_'+k)
            report['summary'][k] = {'changed': True}
        else:
            report['details'][k] = ''
            report['summary'][k] = {'changed': False}

    # hardware / text-like diffs
    text_keys = ['lsblk','dmidecode','lspci','lsusb','cpuinfo','memory','ip_brief','ip_link','nmcli','subscription','insights','rhc','updates','updateinfo','dmesg','journal_errors']
    for k in text_keys:
        before_text = before.get(k, '')
        after_text = after.get(k, '')
        if before_text != after_text:
            report['details'][k] = unified(before_text, after_text, fromfile='before_'+k, tofile='after_'+k)
            report['summary'][k] = {'changed': True}
        else:
            report['details'][k] = ''
            report['summary'][k] = {'changed': False}

    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument('before')
    p.add_argument('after')
    p.add_argument('--output', '-o', help='Write JSON report to this file')
    args = p.parse_args()

    before_path = pick_file(args.before)
    after_path = pick_file(args.after)

    before = load(before_path)
    after = load(after_path)

    report = build_report(before, after)

    # print concise summary
    print('Snapshot comparison')
    print('  before: ', before_path)
    print('  after:  ', after_path)
    print('Summary:')
    for k, v in report['summary'].items():
        print(f'  {k}: {v}')

    if args.output:
        os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print('Wrote report to', args.output)
    else:
        print('\nFull report JSON:\n')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
