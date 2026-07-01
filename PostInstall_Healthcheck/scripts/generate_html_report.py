#!/usr/bin/env python3
"""Generate a simple HTML report from the JSON report produced by compare_snapshots.py

Usage: generate_html_report.py report.json output.html
"""
import json
import sys
import os
from html import escape


def render_list(title, items):
    if not items:
        return f"<h4>{escape(title)}</h4><p>None</p>\n"
    s = f"<h4>{escape(title)}</h4>\n<ul>\n"
    for it in items:
        s += f"  <li>{escape(str(it))}</li>\n"
    s += "</ul>\n"
    return s


def render_summary(report):
    s = '<table class="summary">\n<tr><th>Item</th><th>Added</th><th>Removed</th><th>Changed</th></tr>\n'
    for k, v in report.get('summary', {}).items():
        added = v.get('added', 0) if isinstance(v, dict) else 0
        removed = v.get('removed', 0) if isinstance(v, dict) else 0
        changed = v.get('changed', False) if isinstance(v, dict) else False
        total = (added or 0) + (removed or 0)
        # determine status class
        if total > 20:
            cls = 'critical'
        elif total > 0 or changed:
            cls = 'warning'
        else:
            cls = 'ok'
        s += f"<tr class=\"{cls}\"><td>{escape(k)}</td><td>{escape(str(added))}</td><td>{escape(str(removed))}</td><td>{escape(str(changed))}</td></tr>\n"
    s += '</table>\n'
    return s


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_html_report.py report.json output.html")
        sys.exit(2)
    report_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(report_path) as f:
        report = json.load(f)

    html = [
        '<!doctype html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="utf-8"/>',
        '<meta name="viewport" content="width=device-width,initial-scale=1"/>',
        '<title>PostInstall Healthcheck Report</title>',
        '<style>',
        'body{font-family: Arial, Helvetica, sans-serif; padding:20px}',
        '.summary{border-collapse:collapse;margin-bottom:1rem}',
        '.summary th,.summary td{border:1px solid #ddd;padding:8px}',
        '.ok{background:#e6ffed}',
        '.warning{background:#fff3cd}',
        '.critical{background:#f8d7da}',
        'h1,h2,h3,h4{margin:0.5rem 0}',
        'pre{background:#f8f8f8;padding:8px;overflow:auto}',
        '</style>',
        '</head>',
        '<body>',
        f"<h1>PostInstall Healthcheck Report</h1>",
        f"<p>Generated at: {escape(report.get('generated_at',''))}</p>",
        '<h2>Summary</h2>',
        render_summary(report),
        '<h2>Details</h2>'
    ]

    details = report.get('details', {})
    # embed chart if present
    chart_path = os.path.join(os.path.dirname(out_path), 'chart.png')
    if os.path.exists(chart_path):
        html.append('<h2>Visual Summary</h2>')
        html.append(f'<img src="chart.png" alt="summary chart" style="max-width:100%;height:auto"/>')
        html.append('<hr/>')
    for k, v in details.items():
        html.append(f"<h3>{escape(k)}</h3>")
        if isinstance(v, dict):
            html.append(render_list('Added', v.get('added', [])))
            html.append(render_list('Removed', v.get('removed', [])))
        else:
            # assume text diff
            html.append('<h4>Diff</h4>')
            html.append('<pre>')
            html.append(escape(v or ''))
            html.append('</pre>')

    html.append('</body>')
    html.append('</html>')

    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    with open(out_path, 'w') as f:
        f.write('\n'.join(html))

    print('Wrote HTML report to', out_path)


if __name__ == '__main__':
    main()
