# skills

Agent Skills for Claude Code and other agents that support the `SKILL.md` format.

## Skills

| Skill | What it does |
|---|---|
| [`article-to-russian-epub`](article-to-russian-epub/SKILL.md) | Translates an article from any language into literary Russian and builds an EPUB: preparation, draft and final translation, independent review, build. |

## Installation

Copy the skill folder into `~/.claude/skills/` (for all projects) or into a project's `.claude/skills/`:

```sh
git clone https://github.com/marvell/skills.git
cp -r skills/article-to-russian-epub ~/.claude/skills/
```

## Requirements

`article-to-russian-epub`: pandoc 3+, python3, curl, and internet access.

## License

[MIT](LICENSE)
