# job-resume-skill 设计文档

## 设计目标

`job-resume-skill` 是一个面向求职材料生成、简历优化和面试防守的 Codex Skill。它的核心目标不是替用户包装经历，而是把真实经历整理成更容易获得面试、且经得起追问的表达。

设计上优先满足四个要求：

- **真实性**：不编造经历、指标、头衔、项目规模或职责边界，缺失事实使用占位符或追问补齐。
- **岗位导向**：所有简历表达都围绕目标岗位、JD、职级和招聘方筛选逻辑做取舍。
- **可追问**：简历 bullet、项目亮点和自我介绍都要能回答“怎么做、为什么这么做、结果如何证明、个人贡献是什么”。
- **渐进加载**：主入口只放路由和原则，细分方法沉淀到 `references/`，重复性解析工作交给 `scripts/`。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.en.md
├── DESIGN.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-and-materials.md
│   ├── resume-audit-and-rewrite.md
│   ├── jd-tailoring.md
│   ├── jd-scorecard.md
│   ├── project-keypoints.md
│   ├── interview-defense.md
│   ├── interview-rubrics.md
│   ├── red-flags-and-ethics.md
│   ├── recruiter-lens.md
│   ├── metrics-library.md
│   ├── occupation-taxonomy.md
│   ├── one-page-resume.md
│   ├── market-localization.md
│   ├── knowledge-sources.md
│   └── word-parsing.md
└── scripts/
    ├── extract_word_text.py
    └── project_inventory.py
```

## 分层设计

### 1. 触发层：`SKILL.md`

`SKILL.md` 是 Skill 的主入口，承担三件事：

- 通过 YAML frontmatter 的 `name` 和 `description` 描述能力边界与触发场景。
- 定义通用原则，例如忠于事实、先判断目标、优先写“动作 + 产物 + 结果”。
- 根据用户意图路由到对应参考文件和脚本。

它不承载完整知识库，避免每次触发都加载过多上下文。新增能力时，优先新增或扩展 `references/` 文件，再在 `SKILL.md` 的“判断任务类型”和“参考文件”中补路由。

### 2. 知识层：`references/`

`references/` 按任务拆分为多个小指南。每个文件只服务一类高频工作流：

- `intake-and-materials.md`：从零创建简历时的素材收集、追问和候选人材料库。
- `resume-audit-and-rewrite.md`：简历审计、问题定位、成果化改写和占位符规则。
- `jd-tailoring.md`：JD 拆解、内容排序、裁剪和关键词处理。
- `jd-scorecard.md`：把 JD 要求转成能力维度、证据链和匹配等级。
- `project-keypoints.md`：从工程目录、项目描述或简历段落中提炼项目定位、技术亮点、业务价值和面试追问。
- `interview-defense.md`：项目讲稿、追问链、好答案/差答案、HR 面和薪资谈判。
- `interview-rubrics.md`：结构化面试评分、STAR/BEI 检查和追问标准。
- `red-flags-and-ethics.md`：空窗、跳槽、外包、玩具项目、夸大风险和真实性边界。
- `recruiter-lens.md`：从 HR、技术面试官和 ATS 角度做压力测试。
- `metrics-library.md`：按岗位类型提供可量化结果口径。
- `occupation-taxonomy.md`：岗位画像、职级判断、能力模型和叙事重心。
- `one-page-resume.md`：一页版简历压缩和取舍。
- `market-localization.md`：国内外简历差异、中英文表达和目标市场本地化。
- `knowledge-sources.md`：岗位标准、薪资、市场趋势等外部信息源路由。
- `word-parsing.md`：Word 简历解析范围、降级策略和解析后检查。

这种拆分让 Codex 可以根据任务只读取必要上下文。例如，用户只要求“根据 JD 改简历”时，优先读 `jd-tailoring.md`，需要评分才追加 `jd-scorecard.md`，不必加载面试、Word 解析或市场本地化内容。

### 3. 工具层：`scripts/`

脚本用于处理重复、确定性强、容易出错的输入准备工作。

#### `scripts/extract_word_text.py`

职责：

- 解析 `.docx` 和 `.docm` 这类 Word Open XML 文件。
- 使用 Python 标准库读取 zip 包和 XML，不依赖 `python-docx`。
- 提取正文、表格行、页眉页脚、脚注、尾注和批注文本。
- 输出 Markdown 风格文本，供后续审计、改写和面试准备使用。

关键边界：

- 不执行 `.docm` 宏。
- 不直接解析旧版二进制 `.doc`。
- 当文档为空、受保护、图片化或损坏时返回失败，而不是假装已经读取成功。

#### `scripts/project_inventory.py`

职责：

- 快速盘点一个工程目录，生成面向简历分析的项目摘要。
- 忽略 `.git`、`node_modules`、`target`、`build`、虚拟环境等高噪音目录。
- 统计语言、文件扩展名、顶层目录和重要工程文件。
- 给出建议优先阅读的 README、构建文件、依赖清单、CI 配置等。

关键边界：

- 它只做目录级盘点，不做业务结论。
- 它不会读取完整工程源码，也不会推断项目规模。
- 后续项目亮点仍需要结合关键文件、用户说明和目标岗位确认。

### 4. 展示层：`agents/openai.yaml`

`agents/openai.yaml` 提供 UI 元数据：

- `display_name`：展示名称。
- `short_description`：短描述。
- `default_prompt`：默认示例提示词。

它不影响核心执行逻辑，但需要和 `SKILL.md` 的能力描述保持一致。若大幅调整 Skill 能力范围，应同步检查该文件是否仍准确。

## 核心工作流

### 从零创建简历

1. 读取 `intake-and-materials.md`。
2. 先建立候选人素材库，包括基础档案、目标岗位、工作经历、项目素材和成果证据。
3. 对缺失事实进行高质量追问。
4. 生成简历草稿，并标出待补事实。

### 解析并优化 Word 简历

1. 读取 `word-parsing.md`。
2. 对 `.docx` 或 `.docm` 运行 `scripts/extract_word_text.py`。
3. 检查解析结果是否包含关键模块、是否乱码、时间线是否完整。
4. 根据任务进入审计、JD 定制或面试防守流程。

### 审计和重写简历

1. 读取 `resume-audit-and-rewrite.md`。
2. 做 30 秒初判：继续看点、最大扣分点、最大可放大亮点。
3. 检查职业故事线、JD 关键词、项目上下文、bullet 质量和量化结果。
4. 用“问题/目标 + 动作 + 产物 + 结果”改写。
5. 对缺少事实的位置保留 `[待补充：...]`。

### 根据 JD 定制

1. 读取 `jd-tailoring.md`。
2. 把 JD 拆成职责、必要技能、加分项、业务背景、隐藏考察点和关键词。
3. 需要匹配度评分时读取 `jd-scorecard.md`。
4. 决定内容前置、压缩、删除或补充。
5. 输出定制版内容和面试追问预警。

### 从工程项目提炼简历亮点

1. 读取 `project-keypoints.md`。
2. 如果输入是工程目录，先运行 `scripts/project_inventory.py`。
3. 优先读取 README、构建文件、接口/架构/配置/测试等关键文件。
4. 区分已明确事实、合理推断和待补信息。
5. 输出项目定位、核心价值、技术栈与架构、项目亮点、简历 bullet 和追问点。

### 面试对抗和讲稿

1. 读取 `interview-defense.md`。
2. 把简历中的强项转成追问链。
3. 对风险点生成 HR、技术和项目追问。
4. 需要评分或模拟面试点评时读取 `interview-rubrics.md`。
5. 输出项目讲稿、可直接说出口的回答版本和补证据清单。

## 数据和控制流

```text
用户输入
  |
  v
识别任务类型
  |
  +--> 需要文件解析? --> scripts/extract_word_text.py
  |
  +--> 需要工程盘点? --> scripts/project_inventory.py
  |
  v
按需读取 references/*
  |
  v
建立目标上下文和证据链
  |
  v
生成策略、改写稿、项目亮点或面试防守材料
  |
  v
标注待补事实和下一步行动
```

所有输出都应围绕证据链组织：

```text
能力关键词 -> 项目场景 -> 个人动作 -> 产物 -> 结果/影响 -> 可防守证据
```

## 设计边界

### 必须坚持

- 不编造经历和指标。
- 不把团队成果全部写成个人主导。
- 不为了 ATS 堆砌无证据关键词。
- 不只凭文件名、目录名或依赖列表判断项目含金量。
- 不在用户只要求局部优化时强行重写整份简历。

### 可以合理推断，但必须标注

- 从工程目录推断技术栈。
- 从 README 或配置推断部署方式。
- 从 JD 措辞推断隐藏考察点。
- 从项目描述推断可能追问方向。

### 应该追问或占位

- 候选人真实职责边界。
- 量化结果和验证口径。
- 项目规模、用户范围和业务价值。
- 上线情况、事故复盘、团队协作方式。
- 目标岗位、目标市场和投递策略。

## 扩展规范

新增能力时按以下顺序处理：

1. 判断是否属于已有参考文件的自然延伸。
2. 如果是，扩展对应 `references/*.md`。
3. 如果是新的任务类型，新增一个聚焦的 reference 文件。
4. 在 `SKILL.md` 的“判断任务类型”和“参考文件”中加入路由。
5. 如果新增重复性、确定性强的处理逻辑，放入 `scripts/`。
6. 如果能力范围或默认用法变化，检查 `agents/openai.yaml` 和 README 是否需要同步。

新增脚本时应满足：

- 优先使用标准库或仓库已接受的轻量依赖。
- 输出应适合直接进入后续简历分析流程。
- 错误要显式返回，不要静默失败。
- 不读取或暴露不必要的敏感信息。

新增 reference 文件时应满足：

- 文件只解决一个明确任务。
- 给出输入类型、分析顺序、输出格式和禁忌。
- 能被 `SKILL.md` 明确路由到。
- 避免和其他 reference 大段重复。

## 维护检查清单

- `SKILL.md` 是否仍保持主入口职责，而不是变成大知识库。
- 每个 `references/*.md` 是否有清晰目标和输出格式。
- 两个脚本的错误提示是否和 `references/word-parsing.md`、`project-keypoints.md` 保持一致。
- README 中的核心能力是否和 `SKILL.md` 的触发描述一致。
- `agents/openai.yaml` 的短描述和默认提示是否仍能代表当前能力。
- 所有改写规则是否继续坚持真实性边界。
