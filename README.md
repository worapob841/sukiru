# sukiru

A personal catalog of [Claude Code](https://claude.ai/code) **skills** — install any of them with the [`skills`](https://github.com/vercel-labs/skills) CLI. One skill today, more added over time.

## Skills

| Skill | What it does |
|---|---|
| [`autoresearch`](./skills/autoresearch) | Autonomous hypothesis-test-eval loop based on Karpathy's autoresearch concept — auto-probes system hardware, asks 3 onboarding questions (task/goal, tracking strategy, env runner), and loops non-stop with auto-commit/revert and progress plots (`autoresearch_progress.png`). |
| [`delegating-to-opencode`](./skills/delegating-to-opencode) | Delegates bounded, self-contained coding tasks to the local `opencode` CLI agent with strict model prompting, isolation, and independent verification rules. |
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
npx skills add worapob841/sukiru --skill autoresearch          # install autoresearch skill
npx skills add worapob841/sukiru --skill delegating-to-opencode # install delegating-to-opencode skill
npx skills add worapob841/sukiru --skill zumen                # install zumen skill
npx skills add worapob841/sukiru -a claude-code -y            # non-interactive, target Claude Code
```

The CLI auto-detects which agents you have installed (pass `-a claude-code`, repeatable, to pin specific ones). Scope is project-local by default; `-g` installs to your user config.

**Manual (git):**

```bash
git clone git@github.com:worapob841/sukiru.git
cp -r sukiru/skills/autoresearch ~/.claude/skills/autoresearch   # copy autoresearch skill
cp -r sukiru/skills/delegating-to-opencode ~/.claude/skills/delegating-to-opencode # copy delegating-to-opencode skill
cp -r sukiru/skills/zumen ~/.claude/skills/zumen                 # copy zumen skill
```

Reload Claude Code afterward so it discovers the skill(s).

## The skills

### autoresearch

`autoresearch` is an autonomous experiment and optimization loop based on Andrej Karpathy's `autoresearch` concept, generalized for AI engineering, machine learning development, LLM fine-tuning, prompt tuning, architecture exploration, hyperparameter search, and code optimization.

The core principle: **Formulate hypothesis → Apply surgical edit → Run in environment → Evaluate metric → Keep if improved (commit/log), revert if degraded → Repeat autonomously non-stop until reaching target goal.**

Key capabilities:
- **Hardware & System Auto-Discovery**: Silently auto-probes GPU acceleration (NVIDIA CUDA, AMD ROCm, Apple Silicon MPS) and CPU/OS specs.
- **3 Onboarding Questions**:
  1. *Task & Goal*: Problem statement, target metric, lower/higher direction, and user solution ideas/POVs.
  2. *Experiment Tracking*: Choice of Git auto-commit/revert, Markdown log (`experiment_log.md`), or hybrid.
  3. *Environment*: Env manager (`conda`, `uv`, `venv`, `poetry`, `pixi`) and run command.
- **Non-Stop Autonomous Execution**: Runs experiments, evaluates metrics, auto-commits gains, auto-reverts regressions, and continues without manual intervention between iterations.
- **Progress Graph Visualizer (`scripts/plot_progress.py`)**: Renders Karpathy-style progress charts (`autoresearch_progress.png`) showing discarded grey dots, kept green dots, running best step-line, and angled hypothesis annotations. Supports both on-demand mid-run plot rendering and final summary plot generation.

### delegating-to-opencode

`delegating-to-opencode` guides when and how to delegate bounded, self-contained coding tasks to the local `opencode` CLI agent.

Key capabilities:
- **Scope & Model Selection**: Prompts user for preferred free `opencode/*` model.
- **Strict Read vs Write Guards**: Enforces `--agent plan` for read-only preview and `--agent build` only inside isolated git branches or `git worktrees`.
- **Independent Verification**: Requires verifying diffs and running builds/tests independently before trusting or committing opencode changes.

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
  autoresearch/                 # the autoresearch skill
    SKILL.md                    # onboarding + autonomous loop workflow
    scripts/
      plot_progress.py          # progress graph visualizer (matplotlib)
  delegating-to-opencode/       # the delegating-to-opencode skill
    SKILL.md                    # opencode CLI delegation rules & verification
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
