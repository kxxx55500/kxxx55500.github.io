"""把霞鹜文楷切成按需加载的 WOFF2 小块，并生成 @font-face 样式表。

切片沿用 Google Fonts 中文字体的 unicode-range 分组（按字频排列，常用字集中在少数几块，
约 1.4 万字，含常用简繁体、标点与西文）。其余生僻字不收录，由系统楷体补位。

用法：
  python _tools/build_wenkai.py <slices.css> <out_dir> <Regular.ttf>:400 <Medium.ttf>:500
其中 slices.css 为 fonts.googleapis.com 返回的任一中文字体样式表（只取其中的 unicode-range）。
依赖：fonttools、brotli
"""
import os
import re
import sys
from multiprocessing import Pool

from fontTools import subset
from fontTools.ttLib import TTFont

FAMILY = "LXGW WenKai"


def parse_ranges(css):
    slices = []
    for block in re.findall(r"unicode-range:\s*([^;]+);", css):
        cps = set()
        for part in block.split(","):
            part = part.strip().upper().removeprefix("U+")
            if "-" in part:
                a, b = part.split("-")
                cps.update(range(int(a, 16), int(b, 16) + 1))
            else:
                cps.add(int(part, 16))
        slices.append(cps)
    return slices


def to_range(cps):
    cps = sorted(cps)
    out, start, prev = [], cps[0], cps[0]
    for c in cps[1:] + [None]:
        if c is not None and c == prev + 1:
            prev = c
            continue
        out.append(f"U+{start:x}" if start == prev else f"U+{start:x}-{prev:x}")
        if c is not None:
            start = prev = c
    return ", ".join(out)


def make_chunk(args):
    ttf, cps, path = args
    font = TTFont(ttf)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.hinting = False
    opts.desubroutinize = True
    opts.name_IDs = ["*"]
    s = subset.Subsetter(opts)
    s.populate(unicodes=cps)
    s.subset(font)
    font.save(path)
    return os.path.getsize(path)


def main():
    slices_css, out_dir, *fonts = sys.argv[1:]
    os.makedirs(out_dir, exist_ok=True)
    slices = parse_ranges(open(slices_css, encoding="utf-8").read())
    css, jobs = [], []
    for spec in fonts:
        ttf, weight = spec.rsplit(":", 1)
        cmap = set(TTFont(ttf)["cmap"].getBestCmap())
        groups, used = [], set()
        for sl in slices:
            g = (sl & cmap) - used
            if g:
                groups.append(g)
                used |= g
        for i, g in enumerate(groups):
            name = f"wenkai-{weight}-{i:03d}.woff2"
            jobs.append((ttf, sorted(g), os.path.join(out_dir, name)))
            css.append(
                "@font-face{"
                f'font-family:"{FAMILY}";font-style:normal;font-weight:{weight};font-display:swap;'
                f'src:url("{name}") format("woff2");unicode-range:{to_range(g)};'
                "}"
            )
    with Pool() as pool:
        sizes = pool.map(make_chunk, jobs)
    with open(os.path.join(out_dir, "wenkai.css"), "w", encoding="utf-8") as f:
        f.write("/* 霞鹜文楷 LXGW WenKai，SIL Open Font License 1.1（见同目录 OFL.txt） */\n")
        f.write("\n".join(css) + "\n")
    print(f"{len(jobs)} chunks, total {sum(sizes) / 1e6:.1f} MB, max {max(sizes) / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
