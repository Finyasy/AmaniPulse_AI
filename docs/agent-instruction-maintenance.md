# Agent Instruction Maintenance

## Rule

When working with agent instruction files, optimize for compliance over completeness.

Keep `AGENTS.md` concise, current, and operational. It should focus on:

- Required commands.
- Important paths.
- Hard rules.
- Current architecture conventions.
- Known pitfalls and gotchas.
- Short links to deeper docs.

Do not let `AGENTS.md` become a history or rationale document.

Move historical decisions, extended rationale, old tradeoffs, meeting notes, and background explanations into separate task-specific Markdown files, then link to them from `AGENTS.md`.

If `AGENTS.md` grows beyond about 150-200 lines, propose splitting it before adding more content.

## Why

Agents follow short, high-signal, immediately actionable instructions more reliably than long mixed-context files. When `AGENTS.md` becomes too large, important conventions can get buried even if they are clearly written.

## Recommended Structure

Use `AGENTS.md` for operational guidance:

- How to run checks.
- Where important files live.
- What conventions are current.
- What mistakes to avoid.
- Which supporting docs to consult for deeper context.

Use separate docs for background:

- `docs/architecture-decisions.md`
- `docs/history.md`
- `docs/rationale/<topic>.md`
- `docs/runbooks/<workflow>.md`

## Maintenance Check

Before adding to `AGENTS.md`, ask:

- Is this instruction needed during active coding?
- Is it current and actionable?
- Can it be stated in one or two short bullets?
- Would a link to a deeper document be better?

If the answer points toward background or explanation, put it in a separate Markdown file and link to it.
