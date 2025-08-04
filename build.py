# build.py
from pathlib import Path
import shutil

template = Path("template.html").read_text()
content_dir = Path("content")
output_dir = Path("build")

if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir()


def apply_template(content_html):
    return template.replace("{{ content }}", content_html)


for file in content_dir.glob("*.html"):
    content = file.read_text()
    output = apply_template(content)
    (output_dir / file.name).write_text(output)

print("Build complete.")
