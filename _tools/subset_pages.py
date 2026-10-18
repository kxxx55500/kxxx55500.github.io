"""按页面裁剪霞鹜文楷：每个页面只打包它实际用到的字。

在 Jekyll 构建之后运行：扫描 <site_dir> 中引用了 wenkai.css 的每个 HTML，
把正文用字裁成常规体（400）、标题等加粗处用字裁成中粗体（500），
写入 assets/fonts/p/，再把 wenkai.css 的引用替换为内联 @font-face。
用字完全相同的页面共用同一个字体文件。

用法：python _tools/subset_pages.py <site_dir> <Regular.ttf> <Medium.ttf>
依赖：fonttools、brotli
"""
import hashlib
import html
import os
import re
import sys
from multiprocessing import Pool
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

LINK = '<link rel="stylesheet" href="/assets/fonts/wenkai.css">'
FAMILY = "LXGW WenKai"
CSS_EXTRA = "＊　"  # 样式里用 content 生成的字（场景分隔线）
BOLD_TAGS = r"<(h1|h2|h3|strong)\b[^>]*>(.*?)</\1>|<a class=\"site-title\"[^>]*>(.*?)</a>"


def visible_text(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", "", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def chars(text):
    return frozenset(c for c in text if not c.isspace())


def make_font(args):
    ttf, cps, path = args
    if os.path.exists(path):
        return
    font = TTFont(ttf)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.hinting = False
    opts.desubroutinize = True
    s = subset.Subsetter(opts)
    s.populate(unicodes=sorted(ord(c) for c in cps))
    s.subset(font)
    font.save(path)


def main():
    site, regular, medium = sys.argv[1:]
    out = Path(site, "assets", "fonts", "p")
    out.mkdir(parents=True, exist_ok=True)
    pages, jobs = [], {}
    for page in Path(site).rglob("*.html"):
        doc = page.read_text(encoding="utf-8")
        if LINK not in doc:
            continue
        body = doc.split("<body", 1)[1]
        normal = chars(visible_text(body) + CSS_EXTRA)
        bold = chars("".join(visible_text(m.group(0)) for m in re.finditer(BOLD_TAGS, body, flags=re.S)))
        faces = []
        for weight, ttf, cps in (("400", regular, normal), ("500", medium, bold)):
            if not cps:
                continue
            name = hashlib.sha1((weight + "".join(sorted(cps))).encode()).hexdigest()[:16] + ".woff2"
            jobs[name] = (ttf, cps, str(out / name))
            faces.append(
                f'@font-face{{font-family:"{FAMILY}";font-weight:{weight};font-display:swap;'
                f'src:url("/assets/fonts/p/{name}") format("woff2")}}'
            )
        pages.append((page, doc.replace(LINK, "<style>" + "".join(faces) + "</style>")))
    with Pool() as pool:
        pool.map(make_font, jobs.values())
    for page, doc in pages:
        page.write_text(doc, encoding="utf-8")
    total = sum(f.stat().st_size for f in out.iterdir())
    print(f"{len(pages)} pages, {len(jobs)} font files, {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
