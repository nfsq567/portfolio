import urllib.request
import time
import os
from PIL import Image
import io

# 作品图片列表（从 HTML 中提取的19张）
images = [
    ("https://aka.doubaocdn.com/s/wGkNrzDBjR", "ui1"),
    ("https://aka.doubaocdn.com/s/Ywf3sEvrvZ", "ui2"),
    ("https://aka.doubaocdn.com/s/Vrnka13eK2", "ui3"),
    ("https://aka.doubaocdn.com/s/fS7G8Y1V8T", "ui4"),
    ("https://aka.doubaocdn.com/s/9NVuk3FLdz", "poster1"),
    ("https://aka.doubaocdn.com/s/HD0mZJhxsi", "poster2"),
    ("https://aka.doubaocdn.com/s/FHpnFsyDSS", "poster3"),
    ("https://aka.doubaocdn.com/s/HJPUEkxBnY", "poster4"),
    ("https://aka.doubaocdn.com/s/UFJfUagaLE", "pack1"),
    ("https://aka.doubaocdn.com/s/YMohLSeU5l", "pack2"),
    ("https://aka.doubaocdn.com/s/ohqADAyFrg", "pack3"),
    ("https://aka.doubaocdn.com/s/k3xzCTa82F", "pack4"),
    ("https://aka.doubaocdn.com/s/RmTNyz3aV4", "brand1"),
    ("https://aka.doubaocdn.com/s/q9tU68uY2k", "brand2"),
    ("https://aka.doubaocdn.com/s/LyNVVKYCkf", "brand3"),
    ("https://aka.doubaocdn.com/s/0kuD6VMkcv", "illu1"),
    ("https://aka.doubaocdn.com/s/V4OFwYVVPr", "illu2"),
    ("https://aka.doubaocdn.com/s/sVSX7cPRBO", "illu3"),
    ("https://aka.doubaocdn.com/s/tNLSvGjFPC", "illu4"),
]

output_dir = r"C:\Users\Lenovo\Doubao\chats\2026-09-13\new-chat-1\portfolio\compressed_images"
os.makedirs(output_dir, exist_ok=True)

results = []
for url, name in images:
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            original_size = len(data) / 1024
            
            # 压缩图片
            img = Image.open(io.BytesIO(data))
            # 最大宽度 800px
            max_width = 800
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
            
            # 保存为 JPEG（如果有透明通道，先转 RGB）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            output_path = os.path.join(output_dir, f"{name}.jpg")
            img.save(output_path, 'JPEG', quality=82, optimize=True)
            compressed_size = os.path.getsize(output_path) / 1024
            
            elapsed = time.time() - start
            print(f"[{name}] {original_size:.1f}KB -> {compressed_size:.1f}KB ({compressed_size/original_size*100:.0f}%) in {elapsed:.1f}s")
            results.append((name, output_path, compressed_size))
    except Exception as e:
        print(f"[{name}] Error: {e}")

print(f"\nDone: {len(results)}/{len(images)} images compressed")
