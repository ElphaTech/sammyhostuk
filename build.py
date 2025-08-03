from pathlib import Path

template = Path('template.html').read_text()

# Simple placeholder replacement


def apply_template(content_html):
    return template.replace('<!-- Content goes here -->', content_html)


content_dir = Path('content')
output_dir = Path('.')

for content_file in content_dir.glob('*.html'):
    content_html = content_file.read_text()
    final_html = apply_template(content_html)

    output_file = output_dir / content_file.name
    output_file.write_text(final_html)

    print(f'Built {output_file}')
