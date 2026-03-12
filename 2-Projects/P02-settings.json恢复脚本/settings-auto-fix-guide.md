# Claude 设置自动修复：大白话说明

## 这套东西到底在干嘛

一句话：
**每次 cc-switch 把 `settings.json` 重置后，系统会自动把你真正需要的配置补回来。**

重点是“补回来”，不是“整文件覆盖”。
所以它会保住关键配置（比如插件启用和状态栏），同时尽量不乱动你别的字段。

---

## 文件分工（你只要记这个）

- `C:\Users\Cc\.claude\settings.baseline.json`
  - 这是“保底模板”（基线）
  - 放必须保护的关键配置（env / enabledPlugins / statusLine）

- `C:\Users\Cc\.claude\fix-settings.ps1`
  - 这是“自动修复工人”
  - 负责读取 baseline + 当前 settings + 已安装插件，然后做合并修复

- 计划任务 `ClaudeCode-SettingsMergeFix`
  - 这是“自动触发器”
  - **每次登录只触发 1 次**（不轮询）调用 `fix-settings.ps1`

---

## 运行逻辑（大白话版）

每次脚本运行时，大概做这几步：

1. 读 `settings.baseline.json`（关键配置来源）
2. 读当前 `settings.json`
3. 如果发现像“被重置过”（比如少了 `enabledPlugins` / `statusLine`），就优先参考 `settings.last-good.json` 做恢复底稿
4. 把 baseline 里的关键 env 键值补进来
5. 根据 `installed_plugins.json` 动态重建 `enabledPlugins`
   - 这样未来新装插件也能自动兼容
6. 如果检测到 claude-hud 已安装：
   - **有现成 `statusLine` 就保留不动**（避免把你修好的 HUD 命令覆盖回去）
   - 只有在 `statusLine` 缺失时，才从 baseline 回填
7. 写回 `settings.json`，并更新 `settings.last-good.json`

---

## 你平时怎么用

## 场景 A：日常使用（推荐）

你啥都不用干。
登录后计划任务会自动修。

## 场景 B：你想手动马上修一次

在 PowerShell 执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\Cc\.claude\fix-settings.ps1"
```

看到：

```text
OK: settings.json repaired via baseline+merge strategy.
```

就说明修复完成。

## 场景 C：你要检查自动任务在不在（且是否单次触发）

```powershell
Get-ScheduledTask -TaskName "ClaudeCode-SettingsMergeFix"
```

能查到任务，状态一般是 `Ready`，就正常。

想确认不是轮询触发，可再看触发器数量（应为 1 个）：

```powershell
(Get-ScheduledTask -TaskName "ClaudeCode-SettingsMergeFix").Triggers.Count
```

---

## 你最关心的几个结果

- ✅ 重置后会自动补回 `enabledPlugins` 和 `statusLine`
- ✅ 不会粗暴覆盖整个 `settings.json`
- ✅ 对后续新插件安装兼容（从 installed_plugins 动态重建）
- ✅ 脚本可重复运行（幂等）

---

## 出问题时先看哪里

优先看：

1. `C:\Users\Cc\.claude\settings.json`（结果文件）
2. `C:\Users\Cc\.claude\settings.last-good.json`（恢复基准）
3. 计划任务是否存在并可启动

如果还不对，再手动跑一次 `fix-settings.ps1` 看输出。
