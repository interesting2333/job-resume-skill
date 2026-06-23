<div align="center">

# job-resume-skill

[中文](README.md) | **English**

_“A resume should not turn you into someone else. It should make your real experience worth interviewing.”_

![Codex](https://img.shields.io/badge/Codex-Skill-111827?labelColor=4b5563)
![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-16a34a?labelColor=4b5563)
![Language](https://img.shields.io/badge/Language-ZH%20%7C%20EN-2563eb?labelColor=4b5563)
![License](https://img.shields.io/badge/License-Not%20declared-f59e0b?labelColor=4b5563)

Need to write a resume from scratch? It helps turn raw experience into a defensible material bank.
Need to tailor a resume to a JD? It helps decide what to move forward, weaken, rewrite, or remove.
Need to turn an engineering project into resume highlights? It extracts evidence from code, notes, and business context.
Need to prepare for interview follow-ups? It turns every bullet into answers that can survive pressure.

**Install this Skill, and AI becomes your resume coach and interview-defense coach.**
**It speaks plainly, stays faithful to real experience, and tests every highlight from the hiring side.**

[Demo](#demo) · [Installation](#installation) · [Skill Structure](#skill-structure) · [Core Capabilities](#core-capabilities) · [Make Your Own](#make-your-own)

</div>

## Demo

Call the skill directly:

```text
Use $job-resume-skill to optimize my resume for this JD.
```

Or describe the task naturally:

```text
Use job-resume-skill to tailor my resume for the JD below and list likely interview follow-up questions.
```

Typical outputs include:

- Resume diagnosis and rewrite suggestions
- JD-tailored resume drafts
- Project experience bullets
- Project scripts, self-introductions, interview Q&A
- One-page resume versions
- HR interview and salary negotiation defense scripts

## Installation

Install this directory as a Codex Skill or place it in your Skill directory, then call it explicitly:

```text
Use $job-resume-skill ...
```

If you are already working inside this repository with Codex, you can also ask naturally:

```text
Use job-resume-skill to review this resume.
```

## Skill Structure

```text
.
├── SKILL.md
├── README.md
├── README.en.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-and-materials.md
│   ├── resume-audit-and-rewrite.md
│   ├── jd-tailoring.md
│   ├── project-keypoints.md
│   ├── interview-defense.md
│   └── ...
└── scripts/
    ├── extract_word_text.py
    └── project_inventory.py
```

## Core Capabilities

- **Create resumes from scratch**: Build a candidate material bank before drafting a resume that can survive follow-up questions.
- **Audit and rewrite resumes**: Check narrative, keywords, project context, measurable results, and authenticity risks.
- **Tailor resumes to JDs**: Extract responsibilities, skills, keywords, hidden evaluation points, and content trade-offs.
- **Extract project highlights**: Turn codebases, project descriptions, or technical notes into business value, technical depth, and personal contribution.
- **Prepare interview defense**: Convert resume highlights into follow-up chains, project scripts, and strong-vs-weak answer comparisons.
- **Handle red flags**: Cover career gaps, frequent job changes, outsourcing experience, toy projects, weak metrics, and authenticity boundaries.
- **Parse Word resumes**: Supports `.docx` and `.docm`, extracting body text, tables, headers, footers, footnotes, endnotes, and comments when available.

## Recommended Inputs

For stronger results, provide:

- Target role or job description
- Current resume text or Word resume
- Project description, code directory, or key technical notes
- Years of experience, direction, level, target city, or target market
- Desired output: full resume, project section, self-introduction, interview Q&A, one-page resume, and so on

## Helper Scripts

Extract text from a Word resume:

```bash
python scripts/extract_word_text.py path/to/resume.docx
```

Inspect a project directory:

```bash
python scripts/project_inventory.py path/to/project
```

## Make Your Own

This Skill can be used as a pattern for other career-coaching skills:

1. Define boundaries first: what it helps with, and what it must not invent.
2. Split complex tasks into focused guides under `references/`.
3. Add scripts for repetitive work, such as parsing files, inspecting projects, or extracting source material.
4. Keep `SKILL.md` clear about trigger scenarios, workflow, and output structure.

## License

No license has been declared. Confirm authorization requirements with the repository owner before using, distributing, or modifying this project.
