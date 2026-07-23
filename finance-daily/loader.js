// PeterLuo财经日报 · 前端加载器
// 功能: 绕过 CDN 缓存加载最新日报
// 用法: 在你的日报应用 index.html 中引入此脚本

const CONFIG = {
    repo: 'PeterLuo23/gold-dashboard',
    branch: 'main',
    // 如需使用 GitHub API（更可靠），请填入你的只读 PAT:
    // token: 'github_pat_xxx',
    paths: {
        evening: 'finance-daily/index.html',
        audio: 'finance-daily/briefing.mp3'
    }
};

async function loadDailyReport() {
    // 方案1: jsDelivr CDN + 时间戳（无需 PAT，但可能有5分钟延迟）
    const cdnUrl = `https://cdn.jsdelivr.net/gh/${CONFIG.repo}@${CONFIG.branch}/${CONFIG.paths.evening}?t=${Date.now()}`;

    // 方案2: GitHub API（需要 PAT，实时无缓存）
    // 取消下面注释并填入 token:
    /*
    const apiUrl = `https://api.github.com/repos/${CONFIG.repo}/contents/${CONFIG.paths.evening}?ref=${CONFIG.branch}`;
    const resp = await fetch(apiUrl, {
        headers: {
            'Authorization': `Bearer ${CONFIG.token}`,
            'Accept': 'application/vnd.github+json'
        }
    });
    const data = await resp.json();
    const html = atob(data.content);
    document.open(); document.write(html); document.close();
    return;
    */

    // 默认使用 CDN 方案
    try {
        const resp = await fetch(cdnUrl, { cache: 'no-store' });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const html = await resp.text();
        document.open(); document.write(html); document.close();
        console.log('✅ 日报已加载 (CDN):', new Date().toLocaleString());
    } catch (e) {
        console.error('❌ CDN 加载失败:', e);
        // 降级: 直接跳转
        window.location.href = cdnUrl;
    }
}

// 自动加载
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadDailyReport);
} else {
    loadDailyReport();
}
