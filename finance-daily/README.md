# PeterLuo财经日报

A股交易日收盘晚报自动生成系统。

## 目录结构

```
finance-daily/
├── config/
│   └── settings.json          # 配置中心（股池、数据源、语音偏好）
├── history/
│   ├── accuracy.json          # 早盘预判准确率历史
│   └── snapshots.json         # 快照索引（7天滚动）
├── index.html                 # 最新日报页面
├── briefing.mp3               # 最新语音播报
├── snapshots/                 # 历史快照
└── run_daily.py               # 自循环执行脚本
```

## 配置说明

编辑 `config/settings.json` 可自定义：
- **watchlist**: 关注个股和板块
- **data_sources**: 数据源优先级（iFinD → 东方财富 → 网络搜索）
- **voice**: 语音引擎偏好（Kimi TTS → edge-tts 降级）
- **rolling_retention**: 快照保留天数

## 执行方式

### 方式1: 手动触发（当前）
向 Kimi Agent 发送消息：
```
执行PeterLuo财经日报17:00收盘晚报更新
```
Agent 会自动：
1. 从本仓库拉取配置
2. 获取当日数据
3. 生成页面和音频
4. 更新准确率历史
5. 推送回仓库

### 方式2: 定时触发（未来）
设置外部定时服务调用 Kimi API，或手机闹钟提醒手动触发。

## 数据源

- **主要**: iFinD（同花顺）
- **备用**: 东方财富数据中心 API
- **辅助**: 财联社、证券时报、每日经济新闻

## 语音

- **首选**: Kimi TTS (voice_id=NLl76XZRVj1RVeXptX3h, 温暖女声)
- **降级**: edge-tts (zh-CN-XiaoxiaoNeural)
- **处理**: ffmpeg loudnorm (I=-11:TP=-1.0:LRA=6)

## 准确率追踪

历史记录保存在 `history/accuracy.json`，支持：
- 逐日预判验证
- 7日/30日滚动准确率统计
- 结构化数据便于回测

---
*自动生成于 2026-07-23*
