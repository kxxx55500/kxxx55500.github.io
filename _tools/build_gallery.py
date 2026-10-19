"""生成画廊图片：读取 _data/gallery.yml（后台「画廊」栏目编辑的列表），
把每张原图压缩成 800 宽与原始宽度两种 WebP，并写出 _data/gallery_built.json 供页面使用。

在 Jekyll 构建之前运行（线上由 GitHub Actions 执行）。生成物不提交到仓库。
文件名取原图内容的哈希，原图不变就不会重复生成。

用法：python _tools/build_gallery.py
依赖：Pillow、PyYAML
"""
import hashlib
import json
from pathlib import Path

import yaml
from PIL import Image

OUT = Path("assets/images/gallery")


def main():
    items = yaml.safe_load(Path("_data/gallery.yml").read_text(encoding="utf-8")) or []
    OUT.mkdir(parents=True, exist_ok=True)
    built = []
    for item in items:
        src = Path(str(item.get("image") or "").lstrip("/"))
        if not src.is_file():
            print(f"跳过「{item.get('title')}」：找不到图片 {src}")
            continue
        key = hashlib.sha1(src.read_bytes()).hexdigest()[:12]
        small, full = OUT / f"{key}-800.webp", OUT / f"{key}-full.webp"
        im = Image.open(src).convert("RGB")
        if not full.exists():
            im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(small, "WEBP", quality=80, method=6)
            im.save(full, "WEBP", quality=80, method=6)
        built.append({
            "title": item.get("title", ""),
            "alt": item.get("alt") or item.get("title", ""),
            "small": "/" + small.as_posix(),
            "full": "/" + full.as_posix(),
            "width": im.width,
            "height": im.height,
        })
    Path("_data/gallery_built.json").write_text(json.dumps(built, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"画廊：{len(built)} 张")


if __name__ == "__main__":
    main()
