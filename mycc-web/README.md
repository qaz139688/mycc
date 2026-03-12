# mycc-web

基于 Next.js 的 mycc Web 版本。

## 贡献指南

欢迎提交 PR！在提交前请确保：

### 提交前检查清单

- [ ] 代码能够成功构建 (`pnpm build`)
- [ ] 通过 ESLint 检查 (`pnpm lint`)
- [ ] 通过 Prettier 格式检查 (`pnpm format:check`)
- [ ] 代码中没有 `any` 类型（除非有充分理由并添加了注释）
- [ ] 本地运行正常 (`pnpm dev`)

### Next.js 开发规范

#### 文件结构

```
src/
├── app/              # Next.js App Router 页面
├── components/       # React 组件
│   ├── ui/          # 通用 UI 组件
│   └── features/    # 功能性组件
├── lib/             # 工具函数
├── hooks/           # 自定义 Hooks
└── types/           # TypeScript 类型定义
```

#### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserProfile.tsx` |
| 工具函数 | camelCase | `formatDate.ts` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 类型/接口 | PascalCase | `interface User {}` |
| Hook | use + PascalCase | `useAuth.ts` |

#### TypeScript 规范

**严格禁止使用 `any` 类型**，除非：
- 第三方库没有类型定义
- 极端复杂的泛型场景

使用时必须添加注释：

```tsx
// @ts-expect-error: Legacy API without type definitions
const data: any = legacyFunction()
```

#### 组件规范

```tsx
// ✅ 推荐：明确的类型定义
interface UserCardProps {
  user: {
    name: string
    email: string
  }
  onEdit?: () => void
}

export function UserCard({ user, onEdit }: UserCardProps) {
  return (
    <div className="rounded-lg border p-4">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && <button onClick={onEdit}>Edit</button>}
    </div>
  )
}

// ❌ 避免：使用 any
export function UserCard({ user }: any) { // 禁止
  return <div>{user.name}</div>
}
```

#### Server vs Client Components

```tsx
// Server Component（默认，可以直接 await）
export default async function Page() {
  const data = await fetchData()
  return <div>{data}</div>
}

// Client Component（需要交互时使用）
'use client'

export function InteractiveButton() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

**原则**：
- 默认使用 Server Component
- 需要 hooks、事件处理时才使用 Client Component
- 尽可能将交互部分拆分为小的 Client Component

### 提交信息规范

使用语义化提交：

```bash
feat: 添加用户头像上传功能
fix: 修复登录页面重定向问题
docs: 更新 API 文档
style: 格式化代码
refactor: 重构用户验证逻辑
perf: 优化图片加载性能
test: 添加用户模块测试
chore: 更新依赖包
```

### 提交流程

1. Fork 仓库并克隆到本地
2. 创建功能分支：`git checkout -b feature/your-feature-name`
3. 开发并测试
4. 运行检查：
   ```bash
   pnpm format        # 自动格式化
   pnpm lint          # 检查代码规范
   pnpm build         # 构建项目
   ```
5. 提交代码：`git commit -m "feat: your feature"`
6. 推送分支：`git push origin feature/your-feature-name`
7. 创建 Pull Request

## 常见问题

### 构建失败？

```bash
rm -rf node_modules .next
pnpm install
pnpm build
```

### ESLint 报错 `any` 类型？

检查代码中是否使用了 `any`，如果必须使用，添加注释说明原因。

### import 路径报错？

使用 `@/` alias：

```tsx
// ✅ 使用 @ alias
import { Button } from '@/components/ui/button'

// ❌ 避免深层相对路径
import { Button } from '../../../components/ui/button'
```

---

感谢你的贡献！
