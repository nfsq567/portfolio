import urllib.request
import time
import os
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

# 作品图片列表
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

def download_and_compress(url, name):
    output_path = os.path.join(output_dir, f"{name}.jpg")
    # 跳过已下载的
    if os.path.exists(output_path):
        size = os.path.getsize(output_path) / 1024
        print(f"[{name}] Already exists: {size:.1f}KB")
        return (name, output_path, size, True)
    
    for attempt in range(3):  # 最多重试3次
        try:
            start = time.time()
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                original_size = len(data) / 1024
                
                # 压缩图片
                img = Image.open(io.BytesIO(data))
                max_width = 800
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                img.save(output_path, 'JPEG', quality=82, optimize=True)
                compressed_size = os.path.getsize(output_path) / 1024
                
                elapsed = time.time() - start
                print(f"[{name}] {original_size:.1f}KB -> {compressed_size:.1f}KB ({compressed_size/original_size*100:.0f}%) in {elapsed:.1f}s")
                return (name, output_path, compressed_size, True)
        except Exception as e:
            print(f"[{name}] Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(2)
    
    print(f"[{name}] FAILED after 3 attempts")
    return (name, None, 0, False)

print(f"Starting download with 4 threads...")
start_time = time.time()

results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(download_and_compress, url, name): name for url, name in images}
    for future in as_completed(futures):
        results.append(future.result())

success = [r for r in results if r[3]]
failed = [r for r in results if not r[3]]

print(f"\n{'='*50}")
print(f"Done: {len(success)}/{len(images)} images compressed in {time.time()-start_time:.1f}s")
if failed:
    print(f"Failed: {[r[0] for r in failed]}")
print(f"{'='*50}")

# 输出成功的文件路径，供后续上传使用
print("\nCompressed files:")
for name, path, size, ok in success:
    print(f"  {name}: {path} ({size:.1f}KB)")
