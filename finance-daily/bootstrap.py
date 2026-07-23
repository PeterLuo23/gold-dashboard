#!/usr/bin/env python3
"""
PeterLuo财经日报 · 自恢复启动脚本
功能: 新会话启动时自动从GitHub仓库拉取配置和历史
用法: 导入 bootstrap 模块或执行 python3 bootstrap.py
"""
import json, os, urllib.request, base64

REPO = "PeterLuo23/gold-dashboard"
BRANCH = "main"
API = "https://api.github.com"

def fetch_repo_file(path, token=""):
    """从仓库拉取文件内容"""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(f"{API}/repos/{REPO}/contents/{path}?ref={BRANCH}", headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data.get("encoding") == "base64":
                return base64.b64decode(data["content"]).decode("utf-8"), data.get("sha")
            return data.get("content", ""), data.get("sha")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise

def bootstrap(token=""):
    """自恢复: 拉取配置和历史到本地"""
    print("🔧 PeterLuo财经日报 · 自恢复启动")
    print(f"   仓库: {REPO}/{BRANCH}")

    # 创建工作区
    workspace = "/mnt/agents/output/peterluo-daily"
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(f"{workspace}/config", exist_ok=True)
    os.makedirs(f"{workspace}/history", exist_ok=True)
    os.makedirs(f"{workspace}/snapshots", exist_ok=True)

    # 拉取配置
    config, _ = fetch_repo_file("finance-daily/config/settings.json", token)
    if config:
        with open(f"{workspace}/config/settings.json", "w", encoding="utf-8") as f:
            f.write(config)
        cfg = json.loads(config)
        print(f"   ✅ 配置已恢复 (v{cfg['meta']['version']})")
    else:
        print("   ⚠️ 配置不存在，将使用默认")

    # 拉取准确率历史
    acc, _ = fetch_repo_file("finance-daily/history/accuracy.json", token)
    if acc:
        with open(f"{workspace}/history/accuracy.json", "w", encoding="utf-8") as f:
            f.write(acc)
        records = json.loads(acc)
        print(f"   ✅ 准确率历史已恢复 ({len(records.get('records', []))} 条记录)")
    else:
        print("   ⚠️ 准确率历史不存在")

    # 拉取快照索引
    snaps, _ = fetch_repo_file("finance-daily/history/snapshots.json", token)
    if snaps:
        with open(f"{workspace}/history/snapshots.json", "w", encoding="utf-8") as f:
            f.write(snaps)
        print(f"   ✅ 快照索引已恢复")

    # 拉取最新日报页面（用于参考模板）
    html, _ = fetch_repo_file("finance-daily/index.html", token)
    if html:
        with open(f"{workspace}/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"   ✅ 最新日报页面已缓存")

    print(f"\n📁 工作区就绪: {workspace}")
    return workspace

if __name__ == "__main__":
    # 尝试从环境变量获取令牌
    token = os.environ.get("GH_TOKEN", "")
    bootstrap(token)
