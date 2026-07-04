# sukiru

A personal catalog of [Claude Code](https://claude.ai/code) **skills** — install any of them with the [`skills`](https://github.com/vercel-labs/skills) CLI. One skill today, more added over time.

## Skills

| Skill | What it does |
|---|---|
| [`zumen`](./skills/zumen) | Turns a fuzzy idea into a phased, well-architected plan — interviews you one question at a time, compares 2–3 architecture approaches, breaks the work into phases, writes a cross-linked `plans/` doc bundle, and **stops before any implementation**. |

_More skills coming._

## Install

Use the [`skills`](https://github.com/vercel-labs/skills) CLI — it discovers every skill under `skills/` and links it into your agent's config:

```bash
# preview what's in the catalog
npx skills add worapob841/sukiru --list

# add every skill to the current project → .claude/skills/
npx skills add worapob841/sukiru

# or install globally for every project → ~/.claude/skills/
npx skills add worapob841/sukiru -g
```

Handy variants:

```bash
npx skills add worapob841/sukiru --skill zumen         # install just one skill by name
npx skills add worapob841/sukiru -a claude-code -y     # non-interactive, target Claude Code
```

The CLI auto-detects which agents you have installed (pass `-a claude-code`, repeatable, to pin specific ones). Scope is project-local by default; `-g` installs to your user config.

**Manual (git):**

```bash
git clone git@github.com:worapob841/sukiru.git
cp -r sukiru/skills/zumen ~/.claude/skills/zumen   # copy whichever skill(s) you want
```

Reload Claude Code afterward so it discovers the skill(s).

## The skills

### zumen

`zumen` (図面, Japanese for *plan / technical drawing*) turns a fuzzy idea into a crystal-clear, well-architected, phased plan — then writes it out as a `plans/` documentation bundle and **stops before any implementation**.

It interviews you one question at a time to lock requirements, proposes and compares 2–3 architecture approaches with a recommendation, breaks the work into phases with S/M/L complexity ratings, and emits four cross-linked docs:

| Doc | Holds |
|---|---|
| `plans/product.md` | WHO / WHY / WHAT — users, scope, non-goals, success criteria |
| `plans/architecture.md` | HOW — tech-stack table, components, domain model, APIs / auth / storage |
| `plans/task.md` | WHEN — phases with goal / deliverables / dependencies + S/M/L subtasks |
| `plans/decisions/YYYY-MM-DD-<topic>.md` | The interview itself — every recommended question + chosen option + why |

It detects and reuses an existing codebase's stack before asking, works greenfield too, and **extends** an existing `plans/` folder instead of overwriting it.

**Use it** by invoking `/zumen`, or just describe what you want to build — it triggers on *"plan / spec / scope this project"*, *"design the architecture / pick a stack"*, *"break this into phases"*, or *"interview / grill me about requirements"*.

zumen runs a six-stage flow — detect terrain → requirements interview → architecture proposal → phasing → write the bundle → **hard stop** — pausing for your approval at each gate. It plans; it never writes code. Handing off to implementation is a separate, fresh invocation.

## Repository layout

```
skills/
  zumen/                        # the zumen skill
    SKILL.md                    # triggers + the 6-stage flow
    references/
      interview-checklist.md    # the requirements decision tree the grill walks
    templates/                  # output doc shapes — copied, then filled
      product.md  architecture.md  task.md
      decision-record.md  interview-scratchpad.md
  ...                           # more skills go here
CLAUDE.md                       # guidance for *developing* this catalog (not shipped in installs)
```

Each skill is a self-contained folder under `skills/`; the `skills` CLI discovers them all.

## Developing

See [`CLAUDE.md`](./CLAUDE.md) for a skill's architecture, the invariants any edit must preserve, and the cross-file coupling to keep in sync.
