# -*- coding: utf-8 -*-
"""
作品集一键部署脚本
使用方法：
1. 第一次使用：在下面配置你的 GitHub Token
2. 以后每次改完 index.html，双击运行这个脚本即可自动部署
"""

import urllib.request
import urllib.error
import json
import base64
import os
import sys

# ============== 配置区域 ==============
# 你的 GitHub 用户名
GITHUB_USERNAME = "nfsq567"
# 仓库名
REPO_NAME = "portfolio"
# 分支名
BRANCH = "main"
# 要上传的文件路径（相对于仓库根目录）
FILE_PATH = "index.html"
# 本地 index.html 的完整路径
LOCAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
# GitHub Personal Access Token（第一次使用时填在这里）
# 获取地址：https://github.com/settings/tokens/new  勾选 repo 权限
GITHUB_TOKEN = ""
# ======================================


def get_file_sha():
    """获取远程文件当前的 SHA（更新文件时需要）"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}?ref={BRANCH}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("sha")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # 文件不存在，是新建
        raise


def upload_file():
    """上传文件到 GitHub"""
    # 读取本地文件
    with open(LOCAL_FILE, "rb") as f:
        content = f.read()
    content_b64 = base64.b64encode(content).decode("utf-8")

    # 获取当前 SHA
    sha = get_file_sha()

    # 构造请求
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"
    payload = {
        "message": f"Update portfolio - {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": content_b64,
        "branch": BRANCH,
    }
    if sha:
        payload["sha"] = sha

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT")
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        return result


def main():
    print("=" * 50)
    print("  作品集一键部署工具")
    print("=" * 50)

    # 检查 Token
    if not GITHUB_TOKEN:
        print("\n[错误] 尚未配置 GitHub Token！")
        print("\n请按以下步骤操作：")
        print("1. 打开 https://github.com/settings/tokens/new")
        print("2. Note 填: portfolio-deploy")
        print("3. Expiration 选: No expiration")
        print("4. 勾选: repo (第一个大选项)")
        print("5. 点 Generate token 生成")
        print("6. 复制生成的 token (ghp_ 开头)")
        print("7. 用记事本打开本脚本，把 token 粘贴到 GITHUB_TOKEN = \"\" 里")
        print("\n配置好后重新运行本脚本即可自动部署。")
        input("\n按回车键退出...")
        return

    # 检查本地文件
    if not os.path.exists(LOCAL_FILE):
        print(f"[错误] 找不到本地文件: {LOCAL_FILE}")
        input("按回车键退出...")
        return

    file_size = os.path.getsize(LOCAL_FILE)
    print(f"\n本地文件: {LOCAL_FILE}")
    print(f"文件大小: {file_size / 1024:.1f} KB")
    print(f"目标仓库: {GITHUB_USERNAME}/{REPO_NAME} ({BRANCH} 分支)")
    print(f"目标文件: {FILE_PATH}")

    print("\n正在上传...")
    try:
        result = upload_file()
        print("\n[成功] 文件已上传到 GitHub！")
        print(f"提交信息: {result['commit']['message']}")
        print(f"\nGitHub Pages 将在 1-2 分钟内自动部署完成。")
        print(f"部署后访问: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
        print(f"\n提示：部署后按 Ctrl+F5 强制刷新浏览器清除缓存。")
    except urllib.error.HTTPError as e:
        print(f"\n[失败] HTTP 错误 {e.code}")
        try:
            err = json.loads(e.read().decode("utf-8"))
            print(f"错误信息: {err.get('message', '未知错误')}")
        except:
            pass
        if e.code == 401:
            print("\n可能原因：Token 无效或没有 repo 权限")
        elif e.code == 403:
            print("\n可能原因：Token 权限不足或触发了 API 限流")
    except Exception as e:
        print(f"\n[失败] {e}")

    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
