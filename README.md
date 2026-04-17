# atom-design

Design repo for **Atom Grants** marketing and company materials — decks, one-pagers, posters, mockups, animations. Everything is assembled as **self-contained HTML** and rendered to PNG/PDF when needed.

This repo holds the shared setup only: brand system (`CLAUDE.md`), logo assets (`assets/`), and the Claude Code skill that renders HTML to PNG (`.claude/skills/html-screenshot/`). Your actual project folders live locally and are gitignored by default.

## Prerequisites

- **[Claude Code](https://claude.com/claude-code)** — the CLI that picks up `CLAUDE.md` and the skills in `.claude/`
- **Python 3** with Playwright (for rendering HTML → PNG)

Install Playwright once per machine:

```bash
pip3 install playwright
python3 -m playwright install chromium
```

## Setup

```bash
git clone https://github.com/tomerds/atom-design.git
cd atom-design
claude
```

That's it. When Claude Code starts in this directory it automatically loads:
- `CLAUDE.md` — brand colors, fonts, layout conventions, folder structure
- `.claude/settings.json` — permission to run `python3` (for the screenshot skill)
- `.claude/skills/html-screenshot/` — the render-to-PNG skill

## Your first deliverable

Ask Claude to make something. It will create a new folder and an HTML file following the brand system in `CLAUDE.md`. For example:

> Make a one-pager announcing our new research grants program.

Claude will produce something like `Research_Grants_Onepager/Research_Grants_Onepager.html`.

Open the HTML file in a browser to preview it, then render it to PNG:

```bash
python3 .claude/skills/html-screenshot/shoot.py Research_Grants_Onepager/Research_Grants_Onepager.html
```

Or just ask Claude to "render it" / "screenshot it" — the `html-screenshot` skill will handle it.

Default output is a 2× retina PNG next to the HTML file (e.g. `Research_Grants_Onepager@2x.png`). See `.claude/skills/html-screenshot/SKILL.md` for flags (`--scale`, `--selector`, `--full-page`, etc.).

## Repo layout

```
atom-design/
├── assets/                  # shared brand assets (logos, wordmarks)
├── .claude/
│   ├── settings.json        # shared permissions
│   └── skills/
│       └── html-screenshot/ # HTML → PNG renderer
├── CLAUDE.md                # brand system + working conventions
├── .gitignore
└── README.md
```

Your local projects show up as sibling folders (`MSU_Poster_2026/`, `LinkedIn-Collaborator-Discovery/`, etc.) and stay out of git by default.

## Sharing a deliverable

To commit a specific project folder, add an allowlist entry to `.gitignore`:

```gitignore
!/MSU_Poster_2026/
```

Rendered `@2x.png` exports can be regenerated from the HTML, so there's usually no need to commit them.
