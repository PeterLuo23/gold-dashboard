#!/usr/bin/env python3
"""
PeterLuo财经日报 · 自循环执行脚本
用法: python3 run_daily.py [--date YYYY-MM-DD]
流程: 拉取配置 → 获取数据 → 生成内容 → 更新历史 → 推送仓库
"""
import json, os, sys, subprocess, base64, urllib.request
from datetime import datetime, timedelta

# 配置
REPO = "PeterLuo23/gold-dashboard"
BRANCH = "main"
TOKEN = os.environ.get("GH_TOKEN", "")
API = "https://api.github.com"

def api_call(method, path, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode()), e.code

def fetch_file(path):
    """从仓库拉取文件内容"""
    data, status = api_call("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")
    if status == 200:
        return base64.b64decode(data["content"]).decode("utf-8")
    return None

def push_file(path, local_path, message):
    """推送文件到仓库"""
    # 获取现有sha
    sha = None
    try:
        data, _ = api_call("GET", f"/repos/{REPO}/contents/{path}?ref={BRANCH}")
        sha = data.get("sha")
    except:
        pass

    with open(local_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()

    body = {"message": message, "content": content_b64, "branch": BRANCH}
    if sha:
        body["sha"] = sha

    _, status = api_call("PUT", f"/repos/{REPO}/contents/{path}", body)
    return status in (200, 201)

def main():
    if not TOKEN:
        print("❌ GH_TOKEN 未设置")
        sys.exit(1)

    today = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--date" else datetime.now().strftime("%Y-%m-%d")
    print(f"📅 PeterLuo财经日报 · {today}")

    # 1. 拉取配置
    print("1️⃣ 拉取配置...")
    config_raw = fetch_file("finance-daily/config/settings.json")
    if config_raw:
        config = json.loads(config_raw)
        print(f"   ✅ 配置已恢复 (v{config['meta']['version']})")
    else:
        print("   ⚠️ 配置不存在，使用默认")
        config = None

    # 2. 拉取准确率历史
    print("2️⃣ 拉取历史...")
    acc_raw = fetch_file("finance-daily/history/accuracy.json")
    if acc_raw:
        acc = json.loads(acc_raw)
        print(f"   ✅ 准确率历史已恢复 ({len(acc['records'])} 条记录)")
    else:
        print("   ⚠️ 历史不存在，新建")
        acc = {"records": [], "stats": {}}

    # 3. 数据获取 (简化版，实际应调用 iFinD/东方财富)
    print("3️⃣ 获取数据...")
    print("   [此处插入数据获取逻辑]")

    # 4. 生成内容
    print("4️⃣ 生成内容...")
    print("   [此处插入页面生成逻辑]")

    # 5. 更新历史
    print("5️⃣ 更新历史...")
    # 验证前日预判
    if acc["records"] and not acc["records"][-1].get("verified"):
        print(f"   待验证: {acc['records'][-1]['date']}")

    # 6. 推送
    print("6️⃣ 推送到仓库...")
    # push_file("finance-daily/index.html", "...", f"[日报] {today} 收盘晚报")

    print("✅ 执行完成")

if __name__ == "__main__":
    main()
