"""把 figures/ 里的原图压缩成画廊用的 WebP（800 宽与原始宽度两种，不放大），输出到 assets/images/gallery/。

用法：python _tools/gallery_image.py <原图> <英文短名>
会打印图片尺寸，填进 _data/gallery.yml 的 width/height。依赖：Pillow
"""
import sys
from pathlib import Path

from PIL import Image

src, slug = sys.argv[1:]
out = Path("assets/images/gallery")
out.mkdir(parents=True, exist_ok=True)
im = Image.open(src).convert("RGB")
small = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
small.save(out / f"{slug}-800.webp", "WEBP", quality=80, method=6)
im.save(out / f"{slug}-full.webp", "WEBP", quality=80, method=6)
print(f"{slug}: width {im.width}, height {im.height}")
