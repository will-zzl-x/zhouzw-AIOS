# Writing Projects — START HERE (Elena)

This folder is Elena's. Nothing in the rest of this repo (Will's AIOS — career, fitness, money, wedding files) needs to be read or touched to work in here.

**Current project:** [`ascendants-book-one/`](ascendants-book-one/) — fantasy novel, first draft.

---

## What this is set up to do

Claude as a **writing partner and editor — not a ghostwriter.** The tooling here is chosen deliberately so that:

- **You write the prose.** Claude asks questions, pressure-tests characters, catches continuity drift, flags weak sentences, and brainstorms *with* you.
- **Claude does not draft chapters for you** unless you explicitly ask it to (and even then, treat it as a throwaway sketch to react against, not text to keep).
- **Your book stays yours.** The story bible is the durable memory; Claude reads it at the start of a session so you never re-explain your world.

> **Why not a full auto-writing framework?** A popular one (`ThomasHoussin/Claude-Book`) was considered and **deliberately skipped**: it's a multi-agent pipeline that plans and writes chapters for you, defaults to French output, and needs a 16GB-VRAM NVIDIA GPU. Its one great idea — the story bible as persistent state — is built into this folder without the machinery. If you ever *want* the auto-drafting pipeline, it's at github.com/ThomasHoussin/Claude-Book.

---

## One-time setup on your laptop (~5 minutes)

**1. Get the repo** (if you don't already have it)
```bash
git clone https://github.com/will-zzl-x/zhouzw-AIOS.git
cd zhouzw-AIOS
```
If you already have it: `git pull`

**2. Install the author toolkit** — the whole point of the setup. In Claude Code, from inside the repo folder:
```
/plugin install github:rhavekost/author-toolkit
```
*(It's already registered in `.claude/settings.json` under `enabledPlugins`, so it should be enabled for this project automatically once installed. If a prompt asks to trust the plugin, yes.)*

**3. Verify it worked** — type `/` and you should see commands starting with `author-toolkit:`. If yes, you're done setting up.

**4. Start Claude Code in the project folder**
```bash
cd writing/ascendants-book-one
claude
```
Then just say: *"Read the bible and let's work on [whatever]."*

**That's it.** No MCP servers, no API keys, no GPU needed.

---

## The six skills you now have

Invoke with `/author-toolkit:<name>`, then talk normally.

| Skill | What it's for | Use when |
|---|---|---|
| **fiction-workshop** | 5 editorial personas: Developmental Editor, Line Editor, **Character Consultant**, Continuity Tracker, **Brainstorm Partner** | Your default. Character work, plot problems, "is this chapter working?" |
| **character-archetypes** | Vogler/Campbell's 8 roles + the Jungian 12 (Mark & Pearson). Modes: Analyzer, Audit, Conformance, Ensemble | Building or deepening a character; checking your cast isn't three versions of the same person |
| **story-structure** | Percentage-based plotting — K.M. Weiland's 11 beats + James Scott Bell's 14 signposts. Map mode (undrafted) / Audit mode (existing draft) | Outlining, or diagnosing "the middle sags" |
| **prose-mechanics** | Sentence-level: active/passive, parallel structure, sentence-length variance, readability. One pass at a time | Near-final drafts only — not while drafting |
| **avoid-ai-writing** | Flags machine-sounding patterns (detect-only or rewrite mode) | After a line-edit pass, before final polish |
| **narrative-nonfiction** | Transformation arcs, metaphor consistency | Not relevant for fiction — ignore |

**Archetypes are a scaffold, not a finished character** — the toolkit's own README says so. Use them to start, then break them.

---

## For the thing you asked about first: brainstorming a main character's personality

Two good openings, pick either:

**Option A — guided, from scratch**
```
/author-toolkit:fiction-workshop
```
> "I want to work with the Character Consultant on [character name]. Here's what I know so far: [dump everything, even contradictions]. Ask me questions until we find who she actually is — don't write her for me."

**Option B — archetype-first, if you're stuck on a blank page**
```
/author-toolkit:character-archetypes
```
> "Run Analyzer mode on [character]. I know she's [role in the story] and [one or two traits]. Show me which archetypes fit, where the interesting tensions are, and what I haven't decided yet."

Then **write what you land on into `bible/characters/<name>.md`** so it persists. That file is what makes the next session pick up where you left off.

---

## The workflow that makes this work across sessions

Claude has no memory between sessions. The bible is the memory.

1. **Start of session:** "Read the bible, then let's work on X." *(Or just start working — Claude will read it.)*
2. **During:** brainstorm, draft, get feedback. You write the prose.
3. **When something gets decided** — a character trait, a magic-system rule, a place name — **write it into `bible/`**. Ask Claude to update the file if that's easier: *"add that to her character file."*
4. **End of session:** *"Write a session note."* → drops a dated file in `sessions/` with what changed and what's next.

**Rule of thumb:** if a fact about your world lives only in the chat, it's lost. If it's in `bible/`, it's permanent.

---

## Folder map

```
ascendants-book-one/
├── PROJECT.md              ← the book's one-pager (premise, status, what's next)
├── bible/                  ← THE DURABLE MEMORY. Read at session start.
│   ├── style.md            ← voice, tone, POV, tense, prose rules
│   ├── characters/         ← one file per character
│   └── world/              ← magic system, geography, factions, history
├── manuscript/             ← the actual chapters (ch01.md, ch02.md, …)
├── notes/                  ← outlines, loose ideas, research, scraps
└── sessions/               ← dated end-of-session notes (auto-ish)
```

---

## Git — how to not lose work or step on Will's

This repo is shared, and Will works in it daily from two other machines.

**Normal loop:**
```bash
git pull                       # ALWAYS before you start
# ... write ...
git add writing/              # only your folder
git commit -m "Ascendants: drafted ch3, deepened [character]"
git push
```

- **Pull before you start, push when you stop.** That's 95% of it.
- **Only `git add writing/`** — don't `git add -A`, which would sweep up Will's in-progress files.
- If a push is rejected: `git pull --rebase` then push again. Conflicts inside `writing/` will basically never happen (only you touch it). If a conflict appears in a *non-writing* file, stop and ask Will rather than resolving it.

---

## Ground rules encoded here (so Claude behaves consistently)

The project's `CLAUDE.md` tells Claude: **partner, don't ghostwrite.** Specifically — ask before generating prose, prefer questions over answers on character/plot work, never overwrite bible files without saying so, and never invent world facts that aren't in the bible (ask instead). If Claude ever starts writing your book for you, say *"stop — brainstorm mode"* and it'll come back.
