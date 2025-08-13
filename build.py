from pathlib import Path
import shutil
import argparse
import subprocess

# === Get commit hash ===


def get_git_commit_hash():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    except subprocess.CalledProcessError:
        return "unknown"


# === Parse arguments ===
parser = argparse.ArgumentParser(description="Build the static site.")
parser.add_argument('--prod', action='store_true',
                    help='Output to build instead of .tempbuild')
args = parser.parse_args()

# === Output directory ===
output_dir = Path("build" if args.prod else ".tempbuild")

# === Config ===
template = Path("template.html").read_text()
content_dir = Path("content")

# === Clean output ===
if output_dir.exists():
    shutil.rmtree(output_dir)
output_dir.mkdir(parents=True)

# === Function to apply template ===


def apply_template(input_template, content_html, placeholder):
    return input_template.replace(placeholder, content_html)


# === Process .html content ===
for file in content_dir.glob("*.html"):
    content = file.read_text()
    output = apply_template(template, content, "<!-- Content goes here -->")
    output = apply_template(output, get_git_commit_hash(),
                            "<!-- Git Commit Hash -->")

    # Create directory for each HTML file, put output as index.html
    if file.stem == "index":
        # Root index.html
        (output_dir / "index.html").write_text(output)
    else:
        page_dir = output_dir / file.stem
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(output)


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

# === Copy start.sh ===
script_src = Path("start.sh")
if script_src.exists():
    shutil.copy2(script_src, output_dir / script_src.name)

print("Build complete.")
