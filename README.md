<div align="center">

# job-resume-skill

**中文** | [English](README.en.md)

_“简历不是把你包装成另一个人，而是把真实经历讲到值得被面试。”_

![Codex](https://img.shields.io/badge/Codex-Skill-111827?labelColor=4b5563)
![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-16a34a?labelColor=4b5563)
![Language](https://img.shields.io/badge/Language-ZH%20%7C%20EN-2563eb?labelColor=4b5563)
![License](https://img.shields.io/badge/License-Not%20declared-f59e0b?labelColor=4b5563)

面向求职者的简历创建、简历审计、JD 定制、项目亮点提炼和面试对抗 Skill。

它把零散经历整理成可信材料库，把工程项目提炼成可写进简历的证据链，把每个亮点都放到真实面试追问里检验。

**真实经历优先，岗位视角取舍，证据链支撑表达。**

[快速开始](#快速开始) · [核心能力](#核心能力) · [工作方式](#工作方式) · [Skill 结构](#skill-结构) · [设计文档](DESIGN.md)

</div>

## 快速开始

根据 JD 优化简历：

```text
Use $job-resume-skill to optimize my resume for this JD.
```

审计中文简历并给改写建议：

```text
使用 job-resume-skill，帮我诊断这份简历最影响面试机会的问题，并给出修改后版本。
```

从工程项目提炼简历亮点：

```text
使用 job-resume-skill，分析这个工程目录，提炼项目定位、技术亮点、简历 bullet 和面试追问。
```

准备面试防守：

```text
使用 job-resume-skill，把这段项目经历转成项目讲稿，并列出面试官可能追问的问题和好答案。
```

## 适合什么场景

- 从零创建简历：先问清经历、项目、成果和目标岗位，再生成简历草稿。
- 优化现有简历：审计故事线、关键词、项目上下文、量化结果和真实性风险。
- 根据 JD 定制：拆解职责、技能、关键词、隐藏考察点，决定前置、压缩、删除或补充什么。
- 提炼项目亮点：从代码目录、README、技术笔记或项目描述中提炼业务价值、技术深度和个人贡献。
- 准备面试追问：把简历 bullet 转成追问链、项目讲稿、好答案/差答案和补证据清单。
- 处理红旗问题：覆盖空窗期、跳槽、外包、玩具项目、弱指标、薪资谈判和真实性边界。
- 解析 Word 简历：支持 `.docx` 和 `.docm`，尽力提取正文、表格、页眉页脚、脚注尾注和批注文本。

## 核心能力

| 能力 | 解决的问题 | 典型产出 |
| --- | --- | --- |
| 简历素材收集 | 没有现成简历或经历很散 | 候选人素材库、追问清单、简历草稿 |
| 简历审计与改写 | 简历写得泛、弱、没有上下文 | 诊断结论、修改策略、改写版本 |
| JD 定制 | 不知道该突出什么、删掉什么 | JD 拆解、匹配度判断、定制版简历 |
| 项目关键点总结 | 项目会做但不会写 | 项目定位、技术亮点、简历 bullet |
| 面试对抗 | 简历亮点经不起追问 | 项目讲稿、追问链、回答模板 |
| 招聘方视角压力测试 | 不确定 HR/面试官怎么看 | 筛选风险、ATS 关键词问题、优化动作 |
| 指标和结果补强 | 结果没有量化或口径模糊 | 指标候选、降级表达、待补数据 |
| 市场本地化 | 国内外简历格式和表达不同 | 中文/英文/海外投递调整建议 |

## 工作方式

这个 Skill 的默认判断逻辑是：

```text
目标岗位/JD
  -> 候选人真实经历
  -> 项目场景和个人动作
  -> 交付产物和结果证据
  -> 简历表达和面试防守
```

它不会先追求“写得漂亮”，而是先判断一段经历是否能形成证据链：

```text
能力关键词 -> 项目场景 -> 个人动作 -> 产物 -> 结果/影响 -> 可防守证据
```

如果事实不足，它会标注 `[待补充：...]` 或提出具体追问；如果只是合理推断，它会明确说明是推断，不会把推断写成事实。

## 推荐输入

为了得到更稳的结果，尽量提供：

- 目标岗位或 JD。
- 当前简历文本，或 `.docx` / `.docm` Word 简历。
- 项目描述、代码目录、README、架构文档或关键技术笔记。
- 年限、方向、职级、目标城市、目标市场或目标公司类型。
- 期望产出：整份简历、项目经历、自我介绍、面试 Q&A、一页版简历等。

## Skill 结构

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

- `SKILL.md`：Skill 主入口，负责触发描述、原则、任务路由和默认工作流。
- `references/`：按任务拆分的参考指南，按需读取，避免一次加载全部上下文。
- `scripts/`：处理重复、确定性强的输入准备工作，例如 Word 文本抽取和工程目录盘点。
- `agents/openai.yaml`：Codex UI 展示用元数据。
- `DESIGN.md`：维护者视角的分层设计、工作流、边界和扩展规范。

## 辅助脚本

提取 Word 简历文本：

```bash
python scripts/extract_word_text.py path/to/resume.docx
```

支持 `.docx` 和 `.docm`。脚本会尽力提取正文、表格、页眉页脚、脚注、尾注和批注文本；不会执行宏，也不会直接解析旧版二进制 `.doc`。

盘点工程目录：

```bash
python scripts/project_inventory.py path/to/project
```

用于分析代码项目之前的第一步。它会统计语言、目录、重要文件和建议阅读入口，但不会替代后续的业务理解和项目亮点判断。

## 不做什么

- 不编造经历、指标、头衔、项目规模或职责边界。
- 不把团队成果全部写成个人主导。
- 不为了 ATS 堆砌没有项目证据支撑的关键词。
- 不只凭目录名、依赖列表或文件名判断项目含金量。
- 不在用户只需要局部优化时强行重写整份简历。
- 不声称完整读取旧版 `.doc`，除非确实获得了可读文本。

## 设计文档

更完整的维护者说明见 [DESIGN.md](DESIGN.md)，其中包含：

- 分层设计：触发层、知识层、工具层、展示层。
- 核心工作流：从零创建、Word 解析、简历审计、JD 定制、项目提炼、面试对抗。
- 数据和控制流。
- 真实性边界和扩展规范。

## 制作你自己的

这个 Skill 的写法可以复用到其他职业教练型能力：

1. 先定义边界：它能帮什么、不能编什么。
2. 把复杂任务拆成 `references/` 里的小指南。
3. 为重复工作提供脚本，比如解析文件、盘点项目、抽取素材。
4. 在 `SKILL.md` 里写清触发场景、工作流和输出结构。

## License

No license has been declared. Confirm authorization requirements with the repository owner before using, distributing, or modifying this project.
