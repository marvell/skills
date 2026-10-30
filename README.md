# skills

Навыки (Agent Skills) для Claude Code и других агентов, поддерживающих формат `SKILL.md`.

## Навыки

| Навык | Что делает |
|---|---|
| [`article-to-russian-epub`](article-to-russian-epub/SKILL.md) | Переводит статью на любом языке в литературный русский и собирает EPUB: подготовка, черновой и чистовой перевод, независимая проверка, сборка. |

## Установка

Скопировать папку навыка в `~/.claude/skills/` (для всех проектов) или в `.claude/skills/` проекта:

```sh
git clone https://github.com/marvell/skills.git
cp -r skills/article-to-russian-epub ~/.claude/skills/
```

## Зависимости

`article-to-russian-epub`: pandoc 3+, python3, curl и доступ в интернет.

## Лицензия

[MIT](LICENSE)
