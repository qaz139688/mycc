# Changelog

## [0.1.0] - 2026-01-29

### Added
- 🖼️ 支持图片消息（发送图片给 Claude）
- 🪟 Windows 跨平台支持 + AI 安装指南
- 📖 AI 可读 FAQ 文档（`docs/FAQ.md`）

### Changed
- ⚡ 优化历史记录加载，压缩 50% 流量
- 🔧 移除 `~/.mycc/` fallback，配置只存项目目录

### Fixed
- 🐛 Windows 上 Claude CLI 路径检测问题
- 🐛 ESM 模式下的 require 调用问题

---

## [2026-01-28]

### Added
- `retryWithBackoff` 通用重试函数
- `waitForReady` 主动探测等待函数
- Worker `/info/{token}` 接口用于验证连接
- `config.ts` 统一配置管理
- `adapters` 适配器架构

### Changed
- tunnel 等待从固定 10 秒改为主动探测（最多 30 秒，快的时候 2-3 秒）
- 注册/验证失败后有明确提示

### Fixed
- 后端重启后前端无法自动重连的问题
- `onRetry` 回调重复调用的 bug

## [2026-01-27]

### Added
- 首次发布
- 基础后端架构
- 网页端配对功能
