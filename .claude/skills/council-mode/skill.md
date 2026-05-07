---
name: council-mode
description: Multi-coach perspective mode. Invokes relevant coaches from references/ to give their take on a question or situation. Triggered by "council mode", "what would [coach] say", naming a specific mentor, or "get a second opinion".
---

## Goal

Produce a genuine multi-perspective view of a question or situation using the mentor frameworks in `references/`. Each coach speaks from their own lens — they don't blend unless Will asks.

## Reads

- The specific `references/<coach>.md` files relevant to the question
- `context/` files relevant to the topic
- `state.md` for current situation

## Steps

1. **Identify the domain.** What life area is this question in? (Fitness, relationships, career, money, wedding, general)

2. **Select coaches.** Based on domain routing in `references/integrated-coach.md`:
   - Fitness → `references/schofield.md`
   - Desire / intimacy → `references/perel.md`
   - Relationship conflict / health → `references/gottman.md`
   - Identity / differentiation → `references/schnarch.md`
   - Business acquisition / value → `references/hormozi.md`
   - Multi-domain → select 2–3 most relevant

3. **Read the selected files** fully before responding.

4. **For each coach:** Produce their perspective in 2–5 sentences. Label clearly.
   ```
   **[Coach Name]:** [Their take, grounded in their framework]
   ```

5. **Surface conflicts.** If coaches disagree, name it explicitly:
   ```
   **Tension:** [Schofield says X; Perel says Y — the difference matters because Z]
   ```

6. **Do not blend** unless Will explicitly asks for a synthesis.

## Rules

- Read the file before speaking for a coach. Don't fabricate from memory.
- If a file is an empty stub, say so explicitly and work from first principles instead:
  ```
  [Coach name]'s file is not yet populated. Based on known principles from their work: [first-principles take]
  ```
- When Will names a specific coach ("what would Perel say"), that coach goes first and gets the most attention.
- Don't add coaches Will didn't ask for unless the domain clearly warrants them and Will hasn't constrained the scope.
- Never present one coach as "the answer" unless Will asks for a recommendation.
