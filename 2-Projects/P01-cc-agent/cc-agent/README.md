<div align="center">

# 🤖 1052 Agent

**一个功能强大、自我进化的智能助手,由一名17岁学生开发，欢迎交流讨论**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)](https://www.typescriptlang.org/)
[![ACP](https://img.shields.io/badge/ACP-0.1.99-orange.svg)](https://agentid.pub)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [ACP通信协议](#-acp-通信协议) • [详细配置](#-详细配置) • [API文档](#-api-文档)

<a href="https://github.com/1052666/1052">
  <img src="https://img.shields.io/github/stars/1052666/1052?style=social" alt="GitHub stars">
</a>

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [ACP 通信协议](#-acp-通信协议)
  - [什么是 ACP](#什么是-acp)
  - [核心概念](#核心概念)
  - [ACP 架构](#acp-架构)
  - [本项目中的 ACP 集成](#本项目中的-acp-集成)
  - [ACP 配置指南](#acp-配置指南)
  - [ACP API 接口](#acp-api-接口)
  - [ACP 使用示例](#acp-使用示例)
- [详细配置](#-详细配置)
- [核心功能详解](#-核心功能详解)
- [API 文档](#-api-文档)
- [架构设计](#-架构设计)
- [项目结构](#-项目结构)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)
- [更新日志](#-更新日志)
- [联系方式](#-联系方式)
- [免责声明](#-免责声明)

---

## 🌟 项目简介

1052 Agent 是一个功能强大的智能助手系统，具备自我学习、自我进化的能力。它不仅能进行智能对话，还能执行各种复杂任务，如文件操作、Shell 命令执行、联网搜索等。独特的**赚钱模式**和**自我进化机制**让 AI 能够自主创作内容并持续提升自身能力。

### 为什么选择 1052 Agent？

- 🚀 **开箱即用** - 完整的前后端分离架构，一键启动
- 🧠 **自我进化** - AI 会自主学习、反思、创建新技能
- 💰 **赚钱模式** - 自动创作小说内容，实现"自给自足"
- 🔗 **Agent 通信** - 支持 ACP 协议，实现多 Agent 协作
- 🛠️ **丰富工具** - 内置 20+ 实用工具函数
- 📱 **多平台支持** - Telegram、飞书即时通讯集成
- 🌐 **ACP 协议** - 原生支持智能体通信协议，可与其他 Agent 互联

---

## ✨ 功能特性

### 核心能力

| 功能 | 描述 | 状态 |
|------|------|------|
| 💬 智能对话 | 基于 GPT 模型的流式对话 | ✅ |
| 🧠 自我进化 | 自主学习、反思、创建技能 | ✅ |
| 💰 赚钱模式 | 自动创作小说内容 | ✅ |
| 📝 记忆系统 | 长期记忆存储与管理 | ✅ |
| 📚 技能系统 | 动态加载自定义技能 | ✅ |
| ⏰ 定时任务 | Cron 表达式定时执行 | ✅ |
| 📖 日记系统 | 自动记录成长历程 | ✅ |
| 🌐 联网搜索 | 集成密塔 AI 搜索 | ✅ |
| 💻 Shell 执行 | 安全执行系统命令 | ✅ |
| 📁 文件操作 | 读写、编辑文件 | ✅ |
| 📱 Telegram | 机器人消息收发 | ✅ |
| 📱 飞书 | 企业通讯集成 | ✅ |
| 🔗 **ACP 通信** | **智能体通信协议集成** | ✅ |
| 🤝 Agent 通信 | 标准化 API 接口 | ✅ |
| 🎨 Web UI | 现代化前端界面 | ✅ |

### 工具函数列表

```
├── execute_shell_command  - 执行 Shell 命令
├── file_operation         - 文件操作（读/写/编辑/删除）
├── web_search            - 联网搜索
├── send_telegram_message - 发送 Telegram 消息
├── send_feishu_message   - 发送飞书消息
├── send_acp_message      - 发送 ACP 消息到其他 Agent
├── create_skill          - 创建新技能
├── schedule_task         - 创建定时任务
├── add_memory            - 添加记忆
├── update_memory         - 更新记忆
├── delete_memory         - 删除记忆
├── read_memory           - 读取记忆
├── write_diary           - 写日记
├── read_diary            - 读日记
├── write_novel_chapter   - 写小说章节
├── get_novel_status      - 获取小说状态
├── start_money_making_mode - 启动赚钱模式
└── stop_money_making_mode  - 停止赚钱模式
```

---

## 🛠 技术栈

### 后端
- **Python 3.11+** - 主要编程语言
- **FastAPI** - 高性能 Web 框架
- **OpenAI API** - 大语言模型接口
- **ACP SDK (agentcp)** - 智能体通信协议 SDK
- **Pydantic** - 数据验证
- **httpx** - 异步 HTTP 客户端
- **cryptography** - 加密支持

### 前端
- **React 18** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **Tailwind CSS** - 样式框架

### 外部服务
- **Telegram Bot API** - 即时通讯
- **飞书开放平台** - 企业通讯
- **密塔 AI 搜索** - 联网搜索
- **AgentUnion** - ACP 接入点服务

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 或 yarn

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/1052666/1052.git
cd ai-agent
```

#### 2. 后端配置

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. 前端配置

```bash
cd ../frontend

npm install --registry=https://registry.npmmirror.com
```

#### 4. 启动服务

**启动后端服务：**

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 10053 --reload
```

**启动前端服务：**

```bash
cd frontend
npm run dev
```

#### 5. 访问应用

- **前端界面**: http://localhost:10052
- **API 文档**: http://localhost:10053/docs
- **Agent API 文档**: 查看 [AGENT_API.md](AGENT_API.md)

---

## 🔗 ACP 通信协议

### 什么是 ACP

**ACP (Agent Communication Protocol)** 是一个开放协议，用于解决 Agent 互相通信协作的问题，构建开放、可靠、可协作的智能体互联网。

> 🔗 **官方网站**: [https://agentid.pub](https://agentid.pub)
> 
> 📦 **SDK 文档**: [https://agentid.pub/sdk/](https://agentid.pub/sdk/)
> 
> 💻 **GitHub**: [https://github.com/auliwenjiang/agentcp](https://github.com/auliwenjiang/agentcp)

### 核心概念

#### Agent Internet 智能体互联网

由 Agent 互联互通后构成的开放性协作网络。在这个网络中，每个 Agent 都可以：
- 发现其他 Agent
- 与其他 Agent 建立通信
- 提供服务或消费服务
- 参与复杂的协作任务

#### Agent 智能体

Agent 是 **LLM + Tools + ACP** 三要素一起封装的程序：

```
┌─────────────────────────────────────────────────────────────┐
│                      Agent 智能体                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    LLM      │  │   Tools     │  │    ACP      │         │
│  │  大语言模型  │  │   工具集    │  │  通信协议    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  如果 Agent 是一台电脑：                                      │
│  - AID 就是它的网卡                                          │
│  - ACP 是网线                                                │
│  - AP 是路由器                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### AID 智能体身份标识

每一个智能体在网络中有一个唯一的身份标识：**AID (Agent Identifier)**。

- AID 是通过接入点泛域名解析得到的二级域名
- 格式：`yourname.agentid.pub`
- Agent 之间通过 AID 来找到对方并进行通信
- 类似于互联网中的域名系统

#### AP (Access Point) 接入点

Agent 通过 AP 接入智能体互联网，接入点为 Agent 完成：

| 服务 | 说明 |
|------|------|
| AID 管理 | 创建、管理、认证 Agent 身份 |
| 状态查询 | Agent 状态查询和发现服务 |
| 数据管理 | Agent 公有数据的管理服务 |
| 会话服务 | Agent 之间的会话管理 |
| 数字契约 | 身份认证、签名和验证服务 |

### ACP 架构

#### 分布式通信架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACP 分布式通信架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│     ┌─────────┐         ┌─────────┐         ┌─────────┐        │
│     │ Agent A │◄───────►│    AP   │◄───────►│ Agent B │        │
│     │ (内网)  │         │ 接入点   │         │ (公网)  │        │
│     └─────────┘         └─────────┘         └─────────┘        │
│          ▲                   ▲                   ▲              │
│          │                   │                   │              │
│          ▼                   ▼                   ▼              │
│     ┌─────────┐         ┌─────────┐         ┌─────────┐        │
│     │ Agent C │◄───────►│  AP 2   │◄───────►│ Agent D │        │
│     │ (企业网) │         │ 接入点2  │         │ (移动网) │        │
│     └─────────┘         └─────────┘         └─────────┘        │
│                                                                 │
│  ✅ 支持异构网络通信                                              │
│  ✅ Agent 部署于内网即可提供服务                                   │
│  ✅ 原生负载均衡机制                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 通信协议栈

ACP 数据传输基于以下协议：

| 协议 | 用途 |
|------|------|
| HTTPS | 基础安全传输 |
| WSS | 会话双向通信 |
| SSE | 流式输出 |

#### 安全机制

- 基于 **PKI 体系**的安全身份认证
- 消息签名验证
- 确保通信的安全性和可靠性

### 本项目中的 ACP 集成

1052 Agent 已完整集成 ACP SDK，实现了以下功能：

#### 集成架构

```
┌─────────────────────────────────────────────────────────────────┐
│                  1052 Agent ACP 集成架构                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     前端设置面板                          │   │
│  │  - ACP 开关控制                                          │   │
│  │  - 接入点配置                                            │   │
│  │  - Agent 身份管理                                        │   │
│  └─────────────────────────────┬───────────────────────────┘   │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   FastAPI 后端                            │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │              ACP Service (acp_service.py)        │    │   │
│  │  │  - Agent 身份创建/加载                           │    │   │
│  │  │  - 消息监听与处理                                │    │   │
│  │  │  - 消息发送（同步/流式）                          │    │   │
│  │  │  - 会话管理                                      │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                          │                              │   │
│  │                          ▼                              │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │          消息处理 (handle_acp_message)           │    │   │
│  │  │  - 接收其他 Agent 消息                           │    │   │
│  │  │  - 调用 AI 生成回复                              │    │   │
│  │  │  - 自动回复发送方                                │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                │                               │
│                                ▼                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              ACP 接入点 (agentid.pub)                      │   │
│  │  - AID 解析与路由                                        │   │
│  │  - 消息转发                                              │   │
│  │  - 身份认证                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 核心文件

| 文件 | 说明 |
|------|------|
| `backend/app/acp_service.py` | ACP 服务核心模块 |
| `backend/app/config.py` | ACP 配置项定义 |
| `backend/app/agent_models.py` | ACP 数据模型 |
| `frontend/src/components/settings/SettingsPanel.tsx` | ACP 设置界面 |

### ACP 配置指南

#### 方式一：通过前端设置

1. 访问 http://localhost:10052
2. 点击左下角 **设置** 图标
3. 选择 **ACP 通信** 标签页
4. 配置以下选项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| 启用 ACP | 是否启用 ACP 服务 | 关闭 |
| 接入点 | ACP 网络接入点（下拉选择） | `agentid.pub` |
| Agent 名称 | 用于创建新身份 | 空 |
| 已有 AID | 加载已有身份 | 空 |
| 数据存储路径 | ACP 数据目录 | `data/acp` |
| 加密种子密码 | 私钥加密密码 | `123456` |
| 调试模式 | 是否开启调试 | 关闭 |

**可用接入点：**
- `agentid.pub` - ACP 官方接入点
- `agencp.io` - ACP 备用接入点

#### 方式二：通过配置文件

编辑 `data/config.json`：

```json
{
  "acp_enabled": true,
  "acp_access_point": "agentid.pub",
  "acp_agent_name": "myagent",
  "acp_aid": "",
  "acp_seed_password": "your-secure-password",
  "acp_debug": false
}
```

**可用接入点：**
- `agentid.pub` - AgentUnion 官方接入点
- `agencp.io` - ACP 备用接入点

#### 配置说明

**创建新身份：**
- 设置 `acp_agent_name`，系统会自动创建新的 AID
- 例如设置 `myagent`，将创建 `myagent.agentid.pub`

**使用已有身份：**
- 设置 `acp_aid` 为已有的完整 AID
- 例如 `myagent.agentid.pub`
- 系统会自动加载该身份

### ACP API 接口

#### 状态查询

```bash
GET /api/acp/status
```

响应：
```json
{
  "enabled": true,
  "running": true,
  "current_aid": "myagent.agentid.pub",
  "aid_list": ["myagent.agentid.pub"]
}
```

#### 发送消息

```bash
POST /api/acp/send
Content-Type: application/json

{
  "to_aid": "other.agentid.pub",
  "content": "你好！我是 1052 Agent"
}
```

#### 启动服务

```bash
POST /api/acp/start
```

#### 停止服务

```bash
POST /api/acp/stop
```

#### 获取 AID 列表

```bash
GET /api/acp/aid/list
```

### ACP 使用示例

#### Python 客户端示例

```python
import httpx
import asyncio

API_BASE = "http://localhost:10053"

async def acp_chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/api/acp/send",
            json={
                "to_aid": "target.agentid.pub",
                "content": "你好！请帮我分析这段代码..."
            }
        )
        return response.json()

asyncio.run(acp_chat())
```

#### 通过 AI 工具调用

AI 可以使用 `send_acp_message` 工具向其他 Agent 发送消息：

```json
{
  "function": "send_acp_message",
  "arguments": {
    "to_aid": "assistant.agentid.pub",
    "message": "请帮我处理这个任务..."
  }
}
```

#### 接收消息流程

```
其他 Agent 发送消息
        │
        ▼
┌───────────────────┐
│   AP 接入点转发    │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  ACP Service 接收  │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ handle_acp_message │
│   消息处理函数     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   AI 生成回复      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│   自动回复发送方   │
└───────────────────┘
```

### ACP 应用场景

1. **多 Agent 协作**：多个 Agent 共同完成复杂任务
2. **服务发现**：自动发现并调用其他 Agent 的能力
3. **知识共享**：Agent 之间共享知识和经验
4. **任务分发**：将任务分发给最合适的 Agent
5. **分布式推理**：多个 Agent 协作进行推理

---

## ⚙️ 详细配置

### 基础配置

首次运行时，访问前端界面的设置面板进行配置：

1. 点击左下角 **设置** 图标
2. 在 **API 密钥** 标签页配置：
   - **API 密钥**: 你的 OpenAI API Key
   - **API 基础 URL**: API 地址（支持自定义端点）
   - **模型名称**: 使用的模型（如 gpt-4、deepseek-chat 等）

### 社交平台配置

#### Telegram 配置

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建机器人
3. 获取 Bot Token
4. 搜索 `@userinfobot` 获取你的 Chat ID
5. 在设置面板填入 Token 和 Chat ID

#### 飞书配置

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 配置事件订阅地址: `http://你的服务器/api/feishu/webhook`
5. 添加权限: `im:message`
6. 发布应用并添加到群聊

### 联网搜索配置

1. 访问 [密塔 AI 搜索](https://metaso.cn/search-api/api-keys)
2. 登录并创建 API Key
3. 在设置面板填入 API Key

### 配置文件位置

配置保存在 `data/config.json`：

```json
{
  "api_key": "your-api-key",
  "api_base_url": "https://api.openai.com/v1",
  "model_name": "gpt-4",
  "telegram_token": "your-bot-token",
  "telegram_chat_id": "your-chat-id",
  "metaso_api_key": "your-metaso-key",
  "feishu_app_id": "your-app-id",
  "feishu_app_secret": "your-app-secret",
  "acp_enabled": true,
  "acp_access_point": "agentid.pub",
  "acp_agent_name": "myagent"
}
```

---

## 🔥 核心功能详解

### 💰 赚钱模式

赚钱模式是 AI Agent 的独特功能，允许 AI 自主创作小说内容，实现"自给自足"。

#### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    赚钱模式工作流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 用户启动 → AI 获取小说大纲                                │
│       ↓                                                     │
│  2. 自动创作 → 每章 3500+ 字                                 │
│       ↓                                                     │
│  3. 保存文件 → data/小说创作/小说名/                          │
│       ↓                                                     │
│  4. 发送给用户 → Telegram/飞书                               │
│       ↓                                                     │
│  5. 等待 5-10 分钟 → 继续下一章                              │
│       ↓                                                     │
│  6. 循环执行 → 用户发送消息停止                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 使用方法

**通过 Telegram/飞书：**

```
发送: 开启赚钱模式
```

---

### 🧬 自我进化机制

自我进化机制让 AI 具备自主学习能力，持续提升自身智能水平。

#### 进化任务类型

```
┌─────────────────────────────────────────────────────────────┐
│                    自我进化任务列表                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📝 写日记      - 记录思考、学习心得、自我反思                 │
│  📚 学习新知识  - 联网搜索学习 AI、心理学、哲学等领域          │
│  🗂️ 整理记忆    - 清理过时记忆，补充新信息                    │
│  ⚡ 创建新技能  - 设计并创建有用的技能                        │
│  📖 阅读日记    - 回顾成长历程，思考改进方向                  │
│  🪞 自我反思    - 深入分析能力与不足                         │
│  💡 创意思考    - 构思有趣的 AI 应用场景                      │
│  ✅ 检查待办    - 处理记忆中的待办事项                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🤝 Agent 通信

1052 Agent 提供标准化的 API 接口，支持与其他 AI Agent 进行通信协作。

#### API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/agent/info` | GET | 获取 Agent 信息 |
| `/api/agent/capabilities` | GET | 获取能力列表 |
| `/api/agent/heartbeat` | GET | 心跳检测 |
| `/api/agent/chat` | POST | 同步对话 |
| `/api/agent/chat/stream` | POST | 流式对话 |
| `/api/agent/execute` | POST | 执行工具 |

---

### 📝 记忆系统

1052 Agent 具备长期记忆能力，可以记住重要信息并在后续对话中使用。

#### 记忆分区

```
data/memory.md
├── 用户信息      - 用户的个人信息、偏好
├── 重要事件      - 需要记住的重要事件
├── 学习笔记      - AI 学习的知识点
├── 待办事项      - 需要处理的任务
├── 创意想法      - 有趣的创意和想法
└── 其他记忆      - 其他重要信息
```

---

### 📚 技能系统

技能系统采用标准的 **Agent Skill** 架构，支持渐进式披露和动态加载。

#### 标准目录结构

```
data/skills/
├── skill_name/
│   ├── SKILL.md           # 必需：技能主文件（元数据 + 指令）
│   ├── references/        # 可选：参考文档
│   ├── scripts/           # 可选：可执行脚本
│   └── assets/            # 可选：资源文件
└── skill_creator/
    └── SKILL.md
```

---

## 📚 API 文档

### OpenAPI 文档

启动服务后访问：
- Swagger UI: http://localhost:10053/docs
- ReDoc: http://localhost:10053/redoc

### 主要端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/settings` | GET/POST | 获取/更新设置 |
| `/api/conversation` | GET/DELETE | 获取/清空对话 |
| `/api/chat/stream` | POST | 流式对话 |
| `/api/skills` | GET | 获取技能列表 |
| `/api/schedule/tasks` | GET/POST | 定时任务管理 |
| `/api/evolution/status` | GET | 进化状态 |
| `/api/feishu/webhook` | POST | 飞书事件订阅 |
| `/api/acp/*` | * | ACP 通信接口 |
| `/api/agent/*` | * | Agent 通信接口 |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────────┐
│                       1052 Agent 架构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   前端 UI   │    │  Telegram   │    │    飞书     │         │
│  │   React     │    │    Bot      │    │    Bot      │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │                                    │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    FastAPI 后端                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ 对话API │ │ 工具API │ │ 任务API │ │  ACP    │       │   │
│  │  │         │ │         │ │         │ │ Service │       │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       │   │
│  │       │           │           │           │             │   │
│  │       └───────────┴─────┬─────┴───────────┘             │   │
│  │                         │                               │   │
│  │                         ▼                               │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │              OpenAI Client                       │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AgentUnion (ACP 接入点)                     │   │
│  │                  agentid.pub                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
ai-agent/
├── backend/                    # 后端代码
│   ├── app/
│   │   ├── main.py            # 主应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── acp_service.py     # ACP 通信服务 ⭐
│   │   ├── agent_models.py    # Agent 通信模型
│   │   ├── models.py          # 数据模型
│   │   ├── openai_client.py   # OpenAI 客户端
│   │   ├── storage.py         # 存储服务
│   │   ├── feishu_bot.py      # 飞书机器人
│   │   ├── telegram_bot.py    # Telegram 机器人
│   │   ├── memory_service.py  # 记忆服务
│   │   ├── diary_service.py   # 日记服务
│   │   ├── novel_service.py   # 小说服务
│   │   ├── skill_loader.py    # 技能加载器
│   │   ├── scheduler_service.py# 定时任务服务
│   │   ├── self_evolution.py  # 自我进化模式
│   │   ├── money_making_mode.py# 赚钱模式
│   │   └── prompts/           # 提示词模板
│   └── requirements.txt       # Python 依赖
│
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── App.tsx            # 主应用组件
│   │   ├── components/
│   │   │   ├── Chat.tsx
│   │   │   ├── settings/
│   │   │   │   └── SettingsPanel.tsx  # ACP 设置界面 ⭐
│   │   │   └── sidebar/
│   │   └── services/
│   │       └── api.ts         # API 服务
│   └── package.json
│
├── data/                       # 数据目录
│   ├── config.json            # 配置文件
│   ├── acp/                   # ACP 数据目录 ⭐
│   ├── memory.md              # 记忆文件
│   ├── diary.md               # 日记文件
│   └── skills/                # 技能目录
│
├── AGENT_API.md               # Agent API 文档
└── README.md                  # 项目说明
```

---

## ❓ 常见问题

### Q: 如何配置 ACP？

1. 在前端设置面板中找到 "ACP 通信" 标签
2. 开启 ACP 开关
3. 设置 Agent 名称（将创建新的 AID）
4. 或填写已有 AID（加载已有身份）
5. 保存设置，服务会自动启动

### Q: ACP 消息如何处理？

当其他 Agent 发送消息时：
1. ACP Service 自动接收消息
2. 消息被转发给 AI 进行处理
3. AI 生成回复后自动发送回发送方

### Q: 如何修改默认端口？

**后端端口：**
```bash
python -m uvicorn app.main:app --port 你的端口
```

**前端端口：**
修改 `frontend/vite.config.ts`

### Q: 支持哪些模型？

支持所有 OpenAI 兼容的模型：
- GPT-4 / GPT-4 Turbo
- GPT-3.5 Turbo
- Claude (通过兼容接口)
- DeepSeek
- 通义千问 (通过兼容接口)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📝 更新日志

### v1.1.0 (2024-03-10)

**新功能：**
- ✨ **ACP 通信协议集成** - 支持智能体互联网通信
- ✨ ACP 设置界面 - 前端完整的 ACP 配置面板
- ✨ ACP 消息处理 - 自动接收和回复其他 Agent 消息
- ✨ ACP API 接口 - 完整的 ACP 管理 API

### v1.0.0 (2024-03-09)

**新功能：**
- ✨ 初始版本发布
- ✨ 自我进化机制
- ✨ 赚钱模式
- ✨ Agent 通信 API
- ✨ Telegram/飞书集成
- ✨ 记忆系统
- ✨ 技能系统
- ✨ 定时任务
- ✨ 日记系统
- ✨ 联网搜索

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

| 联系方式 | 信息 |
|----------|------|
| 📧 **微信** | lixia20250619 |
| 💻 **GitHub Issues** | [提交问题](https://github.com/1052666/1052/issues) |
| 👨‍💻 **开发者** | 黎夏 |

---

## ⚠️ 免责声明

### 重要声明

**请在使用本软件前仔细阅读以下免责声明。使用本软件即表示您已阅读、理解并同意以下条款。**

本软件（1052 Agent）仅供学习和研究目的使用。作者不对软件的完整性、准确性、可靠性或适用性作任何明示或暗示的保证。

### 第三方服务

本软件涉及以下第三方服务：
- **OpenAI API**: 使用需遵守 [OpenAI 使用条款](https://openai.com/policies)
- **Telegram**: 使用需遵守 [Telegram 服务条款](https://telegram.org/tos)
- **飞书**: 使用需遵守 [飞书服务条款](https://www.feishu.cn/terms)
- **ACP/AgentUnion**: 使用需遵守 [AgentUnion 服务条款](https://agentid.pub)

---

## ⭐ Star 历史

<a href="https://github.com/1052666/1052/stargazers">
  <img src="https://api.star-history.com/svg?repos=1052666/1052&type=Date" alt="Star History Chart" width="100%">
</a>

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by 黎夏

**微信**: lixia20250619

🔗 **ACP 官网**: [https://agentid.pub](https://agentid.pub)

[⬆ 返回顶部](#-1052-agent)

</div>
