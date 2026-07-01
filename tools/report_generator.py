#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

try:
    from jinja2 import Template
except Exception:
    print("Please install jinja2: pip install jinja2")
    raise

TEMPLATE_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 18px; color: #222 }
    header { border-bottom:1px solid #ddd; margin-bottom:12px }
    h1 { font-size: 1.6em }
    nav { margin-top:8px }
    nav a { margin-right: 8px }
    .section { margin-top: 18px; padding-top: 8px }
    .summary { display:flex; gap:12px; flex-wrap:wrap }
    .card { border:1px solid #eee; padding:10px; border-radius:6px; background:#fafafa; min-width:200px }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #e6e6e6; padding: 6px; text-align: left; vertical-align: top }
    pre { background:#f7f7f7; padding:8px; white-space:pre-wrap }
    .appendix { font-size:0.9em; color:#444 }
  </style>
  <meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body>
<header>
  <h1>{{ title }}</h1>
  <div>Generated: {{ generated }}</div>
  <nav>
  {% for fname in report.keys() %}
    <a href="#{{ loop.index0 }}">{{ fname }}</a>
  {% endfor %}
  </nav>
</header>

{% for fname,content in report.items() %}
  <section class="section" id="{{ loop.index0 }}">
    <h2>{{ fname }}</h2>
    {% if content is mapping %}
      <div class="summary">
        {% if content.ansible_facts is defined %}
          <div class="card"><strong>OS</strong><div>{{ content.ansible_facts.distribution }} {{ content.ansible_facts.distribution_major | default('') }}</div></div>
        {% endif %}
        {% if content.rpm_packages is defined %}
          <div class="card"><strong>RPM packages</strong><div>{{ (content.rpm_packages | length) }} installed</div></div>
        {% endif %}
        {% if content.running_services is defined %}
          <div class="card"><strong>Running services</strong><div>{{ (content.running_services | length) }}</div></div>
        {% endif %}
      </div>

      {% for k,v in content.items() %}
        <div style="margin-top:12px">
          <h3>{{ k.replace('_',' ').title() }}</h3>
          {% if v is string %}
            <pre>{{ v }}</pre>
          {% elif v is mapping %}
            <table>
              <thead><tr><th>Key</th><th>Value</th></tr></thead>
              <tbody>
              {% for kk,vv in v.items() %}
                <tr><td>{{ kk }}</td><td><pre>{{ vv }}</pre></td></tr>
              {% endfor %}
              </tbody>
            </table>
          {% elif v is iterable %}
            <table>
              <thead><tr><th>#</th><th>Item</th></tr></thead>
              <tbody>
              {% for it in v %}
                <tr><td>{{ loop.index }}</td><td><pre>{{ it }}</pre></td></tr>
              {% endfor %}
              </tbody>
            </table>
          {% else %}
            <pre>{{ v }}</pre>
          {% endif %}
        </div>
      {% endfor %}

    {% else %}
      <pre>{{ content }}</pre>
    {% endif %}
    <div class="appendix">
      {% if content.source_urls is defined %}
        <h4>Documentation</h4>
        <ul>
        {% for u in content.source_urls %}
          <li><a href="{{ u }}">{{ u }}</a></li>
        {% endfor %}
        </ul>
      {% endif %}
    </div>
  </section>
{% endfor %}

</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--inputs', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--title', default='Healthcheck Report')
    args = p.parse_args()

    input_path = Path(args.inputs)
    if not input_path.exists():
        print(f"Input {input_path} not found")
        return 2

    with input_path.open() as fh:
        data = json.load(fh)

    tpl = Template(TEMPLATE_HTML)
    out_html = tpl.render(title=args.title, report=data, generated=input_path.stat().st_mtime)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_html)
    print(f"Wrote {out_path}")

if __name__ == '__main__':
    main()
