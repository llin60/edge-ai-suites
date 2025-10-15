import pathlib
import tempfile
import webbrowser
import markdown

def render_markdown_with_template(md_path, template_path, page_title=None, out_path=None, open_browser=True):
    """
    Convert a markdown file to HTML inside a template and optionally open it.

    Placeholders in template:
      {{PAGE_TITLE}}         -> replaced with page_title (or markdown stem)
      {{MARKDOWN_CONTENT}}   -> replaced with converted markdown HTML

    Args:
        md_path: Path to markdown file.
        template_path: Path to HTML template containing placeholders.
        page_title: Optional title override.
        out_path: Optional output HTML path. If None, a temp file is used.
        open_browser: If True, open result in default browser.

    Returns:
        Path to generated HTML file.
    """
    md_p = pathlib.Path(md_path).expanduser().resolve()
    tpl_p = pathlib.Path(template_path).expanduser().resolve()
    if not md_p.is_file():
        raise FileNotFoundError(f"Markdown not found: {md_p}")
    if not tpl_p.is_file():
        raise FileNotFoundError(f"Template not found: {tpl_p}")

    md_text = md_p.read_text(encoding="utf-8")
    html_md = markdown.markdown(md_text, extensions=["fenced_code", "tables"])

    tpl = tpl_p.read_text(encoding="utf-8")
    title = page_title or md_p.stem
    html = (tpl
            .replace("{{PAGE_TITLE}}", title)
            .replace("{{MARKDOWN_CONTENT}}", html_md))

    if out_path:
        out_file = pathlib.Path(out_path).expanduser().resolve()
        out_file.write_text(html, encoding="utf-8")
    else:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        tmp.write(html.encode("utf-8"))
        tmp.flush()
        tmp.close()
        out_file = pathlib.Path(tmp.name)

    if open_browser:
        webbrowser.open(f"file://{out_file}")

    return str(out_file)