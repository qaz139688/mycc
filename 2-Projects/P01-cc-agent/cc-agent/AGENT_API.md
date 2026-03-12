# 1052 Agent 通信接口文档

## 概述

1052 Agent 提供了一套完整的 RESTful API 接口，允许其他 AI Agent、应用程序或服务与之进行通信和协作。本文档详细描述了所有可用的 API 端点、请求格式和响应格式。

## 基础信息

- **基础 URL**: `http://localhost:10053`
- **API 版本**: v1.0.0
- **Agent ID**: `1052-agent`
- **Agent 名称**: `1052 Agent`
- **支持格式**: JSON
- **字符编码**: UTF-8

---

## API 端点

### 1. 获取 Agent 信息

获取 Agent 的基本信息、能力和可用端点。

**请求**
```
GET /api/agent/info
```

**响应**
```json
{
  "agent_id": "1052-agent",
  "agent_name": "1052 Agent",
  "version": "1.0.0",
  "capabilities": [
    "chat",
    "stream_chat",
    "tool_execution",
    "file_operations",
    "shell_commands",
    "web_search",
    "memory_management",
    "skill_system",
    "scheduled_tasks"
  ],
  "description": "一个功能强大的 AI Agent，支持多种工具和功能，可与其他 Agent 进行通信协作",
  "endpoints": [
    {"path": "/api/agent/info", "method": "GET", "description": "获取 Agent 信息"},
    {"path": "/api/agent/chat", "method": "POST", "description": "发送消息并获取回复"},
    {"path": "/api/agent/chat/stream", "method": "POST", "description": "流式对话"},
    {"path": "/api/agent/capabilities", "method": "GET", "description": "获取能力列表"},
    {"path": "/api/agent/heartbeat", "method": "GET", "description": "获取心跳状态"}
  ]
}
```

---

### 2. 获取能力列表

获取 Agent 支持的所有能力及其参数定义。

**请求**
```
GET /api/agent/capabilities
```

**响应**
```json
{
  "agent_id": "1052-agent",
  "capabilities": [
    {
      "name": "chat",
      "description": "与 Agent 进行对话",
      "parameters": {
        "message": {"type": "string", "description": "消息内容"},
        "conversation_id": {"type": "string", "description": "会话ID（可选）"},
        "context": {"type": "array", "description": "上下文消息（可选）"}
      },
      "required": ["message"]
    },
    {
      "name": "execute_shell",
      "description": "执行 Shell 命令",
      "parameters": {
        "command": {"type": "string", "description": "要执行的命令"},
        "shell_type": {"type": "string", "enum": ["cmd", "powershell"], "description": "Shell 类型"},
        "timeout": {"type": "integer", "description": "超时时间（秒）"}
      },
      "required": ["command"]
    },
    {
      "name": "file_operation",
      "description": "文件操作",
      "parameters": {
        "operation": {"type": "string", "enum": ["read", "write", "append", "delete", "list", "exists"], "description": "操作类型"},
        "path": {"type": "string", "description": "文件路径"},
        "content": {"type": "string", "description": "文件内容（写入时需要）"}
      },
      "required": ["operation", "path"]
    },
    {
      "name": "web_search",
      "description": "联网搜索",
      "parameters": {
        "query": {"type": "string", "description": "搜索关键词"}
      },
      "required": ["query"]
    },
    {
      "name": "send_message",
      "description": "发送消息到 Telegram 或飞书",
      "parameters": {
        "platform": {"type": "string", "enum": ["telegram", "feishu"], "description": "平台"},
        "message": {"type": "string", "description": "消息内容"}
      },
      "required": ["platform", "message"]
    }
  ]
}
```

---

### 3. 获取心跳状态

获取 Agent 的运行状态和健康检查信息。

**请求**
```
GET /api/agent/heartbeat
```

**响应**
```json
{
  "agent_id": "ai-agent-main",
  "status": "online",
  "timestamp": 1709876543,
  "current_tasks": 2,
  "uptime_seconds": 86400
}
```

**状态说明**
- `online`: Agent 在线且空闲
- `busy`: Agent 正在执行任务
- `offline`: Agent 离线

---

### 4. 发送消息（同步）

向 Agent 发送消息并获取完整回复。

**请求**
```
POST /api/agent/chat
Content-Type: application/json
```

**请求体**
```json
{
  "message": "你好，请帮我分析一下这个文件的内容",
  "conversation_id": "optional-conversation-id",
  "agent_id": "caller-agent-id",
  "agent_name": "Caller Agent",
  "context": [
    {
      "role": "user",
      "content": "之前的消息内容",
      "timestamp": 1709876543000
    },
    {
      "role": "assistant",
      "content": "之前的回复内容",
      "timestamp": 1709876544000
    }
  ],
  "metadata": {
    "source": "external_agent",
    "priority": "normal"
  }
}
```

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 消息内容 |
| conversation_id | string | 否 | 会话ID，用于保持对话上下文 |
| agent_id | string | 否 | 调用方 Agent 的唯一标识 |
| agent_name | string | 否 | 调用方 Agent 的名称，会显示在消息前缀 |
| context | array | 否 | 上下文消息列表，用于提供历史对话 |
| metadata | object | 否 | 额外的元数据 |

**响应**
```json
{
  "success": true,
  "conversation_id": "conv-abc123",
  "response": "好的，我来帮您分析文件内容。首先，我需要知道您指的是哪个文件...",
  "agent_id": "ai-agent-main",
  "agent_name": "1052 Agent",
  "timestamp": 1709876545000,
  "tool_calls": [
    {
      "tool_call_id": "call_xyz",
      "function_name": "file_operation",
      "arguments": "{\"operation\": \"read\", \"path\": \"/path/to/file\"}"
    }
  ]
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| success | boolean | 请求是否成功 |
| conversation_id | string | 会话ID，可用于后续对话 |
| response | string | Agent 的回复内容 |
| agent_id | string | Agent 的唯一标识 |
| agent_name | string | Agent 的名称 |
| timestamp | integer | 响应时间戳（毫秒） |
| tool_calls | array | 调用的工具列表（可选） |
| error | string | 错误信息（仅在失败时） |

---

### 5. 发送消息（流式）

向 Agent 发送消息并以流式方式接收回复，适合长回复场景。

**请求**
```
POST /api/agent/chat/stream
Content-Type: application/json
```

**请求体**
```json
{
  "message": "请帮我写一篇关于 AI Agent 通信的文章",
  "agent_name": "Research Agent"
}
```

**响应格式**

响应为 Server-Sent Events (SSE) 格式：

```
data: {"type": "conversation_id", "conversation_id": "conv-abc123"}

data: {"type": "content", "content": "好的"}

data: {"type": "content", "content": "，我来"}

data: {"type": "content", "content": "为您撰写"}

data: {"type": "tool_call", "tool_call": {"id": "call_1", "function_name": "web_search", "arguments": "{\"query\": \"AI Agent communication\"}"}}

data: {"type": "tool_result", "tool_call_id": "call_1", "result": "..."}

data: {"type": "content", "content": "这篇文章..."}

data: {"type": "done", "conversation_id": "conv-abc123", "agent_id": "1052-agent", "agent_name": "1052 Agent"}
```

**事件类型说明**

| 类型 | 说明 |
|------|------|
| conversation_id | 会话ID |
| content | 内容片段 |
| tool_call | 工具调用 |
| tool_result | 工具执行结果 |
| done | 流结束 |
| error | 错误信息 |

---

### 6. 执行工具

直接调用 Agent 的工具函数。

**请求**
```
POST /api/agent/execute?tool_name=execute_shell_command
Content-Type: application/json
```

**请求体**
```json
{
  "command": "dir",
  "shell_type": "cmd",
  "timeout": 30
}
```

**响应**
```json
{
  "success": true,
  "agent_id": "ai-agent-main",
  "tool_name": "execute_shell_command",
  "result": {
    "success": true,
    "output": "Volume in drive C is OS...",
    "exit_code": 0
  },
  "timestamp": 1709876545000
}
```

---

## 可用工具列表

### execute_shell_command
执行 Shell 命令。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| command | string | 是 | 要执行的命令 |
| shell_type | string | 否 | Shell 类型：cmd 或 powershell |
| timeout | integer | 否 | 超时时间（秒），最大 300 |

### file_operation
文件操作。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| operation | string | 是 | 操作类型：read, write, append, delete, list, exists, edit, replace |
| path | string | 是 | 文件路径 |
| content | string | 否 | 文件内容（写入/追加时需要） |
| encoding | string | 否 | 编码，默认 utf-8 |

### web_search
联网搜索。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索关键词 |

### send_telegram_message
发送 Telegram 消息。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 消息内容 |

### send_feishu_message
发送飞书消息。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| message | string | 是 | 消息内容 |
| receive_id | string | 否 | 接收者ID，不填则使用默认配置 |

### create_skill
创建技能。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 技能名称 |
| description | string | 是 | 技能描述 |
| system_prompt | string | 是 | 系统提示词 |

### schedule_task
创建定时任务。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 任务名称 |
| description | string | 否 | 任务描述 |
| trigger_type | string | 是 | 触发类型：once, interval |
| trigger_time | string | 否 | 触发时间（once 类型需要） |
| interval_seconds | integer | 否 | 间隔秒数（interval 类型需要） |
| prompt | string | 是 | 执行的提示词 |

### add_memory / update_memory / delete_memory / read_memory
记忆管理。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| section | string | 是 | 记忆分区 |
| content | string | 是 | 记忆内容 |

### write_diary / read_diary
日记管理。

**参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 日记标题 |
| content | string | 是 | 日记内容 |
| mood | string | 否 | 心情，默认"平静" |

---

## 错误处理

所有 API 在发生错误时会返回相应的错误信息：

```json
{
  "success": false,
  "conversation_id": "",
  "response": "",
  "agent_id": "1052-agent",
  "agent_name": "1052 Agent",
  "timestamp": 1709876545000,
  "error": "API key not configured. Please set it in settings."
}
```

**常见错误码**

| HTTP 状态码 | 说明 |
|-------------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 使用示例

### Python 示例

```python
import httpx
import json

API_BASE = "http://localhost:10053"

async def chat_with_agent(message: str, agent_name: str = "Python Client"):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/api/agent/chat",
            json={
                "message": message,
                "agent_name": agent_name
            },
            timeout=60
        )
        return response.json()

async def stream_chat(message: str):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{API_BASE}/api/agent/chat/stream",
            json={"message": message},
            timeout=120
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if data["type"] == "content":
                        print(data["content"], end="", flush=True)
                    elif data["type"] == "done":
                        print("\n[完成]")

async def main():
    result = await chat_with_agent("你好，请介绍一下你自己")
    print(result["response"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### JavaScript 示例

```javascript
const API_BASE = 'http://localhost:10053';

async function chatWithAgent(message, agentName = 'JS Client') {
  const response = await fetch(`${API_BASE}/api/agent/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      agent_name: agentName
    })
  });
  return await response.json();
}

async function streamChat(message, onChunk) {
  const response = await fetch(`${API_BASE}/api/agent/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        if (data.type === 'content') {
          onChunk(data.content);
        }
      }
    }
  }
}

// 使用示例
chatWithAgent('你好').then(result => {
  console.log(result.response);
});
```

### cURL 示例

```bash
# 获取 Agent 信息
curl http://localhost:10053/api/agent/info

# 发送消息
curl -X POST http://localhost:10053/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，请介绍一下你自己", "agent_name": "cURL Client"}'

# 执行工具
curl -X POST "http://localhost:10053/api/agent/execute?tool_name=file_operation" \
  -H "Content-Type: application/json" \
  -d '{"operation": "read", "path": "/path/to/file.txt"}'
```

---

## 最佳实践

### 1. 会话管理
- 使用 `conversation_id` 保持对话上下文
- 对于新对话，不传递 `conversation_id`，系统会自动创建

### 2. 流式响应
- 对于长回复，推荐使用流式接口 `/api/agent/chat/stream`
- 流式接口可以更快地开始显示内容，提升用户体验

### 3. 错误处理
- 始终检查响应中的 `success` 字段
- 错误信息在 `error` 字段中

### 4. 超时设置
- 同步接口建议设置 60 秒以上超时
- 流式接口建议设置 120 秒以上超时

### 5. Agent 标识
- 建议传递 `agent_id` 和 `agent_name`，便于追踪和调试
- 消息会显示来源 Agent 的名称

---

## 安全建议

1. **API 访问控制**: 在生产环境中，建议添加认证机制
2. **输入验证**: 对用户输入进行适当的验证和清理
3. **速率限制**: 实施速率限制以防止滥用
4. **HTTPS**: 在生产环境中使用 HTTPS 加密通信

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.0.0 | 2024-03-09 | 初始版本，支持基础对话、工具调用、流式响应 |

---

## 联系方式

如有问题或建议，请联系开发者：黎夏(微信：lixia20250619)
