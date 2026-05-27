# Job Resume Skill

An OpenCode skill for resume writing, resume review, JD-based tailoring, project highlight extraction, and interview preparation.

This skill helps job seekers turn real experience into a stronger, more defensible resume. It does not fabricate achievements, metrics, titles, project scale, or responsibilities.

## Overview

`job-resume-skill` acts as a resume coach and interview-defense coach. It can create a resume from scratch, improve an existing resume, tailor materials for a target job description, extract resume-worthy project points from code or project notes, and prepare answers for likely interview follow-up questions.

## Use Cases

Use this skill when you need to:

- Write a resume from scratch.
- Review and rewrite an existing resume.
- Tailor a resume to a specific JD.
- Extract project highlights from a codebase, project description, or technical notes.
- Convert project experience into resume bullets.
- Prepare project scripts, self-introductions, interview Q&A, and follow-up defenses.
- Build a one-page resume.
- Handle resume red flags such as career gaps, frequent job changes, outsourcing experience, toy projects, weak metrics, or authenticity risks.
- Parse Word resumes in `.docx` or `.docm` format.

## How To Use

Call the skill directly in OpenCode:

```text
Use $job-resume-skill to optimize my resume for this JD.
```

You can also describe the task naturally:

```text
Use job-resume-skill to tailor my resume for the JD below and list likely interview follow-up questions.
```

Chinese requests are supported:

```text
使用 job-resume-skill，帮我根据下面 JD 优化简历，并列出面试官可能追问的问题。
```

## Recommended Inputs

For better results, provide any of the following:

- Target role or job description.
- Current resume text or Word resume.
- Project description, code directory, or key technical notes.
- Candidate background, years of experience, career direction, target city, or target market.
- Desired output, such as a full resume, project experience section, self-introduction, interview Q&A, or one-page resume.

## Core Principles

- Do not invent experience, metrics, titles, project scale, or responsibility boundaries.
- Mark missing facts with `[待补充：...]` or ask focused follow-up questions.
- Prefer resume bullets built around action, deliverable, and result.
- Always include project context: what the system does, who it serves, and what problem it solves.
- Prepare for real interview pressure: implementation details, trade-offs, evidence of impact, and personal contribution.

## Image Input Limitation

ERROR: Cannot read "image.png" (this model does not support image input). Please provide the image content as text, or describe the target format in words.

## Helper Scripts

### Extract Text From Word Resumes

```bash
python scripts/extract_word_text.py path/to/resume.docx
```

Supports `.docx` and `.docm`. The script attempts to extract text from body content, tables, headers, footers, footnotes, endnotes, and comments.

### Inspect A Project Directory

```bash
python scripts/project_inventory.py path/to/project
```

Use this before analyzing a codebase for resume-worthy project highlights. It summarizes languages, directory structure, important files, and suggested reading entry points.

## Directory Structure

```text
.
├── SKILL.md
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

## References

The `references/` directory contains task-specific guides for intake, resume audit, JD tailoring, project highlight extraction, interview defense, red-flag handling, job taxonomy, metric selection, recruiter review, and market localization.

## License

No license has been declared. Confirm authorization requirements with the repository owner before using, distributing, or modifying this project.
