#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys
import subprocess

try:
    from jinja2 import Template
except Exception:
    print("Please install jinja2: pip install jinja2")
    raise

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
  <style>body{font-family: Arial;} h1{border-bottom:1px solid #ccc;} pre{background:#f7f7f7;padding:8px}</style>
</head>
<body>
<h1>{{ title }}</h1>
<p>Generated from artifacts in {{ artifacts_dir }}</p>
{% for fname,content in data.items() %}
  <h2>{{ fname }}</h2>
  <pre>{{ content | tojson(indent=2) }}</pre>
{% endfor %}
</body>
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--artifacts', default=str(Path.home() / '.ansible' / 'artifacts'))
    p.add_argument('--output-dir', default=str(Path.home() / '.ansible' / 'reports'))
    p.add_argument('--title', default='Combined HealthChecks Report')
    p.add_argument('--formats', default='html')  # comma-separated: html,pdf,csv,xlsx,docx
    args = p.parse_args()

    artifacts = Path(args.artifacts)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    files = list(artifacts.glob('**/*.json'))
    combined = {}
    for f in files:
        try:
            combined[f.name] = json.loads(f.read_text())
        except Exception:
            combined[f.name] = f.read_text()

    combined_path = outdir / 'combined_reports.json'
    combined_path.write_text(json.dumps(combined, indent=2))
    print(f"Wrote combined json: {combined_path}")

    formats = [x.strip() for x in args.formats.split(',') if x.strip()]

    if 'html' in formats:
        tpl = Template(HTML_TEMPLATE)
        out_html = tpl.render(title=args.title, artifacts_dir=str(artifacts), data=combined)
        html_path = outdir / 'combined_reports.html'
        html_path.write_text(out_html)
        print(f"Wrote HTML report: {html_path}")

        if 'pdf' in formats:
            # try wkhtmltopdf
            try:
                subprocess.run(['wkhtmltopdf', str(html_path), str(outdir / 'combined_reports.pdf')], check=True)
                print('Wrote PDF via wkhtmltopdf')
            except Exception:
                print('wkhtmltopdf not available or failed to create PDF')

    if 'csv' in formats:
        import csv
        csv_path = outdir / 'combined_reports.csv'
        with csv_path.open('w', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow(['file','json'])
            for k,v in combined.items():
                writer.writerow([k, json.dumps(v)])
        print(f"Wrote CSV: {csv_path}")

    if 'xlsx' in formats:
        try:
            import pandas as pd
            xlsx_path = outdir / 'combined_reports.xlsx'
            # create a simple sheet with filename + json string
            rows = [{'file':k, 'json': json.dumps(v)} for k,v in combined.items()]
            df = pd.DataFrame(rows)
            df.to_excel(xlsx_path, index=False)
            print(f"Wrote XLSX: {xlsx_path}")
        except Exception:
            print('pandas not available; skipping xlsx')

    if 'docx' in formats:
        try:
            import pypandoc
            docx_path = outdir / 'combined_reports.docx'
            pypandoc.convert_file(str(html_path), 'docx', outputfile=str(docx_path))
            print(f"Wrote DOCX: {docx_path}")
        except Exception:
            print('pypandoc or pandoc not available; skipping docx')

    return 0

if __name__ == '__main__':
    sys.exit(main())
