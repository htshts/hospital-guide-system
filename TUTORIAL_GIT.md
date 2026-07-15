# 医院智能导诊系统 — Git 版本化管理搭建教程

> 本教程在项目搭建的每一步中融入 Git 版本控制思想。不是单独学 Git，而是在**真实开发流程中**自然地使用 Git，让版本管理成为开发习惯。
>
> 配合 `TUTORIAL_PYCHARM.md` 使用：搭建代码时参照那份文档，Git 操作参照本文档。

---

## 目录

- [第 0 章：Git 基础概念](#第-0-章git-基础概念)
- [第 1 章：项目初始化 — 让项目从一开始就有版本记录](#第-1-章项目初始化--让项目从一开始就有版本记录)
- [第 2 章：.gitignore — 告诉 Git 哪些文件不需要管](#第-2-章gitignore--告诉-git-哪些文件不需要管)
- [第 3 章：第一次提交 — 记录项目骨架](#第-3-章第一次提交--记录项目骨架)
- [第 4 章：分支策略 — 用分支管理功能开发](#第-4-章分支策略--用分支管理功能开发)
- [第 5 章：数据层开发 — 第一个功能分支](#第-5-章数据层开发--第一个功能分支)
- [第 6 章：模型层开发](#第-6-章模型层开发)
- [第 7 章：API 层开发](#第-7-章api-层开发)
- [第 8 章：主入口与首次能运行](#第-8-章主入口与首次能运行)
- [第 9 章：前端开发](#第-9-章前端开发)
- [第 10 章：联调与修复](#第-10-章联调与修复)
- [第 11 章：打标签 — 标记里程碑版本](#第-11-章打标签--标记里程碑版本)
- [第 12 章：PyCharm 中的 Git 图形化操作](#第-12-章pycharm-中的-git-图形化操作)
- [附录 A：提交信息规范](#附录-a提交信息规范)
- [附录 B：Git 常用命令速查](#附录-b-git-常用命令速查)
- [附录 C：完整提交历史参考](#附录-c-完整提交历史参考)

---

## 第 0 章：Git 基础概念

### 0.1 为什么要用 Git？

> **场景**：你写了一整天代码，突然发现改出了 bug，想回到之前的版本——但没有 Git，你只能凭记忆手动改回去。
>
> **Git 解决的问题**：
> 1. **版本回溯** — 随时回到任何一个历史版本
> 2. **改动追踪** — 知道谁在什么时候改了什么、为什么改
> 3. **分支开发** — 在不影响主线的情况下开发新功能
> 4. **协作基础** — 多人同时开发不冲突
> 5. **备份保障** — 代码推送到远程仓库，本地丢了也不怕

### 0.2 核心概念

```
工作区 (Working Directory)
    │  你在 PyCharm 中看到的文件
    │  git add ↓
暂存区 (Staging Area)
    │  "准备提交"的文件集合
    │  git commit ↓
本地仓库 (Local Repository)
    │  已记录的提交历史
    │  git push ↓
远程仓库 (Remote Repository)
       GitHub / Gitee / 公司内网 GitLab
```

| 概念 | 通俗解释 |
|------|---------|
| **工作区** | 你正在编辑的文件，PyCharm 左侧目录树看到的 |
| **暂存区** | "购物车"——把要提交的改动先放进来 |
| **本地仓库** | "收银台"——提交后改动被永久记录 |
| **远程仓库** | "云备份"——推送到服务器，别人能拉取 |
| **提交 (commit)** | 一次"存档"——记录当前代码状态 |
| **分支 (branch)** | 一条独立的开发线，不影响其他线 |
| **合并 (merge)** | 把分支的改动合并回主线 |

### 0.3 安装与配置 Git

**安装 Git：**
- Windows：https://git-scm.com/download/win （下载后一路 Next）
- Mac：`brew install git`
- 验证：终端输入 `git --version`，应显示版本号

**首次使用配置：**

```bash
# 配置你的身份（每次提交都会带上这些信息）
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 配置默认分支名为 main（业界惯例）
git config --global init.defaultBranch main

# 配置中文文件名不乱码
git config --global core.quotepath false
```

> **提示**：PyCharm 自带 Git 支持，安装 Git 后 PyCharm 会自动检测到。你可以在 PyCharm 中用图形界面操作 Git，也可以在终端用命令行。

### ✅ 本章验证
- [ ] `git --version` 能输出版本号
- [ ] `git config --global user.name` 能看到你的名字

---

## 第 1 章：项目初始化 — 让项目从一开始就有版本记录

> **原则**：项目创建的第一件事就是 `git init`，让之后的每一步都有记录。

### 1.1 在 PyCharm 中创建项目

按照 `TUTORIAL_PYCHARM.md` 第 1 章创建 PyCharm 项目（项目名 `hospital-guide`）。

### 1.2 初始化 Git 仓库

**方式一：PyCharm 图形界面（推荐）**

1. 菜单栏：**`VCS → Enable Version Control Integration`**（或 `Git → Enable Version Control Integration`）
2. 选择 **`Git`**
3. 点击 **OK**

```
┌──────────────────────────────────┐
│  Enable Version Control Integration │
│                                    │
│  Select a version control system:  │
│  [Git ▼]                           │
│                                    │
│         [OK]    [Cancel]           │
└──────────────────────────────────┘
```

初始化后，你会注意到：
- 左侧文件名变成**绿色**（表示未跟踪的新文件）
- 底部出现 **Git** 工具窗口标签
- 右上角出现 Git 相关按钮（commit、push、pull 等）

**方式二：终端命令行**

在 PyCharm 底部 Terminal 中：

```bash
git init
```

### 1.3 确认初始化成功

```bash
git status
```

应该输出类似：

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .idea/
        venv/

nothing added to commit but untracked files present
```

> 这说明 Git 仓库已初始化，但还没有任何文件被跟踪。接下来要配置 `.gitignore` 来排除不需要版本控制的文件。

### ✅ 本章验证
- [ ] 项目根目录下有 `.git/` 隐藏目录
- [ ] PyCharm 底部出现 Git 标签
- [ ] 文件名显示为绿色

---

## 第 2 章：.gitignore — 告诉 Git 哪些文件不需要管

> **原则**：不是所有文件都应该进版本库。虚拟环境、缓存文件、IDE 配置等不应该提交。

### 2.1 创建 .gitignore 文件

在 PyCharm 中，右键项目根目录 → **`New → File`** → 输入 `.gitignore`

### 2.2 .gitignore 内容

```gitignore
# ===== Python =====
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/

# ===== 虚拟环境 =====
venv/
env/
ENV/

# ===== IDE 配置 =====
.idea/
.vscode/
*.swp
*.swo

# ===== 环境变量（含敏感信息，绝不提交）=====
.env
.env.local
.env.*.local

# ===== Docker 数据卷 =====
volumes/

# ===== 日志 =====
*.log
logs/

# ===== 操作系统文件 =====
.DS_Store
Thumbs.db
desktop.ini

# ===== 临时文件 =====
*.tmp
*.bak
*~

# ===== PyCharm 特定 =====
.idea/workspace.xml
.idea/shelf/
.idea/httpRequests/
```

### 2.3 .gitignore 规则说明

| 语法 | 含义 | 示例 |
|------|------|------|
| `file` | 忽略指定文件 | `.env` |
| `dir/` | 忽略整个目录 | `venv/` |
| `*.ext` | 忽略所有该后缀的文件 | `*.log` |
| `!file` | 取消忽略（例外） | `!important.log` |
| `dir/*/` | 忽略目录下所有子目录 | `logs/*/` |

> **重要**：`.env` 文件包含 API Key 等敏感信息，**绝对不能**提交到 Git 仓库。`.gitignore` 中已排除。

### 2.4 如果已经提交了不该提交的文件

```bash
# 从 Git 中移除但保留本地文件
git rm --cached <文件名>

# 移除整个目录
git rm --cached -r <目录名>

# 然后重新提交
git commit -m "chore: 从版本库移除不应跟踪的文件"
```

### ✅ 本章验证
- [ ] `.gitignore` 文件已创建
- [ ] `git status` 中不再显示 `venv/` 和 `.idea/` 目录
- [ ] `.env` 文件（如果存在）不在 `git status` 列表中

---

## 第 3 章：第一次提交 — 记录项目骨架

> **原则**：每一次有意义的改动都应该提交。项目骨架搭好了，这就是第一个提交点。

### 3.1 暂存文件

**方式一：PyCharm 图形界面**

1. 选中要提交的文件（左侧文件树）
2. 右键 → **`Git → Add`**（或快捷键 `Ctrl+Alt+A`）

**方式二：终端命令**

```bash
# 添加所有文件到暂存区
git add .

# 或只添加特定文件
git add .gitignore backend/requirements.txt
```

> **区别**：`git add .` 添加所有改动，`git add <文件>` 只添加指定文件。开发中建议精确添加，避免误提交。

### 3.2 查看暂存状态

```bash
git status
```

应该显示：

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitignore
        new file:   backend/app/__init__.py
        new file:   backend/app/api/__init__.py
        new file:   backend/app/models/__init__.py
        new file:   backend/requirements.txt
```

### 3.3 创建提交

**方式一：PyCharm 图形界面**

1. 点击右上角 **绿色对勾 ✓**（Commit 按钮），或 `Ctrl+K`
2. 在弹出的 Commit 窗口中：

```
┌───────────────────────────────────────────┐
│  Commit Changes                            │
│                                            │
│  Files:                                    │
│  ☑ .gitignore                  (new)      │
│  ☑ backend/app/__init__.py     (new)      │
│  ☑ backend/requirements.txt    (new)      │
│                                            │
│  Commit Message:                           │
│  ┌──────────────────────────────────────┐ │
│  │ chore: 初始化项目结构与依赖配置         │ │
│  │                                        │ │
│  │ - 创建 backend/frontend 目录骨架       │ │
│  │ - 配置 requirements.txt               │ │
│  │ - 添加 .gitignore                    │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  [Commit]  [Commit and Push...]            │
└───────────────────────────────────────────┘
```

3. 勾选要提交的文件
4. 输入提交信息
5. 点击 **Commit**

**方式二：终端命令**

```bash
git commit -m "chore: 初始化项目结构与依赖配置

- 创建 backend/frontend 目录骨架
- 配置 requirements.txt
- 添加 .gitignore"
```

> **提交信息规范**：使用 Conventional Commits 格式，详见附录 A。简单来说：
> - `feat:` 新功能
> - `fix:` 修 bug
> - `chore:` 杂项（配置、依赖等）
> - `docs:` 文档
> - `refactor:` 重构

### 3.4 查看提交历史

```bash
git log --oneline
```

输出：

```
a1b2c3d (HEAD -> main) chore: 初始化项目结构与依赖配置
```

或在 PyCharm 中：底部 **Git 标签** → 左侧 **Log** 标签页，可以看到可视化的提交历史。

```
┌─ Git ────────────────────────────────────────┐
│  Log    Console    Commit    [Refresh]        │
│                                                │
│  ●  a1b2c3d  (HEAD -> main)                  │
│     chore: 初始化项目结构与依赖配置            │
│     Author: 你的名字 <your@email.com>         │
│     Date: 2026-07-08 16:30                    │
│                                                │
│     Files: .gitignore, backend/..., ...        │
└──────────────────────────────────────────────┘
```

### ✅ 本章验证
- [ ] `git log` 能看到第一次提交
- [ ] PyCharm 左侧文件名从绿色变为白色（已跟踪）
- [ ] Git Log 中能看到提交记录

---

## 第 4 章：分支策略 — 用分支管理功能开发

> **原则**：不要一直在 main 分支上写代码。每个功能开一个分支，写完合并回 main。这样 main 始终是"可运行的正确版本"。

### 4.1 分支模型

```
main (主干 — 始终可运行)
  │
  ├── feature/data-layer      ← 数据层开发分支
  │     └── 合并回 main
  │
  ├── feature/models          ← 模型层开发分支
  │     └── 合并回 main
  │
  ├── feature/api-department  ← 科室推荐 API 分支
  │     └── 合并回 main
  │
  ├── feature/api-doctor      ← 医生查询 API 分支
  │     └── 合并回 main
  │
  └── feature/frontend        ← 前端开发分支
        └── 合并回 main
```

### 4.2 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能 | `feature/api-department` |
| `fix/` | 修 bug | `fix/cors-error` |
| `hotfix/` | 紧急修复 | `hotfix/port-conflict` |
| `refactor/` | 重构 | `refactor/api-structure` |
| `docs/` | 文档 | `docs/readme` |

### 4.3 创建第一个功能分支

**方式一：PyCharm 图形界面**

1. 右下角点击分支名（如 `main`）

```
  hospital-guide | main ▼ | Python 3.10 | UTF-8
                   ↑
              点击这里切换/创建分支
```

2. 选择 **`+ New Branch`**
3. 输入分支名：`feature/data-layer`
4. 点击 **Create**

**方式二：终端命令**

```bash
# 创建并切换到新分支
git checkout -b feature/data-layer

# 等价于以下两条命令：
git branch feature/data-layer   # 创建分支
git checkout feature/data-layer  # 切换到分支
```

### 4.4 在分支上工作

现在你在 `feature/data-layer` 分支上。接下来编写的所有代码都只影响这个分支，main 分支不受影响。

```bash
# 确认当前分支
git branch
# * feature/data-layer    ← 星号表示当前分支
#   main
```

### 4.5 查看分支间差异

开发过程中随时查看当前分支和 main 的差异：

```bash
# 查看有哪些文件不同
git diff main --stat

# 查看具体代码差异
git diff main
```

在 PyCharm 中：菜单 `Git → Compare with Branch...` → 选择 `main`，可以可视化对比。

### ✅ 本章验证
- [ ] 已创建并切换到 `feature/data-layer` 分支
- [ ] 右下角显示当前分支名
- [ ] `git branch` 显示星号在功能分支上

---

## 第 5 章：数据层开发 — 第一个功能分支

> 现在在 `feature/data-layer` 分支上，按照 TUTORIAL_PYCHARM.md 第 4.1 节创建 4 个 JSON 数据文件。

### 5.1 编写数据文件

创建以下文件（参照 TUTORIAL_PYCHARM.md）：
- `backend/app/data/departments.json`
- `backend/app/data/doctors.json`
- `backend/app/data/symptom_disease.json`
- `backend/app/data/cost_insurance.json`

### 5.2 提交数据文件

```bash
# 查看改动
git status

# 添加文件
git add backend/app/data/

# 提交
git commit -m "feat(data): 添加科室、医生、症状、费用数据

- departments.json: 10个科室数据
- doctors.json: 10位医生数据
- symptom_disease.json: 16个症状到疾病映射
- cost_insurance.json: 5个科室费用与医保政策"
```

### 5.3 合并回 main

数据层开发完成，合并回主干：

**方式一：PyCharm 图形界面**

1. 先切换到 main：右下角点击 `feature/data-layer` → 选择 `main` → **Checkout**
2. 合并：菜单 `Git → Merge...` → 选择 `feature/data-layer` → **Merge**

```
┌───────────────────────────────┐
│  Merge Branches                │
│                                │
│  Branches to merge:            │
│  ☑ feature/data-layer         │
│                                │
│  [--no-ff] [--squash]         │
│                                │
│  [Merge]  [Cancel]            │
└───────────────────────────────┘
```

> **合并方式选择**：
> - **Merge**（默认 `--no-ff`）：保留分支历史，推荐
> - **Squash**：把分支上的多个提交压缩成一个

**方式二：终端命令**

```bash
# 切换到 main
git checkout main

# 合并功能分支
git merge feature/data-layer

# 删除已合并的功能分支（可选，保持分支列表干净）
git branch -d feature/data-layer
```

### 5.4 合并后的提交历史

```bash
git log --oneline --graph
```

```
*   c3d4e5f (HEAD -> main) Merge branch 'feature/data-layer'
|\
| * b2c3d4e feat(data): 添加科室、医生、症状、费用数据
|/
* a1b2c3d chore: 初始化项目结构与依赖配置
```

> 看到这个图就对了——main 上有一个合并节点，分叉出功能分支后又合并回来。

### ✅ 本章验证
- [ ] 已在 main 分支上，包含数据文件
- [ ] `git log --graph` 能看到分叉和合并
- [ ] 功能分支已删除（或保留作为记录）

---

## 第 6 章：模型层开发

> 开新分支 `feature/models`，编写 Pydantic 数据模型。

### 6.1 创建分支并开发

```bash
# 从最新的 main 创建分支
git checkout main
git checkout -b feature/models
```

编写文件：
- `backend/app/models/chat.py`
- `backend/app/models/response.py`

（代码参照 TUTORIAL_PYCHARM.md 第 4.2 节）

### 6.2 验证后提交

```bash
# 验证代码能导入
cd backend
python -c "from app.models.chat import ChatRequest; print('OK')"

# 提交
git add backend/app/models/
git commit -m "feat(models): 添加 Pydantic 数据模型

- chat.py: ChatMessage/ChatRequest/ChatResponse/SessionResponse
- response.py: 科室推荐/医生查询/费用估算的请求与响应模型"
```

### 6.3 合并回 main

```bash
git checkout main
git merge feature/models
git branch -d feature/models
```

### ✅ 本章验证
- [ ] main 分支包含数据模型文件
- [ ] Python 导入测试通过

---

## 第 7 章：API 层开发

> 这是最核心的部分。建议每个 API 一个分支，独立开发和测试。

### 7.1 科室推荐 API

```bash
git checkout -b feature/api-department
```

编写 `backend/app/api/department.py`（代码参照 TUTORIAL_PYCHARM.md 第 4.3.1 节）。

```bash
# 验证
cd backend
python -c "from app.api.department import load_departments; print(f'科室数: {len(load_departments())}')"

# 提交
git add backend/app/api/department.py
git commit -m "feat(api): 实现科室推荐 API

- 症状关键词提取与分词匹配
- 症状→疾病→科室的推荐算法
- 置信度计算与排序"

git checkout main
git merge feature/api-department
git branch -d feature/api-department
```

### 7.2 医生查询 API

```bash
git checkout -b feature/api-doctor
```

编写 `backend/app/api/doctor.py`。

```bash
git add backend/app/api/doctor.py
git commit -m "feat(api): 实现医生查询 API

- 按科室精确/模糊匹配
- 支持排班日期过滤
- 按评分排序"

git checkout main
git merge feature/api-doctor
git branch -d feature/api-doctor
```

### 7.3 费用估算 API

```bash
git checkout -b feature/api-cost
```

编写 `backend/app/api/cost.py`。

```bash
git add backend/app/api/cost.py
git commit -m "feat(api): 实现费用估算 API

- 按科室获取常见检查项目
- 计算总费用与医保报销
- 返回费用明细与医保政策说明"

git checkout main
git merge feature/api-cost
git branch -d feature/api-cost
```

### 7.4 对话管理 API

```bash
git checkout -b feature/api-chat
```

编写 `backend/app/api/chat.py`。

```bash
git add backend/app/api/chat.py
git commit -m "feat(api): 实现对话管理 API

- 会话创建与管理
- 非流式消息发送
- SSE 流式响应（逐字输出）"

git checkout main
git merge feature/api-chat
git branch -d feature/api-chat
```

### ✅ 本章验证

查看提交历史，应该有清晰的 API 开发轨迹：

```bash
git log --oneline --graph
```

```
*   f6g7h8i Merge branch 'feature/api-chat'
|\
| * e5f6g7h feat(api): 实现对话管理 API
|/
*   d4e5f6g Merge branch 'feature/api-cost'
|\
| * c3d4e5f feat(api): 实现费用估算 API
|/
*   b2c3d4e Merge branch 'feature/api-doctor'
...
```

---

## 第 8 章：主入口与首次能运行

> 这是第一个"能运行"的里程碑。

### 8.1 创建 main.py

```bash
git checkout -b feature/main-entry
```

编写 `backend/app/main.py`（代码参照 TUTORIAL_PYCHARM.md 第 4.4 节）。

### 8.2 验证能运行

```bash
cd backend
python -c "from app.main import app; print('所有模块导入成功')"
```

### 8.3 提交并合并

```bash
git add backend/app/main.py
git commit -m "feat: 实现 FastAPI 主入口

- 创建 FastAPI 应用
- 配置 CORS 中间件
- 配置静态文件服务
- 注册 4 个 API 路由"

git checkout main
git merge feature/main-entry
git branch -d feature/main-entry
```

### 8.4 启动测试

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

确认 `http://localhost:8000/docs` 能访问 API 文档。

---

## 第 9 章：前端开发

```bash
git checkout -b feature/frontend
```

按照 TUTORIAL_PYCHARM.md 第 7 章创建前端文件。

### 9.1 分步提交

前端有 6 个文件，可以分两步提交，也可以一次性提交。建议按逻辑分组：

**第一步：HTML + CSS（页面结构与样式）**

```bash
git add frontend/index.html frontend/css/style.css
git commit -m "feat(frontend): 实现页面结构与样式

- index.html: 左右分栏布局（对话区+结果区）
- style.css: Ant Design 风格主题"
```

**第二步：JavaScript（交互逻辑）**

```bash
git add frontend/js/
git commit -m "feat(frontend): 实现前端交互逻辑

- utils.js: DOM 操作工具函数
- api.js: 后端 API 请求封装
- components.js: 科室/医生/费用卡片渲染
- chat.js: 对话流程管理（发送消息→调用API→渲染结果）"
```

### 9.2 合并回 main

```bash
git checkout main
git merge feature/frontend
git branch -d feature/frontend
```

---

## 第 10 章：联调与修复

> 联调阶段经常需要修复问题，每个修复都应该是一个单独的提交。

### 10.1 创建联调分支

```bash
git checkout -b fix/integration
```

### 10.2 复制前端到后端静态目录

```bash
# 复制前端到 backend/static/
cp -r frontend/* backend/static/
```

### 10.3 修复过程中提交

> **原则**：每修一个问题，提交一次。不要攒一堆改动才提交。

```bash
# 修复 API 跨域问题后
git add backend/app/main.py
git commit -m "fix: 配置 CORS 中间件允许前端跨域访问"

# 修复 API 路径后
git add frontend/js/api.js
git commit -m "fix: 修正前端 API 请求路径"

# 修复中文编码问题后
git add backend/app/api/department.py
git commit -m "fix: 修复科室推荐中文匹配问题"
```

### 10.4 合并并标记

```bash
git checkout main
git merge fix/integration
git branch -d fix/integration
```

---

## 第 11 章：打标签 — 标记里程碑版本

> **原则**：当项目到达一个有意义的节点（如"能跑了"、"发布 1.0"），打一个标签标记这个时刻。

### 11.1 打标签

```bash
# 轻量标签（只标记位置）
git tag v1.0.0

# 附注标签（推荐，包含更多信息）
git tag -a v1.0.0 -m "医院智能导诊系统 v1.0.0

功能：
- 症状输入与科室推荐
- 医生排班查询
- 费用与医保估算
- 前端界面完整可用

技术栈：FastAPI + 纯 HTML/JS"
```

### 11.2 查看标签

```bash
# 查看所有标签
git tag

# 查看标签详情
git show v1.0.0
```

### 11.3 推送到远程（如果配置了远程仓库）

```bash
# 推送标签到远程
git push origin v1.0.0

# 推送所有标签
git push origin --tags
```

### 11.4 后续版本

```bash
# 后续迭代时
git tag -a v1.1.0 -m "v1.1.0: 接入 OpenAI API"
git tag -a v2.0.0 -m "v2.0.0: 完整 RAG + ReAct 实现"
```

### ✅ 本章验证
- [ ] `git tag` 能看到 v1.0.0
- [ ] `git show v1.0.0` 能看到标签信息

---

## 第 12 章：PyCharm 中的 Git 图形化操作

> 虽然命令行很强大，但 PyCharm 的 Git 图形界面更直观，日常开发中更方便。

### 12.1 颜色含义

| 文件颜色 | 含义 |
|---------|------|
| **白色** | 已跟踪，无改动 |
| **蓝色** | 已修改，未暂存 |
| **绿色** | 新文件，未跟踪 |
| **灰色** | 被 .gitignore 忽略 |
| **红色** | 已删除 |

### 12.2 常用操作入口

| 操作 | 菜单路径 | 快捷键 |
|------|---------|--------|
| 提交 | `Git → Commit` | `Ctrl+K` |
| 拉取 | `Git → Pull` | `Ctrl+T` |
| 推送 | `Git → Push` | `Ctrl+Shift+K` |
| 添加到暂存区 | 右键文件 → `Git → Add` | `Ctrl+Alt+A` |
| 查看历史 | 底部 Git 窗口 → Log | `Alt+9` |
| 对比差异 | 右键文件 → `Git → Show Diff` | `Ctrl+D` |
| 撤销修改 | 右键文件 → `Git → Rollback` | `Ctrl+Alt+Z` |

### 12.3 查看改动差异

修改文件后，文件名变蓝。在 PyCharm 中查看改了什么：

1. 右键蓝色文件 → **`Git → Show Diff`**
2. 弹出差异对比窗口：

```
┌──────────────────┬──────────────────┐
│  左侧（修改前）    │  右侧（修改后）    │
│                  │                  │
│  def hello():    │  def hello():    │
│ -    print("hi") │ +    print("Hello│
│                  │ +  World!")      │
│                  │                  │
└──────────────────┴──────────────────┘
     红色 = 删除      绿色 = 新增
```

### 12.4 查看文件历史

右键文件 → **`Git → Show History`**，可以看到这个文件的所有修改记录：

```
┌─ History ──────────────────────────────┐
│                                          │
│  ●  f6g7h8i  2026-07-08 17:30          │
│     feat(api): 实现对话管理 API          │
│                                          │
│  ●  c3d4e5f  2026-07-08 16:50          │
│     feat(data): 添加科室数据              │
│                                          │
│  ●  a1b2c3d  2026-07-08 16:30          │
│     chore: 初始化项目结构                │
│                                          │
└──────────────────────────────────────────┘
```

点击任意历史版本，可以对比当前版本和该版本的差异。

### 12.5 暂存修改（Stash）

> 临时切到别的分支修 bug，但当前改动还不想提交？用 Stash 暂存。

1. 菜单 `Git → Uncommitted Changes → Stash Changes...`
2. 输入暂存名称
3. 切到其他分支工作
4. 回来后：`Git → Uncommitted Changes → Unstash Changes...`
5. 选择之前暂存的改动，恢复

### 12.6 配置远程仓库（可选）

如果你想推送到 GitHub/Gitee：

1. 在 GitHub/Gitee 创建空仓库
2. PyCharm 菜单：`Git → Manage Remotes...`
3. 添加远程地址：`https://github.com/你的用户名/hospital-guide.git`
4. 首次推送：`Git → Push`（`Ctrl+Shift+K`）

```bash
# 命令行等价操作
git remote add origin https://github.com/用户名/hospital-guide.git
git push -u origin main
git push origin --tags
```

---

## 附录 A：提交信息规范

### Conventional Commits 格式

```
<类型>(<范围>): <简短描述>

<详细说明（可选）>
```

### 类型 (type)

| 类型 | 含义 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(api): 实现科室推荐 API` |
| `fix` | 修 bug | `fix: 修复 CORS 跨域问题` |
| `docs` | 文档 | `docs: 更新 README` |
| `style` | 代码格式（不影响逻辑） | `style: 格式化代码` |
| `refactor` | 重构 | `refactor: 重构科室推荐逻辑` |
| `test` | 测试 | `test: 添加科室推荐单元测试` |
| `chore` | 构建/配置/依赖 | `chore: 添加 .gitignore` |
| `perf` | 性能优化 | `perf: 优化 JSON 文件加载` |

### 范围 (scope) — 可选

表示改动影响的模块，如 `api`、`frontend`、`data`、`models`。

### 好的提交信息示例

```
feat(api): 实现科室推荐 API

- 症状关键词提取与分词匹配
- 症状→疾病→科室的推荐算法
- 置信度计算与排序

Closes #12
```

### 不好的提交信息

```
update              ← 改了什么？不知道
fix bug             ← 哪个 bug？怎么修的？
asdfasdf            ← 无意义
大改                ← 太笼统
```

---

## 附录 B：Git 常用命令速查

### 基础操作

```bash
git init                          # 初始化仓库
git status                        # 查看状态
git add <文件>                     # 暂存文件
git add .                         # 暂存所有改动
git commit -m "提交信息"           # 提交
git log --oneline --graph         # 查看历史
git diff                          # 查看未暂存的改动
git diff --staged                 # 查看已暂存的改动
```

### 分支操作

```bash
git branch                        # 查看分支
git branch <名称>                  # 创建分支
git checkout <名称>                # 切换分支
git checkout -b <名称>             # 创建并切换
git merge <名称>                   # 合并分支
git branch -d <名称>               # 删除已合并的分支
git branch -D <名称>               # 强制删除分支
```

### 撤销操作

```bash
git checkout -- <文件>             # 撤销工作区修改
git reset HEAD <文件>              # 撤销暂存
git reset --soft HEAD~1           # 撤销上次提交（保留改动）
git revert <commit>                # 创建一个反向提交来撤销
```

### 标签

```bash
git tag                           # 查看标签
git tag v1.0.0                    # 创建轻量标签
git tag -a v1.0.0 -m "说明"        # 创建附注标签
git push origin v1.0.0            # 推送标签到远程
```

### 远程

```bash
git remote add origin <url>       # 添加远程仓库
git push -u origin main          # 首次推送
git push                         # 后续推送
git pull                         # 拉取远程更新
git clone <url>                   # 克隆仓库
```

### 暂存

```bash
git stash                         # 暂存当前改动
git stash list                    # 查看暂存列表
git stash pop                     # 恢复最近的暂存
git stash drop                    # 删除最近的暂存
```

---

## 附录 C：完整提交历史参考

按照本教程操作，最终的提交历史应该类似：

```bash
git log --oneline --graph
```

```
*   h8i9j0k (HEAD -> main, tag: v1.0.0) Merge branch 'fix/integration'
|\
| * g7h8i9j fix: 修复科室推荐中文匹配问题
| * f6g7h8i fix: 修正前端 API 请求路径
| * e5f6g7h fix: 配置 CORS 中间件
|/
*   d4e5f6g Merge branch 'feature/frontend'
|\
| * c3d4e5f feat(frontend): 实现前端交互逻辑
| * b2c3d4e feat(frontend): 实现页面结构与样式
|/
*   a1b2c3d Merge branch 'feature/main-entry'
|\
| * z0y1z2y feat: 实现 FastAPI 主入口
|/
*   y9z0y1z Merge branch 'feature/api-chat'
|\
| * x8y9z0x feat(api): 实现对话管理 API
|/
*   w7y8z9w Merge branch 'feature/api-cost'
|\
| * v6w7x8v feat(api): 实现费用估算 API
|/
*   u5w6x7u Merge branch 'feature/api-doctor'
|\
| * t4v5w6t feat(api): 实现医生查询 API
|/
*   s3u4v5s Merge branch 'feature/api-department'
|\
| * r2s3t4r feat(api): 实现科室推荐 API
|/
*   q1r2s3q Merge branch 'feature/models'
|\
| * p0q1r2p feat(models): 添加 Pydantic 数据模型
|/
*   o9p0q1o Merge branch 'feature/data-layer'
|\
| * n8o9p0n feat(data): 添加科室、医生、症状、费用数据
|/
* m7n8o9m chore: 初始化项目结构与依赖配置
```

> 看到这个清晰的历史树，说明你的版本管理做对了。每一层都是一个功能分支的合并，主线 main 始终干净。

---

> 🎉 **Git 不只是工具，是一种开发纪律。** 养成"小步提交、频繁合并、分支开发"的习惯，你的代码会越来越可控、可追溯、可回退。
>
> 配合 `TUTORIAL_PYCHARM.md` 使用：**搭建代码参照那份，Git 操作参照本文件。**