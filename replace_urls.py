# 批量替换 HTML 中的作品图片 URL
html_path = r"C:\Users\Lenovo\Doubao\chats\2026-09-13\new-chat-1\portfolio\index.html"

# 旧 URL → 新 URL 映射
url_map = {
    "https://aka.doubaocdn.com/s/wGkNrzDBjR": "https://aka.doubaocdn.com/s/8gDiRUkIBb",
    "https://aka.doubaocdn.com/s/Ywf3sEvrvZ": "https://aka.doubaocdn.com/s/vkleL8OXYo",
    "https://aka.doubaocdn.com/s/Vrnka13eK2": "https://aka.doubaocdn.com/s/ylz3IWlWmS",
    "https://aka.doubaocdn.com/s/fS7G8Y1V8T": "https://aka.doubaocdn.com/s/c2m3IznPZA",
    "https://aka.doubaocdn.com/s/9NVuk3FLdz": "https://aka.doubaocdn.com/s/bWddalvS2O",
    "https://aka.doubaocdn.com/s/HD0mZJhxsi": "https://aka.doubaocdn.com/s/OVVZc9IYul",
    "https://aka.doubaocdn.com/s/FHpnFsyDSS": "https://aka.doubaocdn.com/s/mH76WIPxdD",
    "https://aka.doubaocdn.com/s/HJPUEkxBnY": "https://aka.doubaocdn.com/s/fmj78i6pmY",
    "https://aka.doubaocdn.com/s/UFJfUagaLE": "https://aka.doubaocdn.com/s/8xVH7gFxXj",
    "https://aka.doubaocdn.com/s/YMohLSeU5l": "https://aka.doubaocdn.com/s/VTU9ZkNu1V",
    "https://aka.doubaocdn.com/s/ohqADAyFrg": "https://aka.doubaocdn.com/s/IR3bo93luD",
    "https://aka.doubaocdn.com/s/k3xzCTa82F": "https://aka.doubaocdn.com/s/l5dU2tINzK",
    "https://aka.doubaocdn.com/s/RmTNyz3aV4": "https://aka.doubaocdn.com/s/Fuv76y90B3",
    "https://aka.doubaocdn.com/s/q9tU68uY2k": "https://aka.doubaocdn.com/s/x60PigYDEI",
    "https://aka.doubaocdn.com/s/LyNVVKYCkf": "https://aka.doubaocdn.com/s/WUJDeqGV4F",
    "https://aka.doubaocdn.com/s/0kuD6VMkcv": "https://aka.doubaocdn.com/s/lcA5Uys8gT",
    "https://aka.doubaocdn.com/s/V4OFwYVVPr": "https://aka.doubaocdn.com/s/VUJaPuR2oA",
    "https://aka.doubaocdn.com/s/sVSX7cPRBO": "https://aka.doubaocdn.com/s/Dybf47wN4Y",
    "https://aka.doubaocdn.com/s/tNLSvGjFPC": "https://aka.doubaocdn.com/s/p7x8gR1kp0",
}

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

count = 0
for old_url, new_url in url_map.items():
    if old_url in content:
        content = content.replace(old_url, new_url)
        count += 1
        print(f"Replaced: {old_url.split('/')[-1]} -> {new_url.split('/')[-1]}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone: {count}/{len(url_map)} URLs replaced")
