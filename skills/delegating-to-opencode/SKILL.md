---
name: delegating-to-opencode
description: Use when delegating a bounded, self-contained coding task to the local `opencode` CLI agent instead of implementing it inline or spawning a Claude subagent — e.g. a written plan/spec prescribes exact file edits, or the user asks to hand a task to opencode.
---

# Delegating to opencode

## Overview

`opencode` is a separate headless coding-agent CLI on this machine. Each invocation is a fresh process with **zero memory of this conversation** — you own all scoping and verification. Core principle: delegate only what you can cheaply verify against source afterward, and trust nothing it self-reports — verify against the tree, not its summary.

## When to Use

- **opencode**: task is bounded, self-contained, spec-driven (a plan file prescribes exact edits), and cheaply verifiable (diffable against a spec, or grep/build/test checkable).
- **Do it yourself**: task needs live context from this conversation, or verifying the result costs as much as doing it.
- **Claude subagent**: task needs your own tools/MCP servers, or is open-ended research/synthesis rather than a bounded edit.

## Quick Reference

| Intent | Command |
|---|---|
| Read/preview (framework-enforced read-only) | `opencode run --agent plan --model <provider>/<model> --dir <ABS repo path> "<task>"` |
| Write | `opencode run --agent build --model <provider>/<model> --dir <ABS repo path> "<task>"` — **only inside an isolated branch or `git worktree`, never on `main`/`dev` directly** |

`--agent plan` is the real read-only guard (it refuses writes outright). The default `build` agent allows arbitrary shell and file writes with **no prompt**, in or out of `--auto`. Never pass `--auto` — it does not add safety, it only auto-approves the *outside-`--dir`* escape-hatch prompts, widening blast radius instead of narrowing it.

## Recipe

1. **Ask the user which model to use.** Run `opencode models` to list available free hosted
   `opencode/*` Zen models. Recommend one as the default — cheap, and model quality isn't
   safety-load-bearing here (see Model Notes) — but let the user pick. There's no configured
   default on this machine, so don't omit `--model` and let opencode fall back silently.
2. **Isolate first.** Create a dedicated branch or `git worktree` for the write. Never point `--dir`/cwd at `main`/`dev` for a `build` invocation.
3. **Write a self-contained prompt.** Since opencode has no memory of this conversation, always include: absolute repo path, the exact file(s) in scope, the exact spec/plan path+section to follow, explicit read-vs-write intent, and an explicit "do not `git commit`/`git push`/touch anything outside these files" clause.
4. **Run it** using the Quick Reference form that matches your intent, with the model chosen in step 1.
5. **Verify independently before trusting or committing anything** — same discipline as reviewing any human-written handoff doc:
   - `git status`/`git diff` — touched *only* the in-scope files?
   - Literal `diff` of the result against the spec's prescribed code, if one exists.
   - Real build/lint/test run, using this repo's actual commands.
   - Grep-based structural proofs where applicable (e.g. "0 hits" for a deleted symbol).
   - Only after all of this passes: `git add`/commit yourself. Never push without separate explicit approval.

## Common Mistakes

- Trusting opencode's textual summary of what it did instead of independently checking the tree — it can be wrong or stale.
- Reaching for `--auto` "to be safe" — it widens scope, it doesn't narrow it.
- Running `--agent build` directly on the working branch instead of an isolated branch/worktree — `build` can commit/push/delete with no prompt.
- Omitting required context in the prompt because "it's obvious" — opencode never saw this conversation.
- Skipping the model question and letting `opencode` fall back to its internal default — there's no configured default model on this machine, so omitting `--model` is unpredictable, not "safe."

## Model Notes

This skill asks the user which model to use up front (Recipe step 1) — never silently default. Free `opencode/*` Zen models (e.g. `opencode/deepseek-v4-flash-free`) suit cheap bounded work and are the recommended default; model quality isn't safety-load-bearing — verification is independent of it, so a weaker model only costs a wasted verification pass, not a bad merge. `opencode models` lists what's actually available (varies by machine).
