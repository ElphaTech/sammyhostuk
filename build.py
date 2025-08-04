from pathlib import Path
import shutil

# === Config ===
template = Path("template.html").read_text()
content_dir = Path("content")
output_dir = Path("build")

# === Clean output ===
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True)

# === Function to apply template ===


def apply_template(content_html):
    return template.replace("{{ content }}", content_html)


# === Process .html content ===
for file in content_dir.glob("*.html"):
    content = file.read_text()
    output = apply_template(content)
    (output_dir / file.name).write_text(output)

# === Copy .css files to output ===
for css_file in Path(".").glob("*.css"):
    shutil.copy2(css_file, output_dir / css_file.name)

# === Copy media/ folder ===
media_src = Path("media")
media_dest = output_dir / "media"
if media_src.exists():
    shutil.copytree(media_src, media_dest)

# === Copy pull-latest.sh ===
script_src = Path("pull-latest.sh")
if script_src.exists():
    shutil.copy2(script_src, output_dir / script_src.name)

print("Build complete.")
