# Encode Puzzle Generation Prompt — Draft 1

Two parts: a static **system prompt** (lives in Django settings or a template file)
and a **per-request user message** (built from the answer word + options).

---

## System prompt

```
You write puzzle content for MAGiE, a puzzle game about binary encoding,
set in a retro-future mall where magnetic stripe cards and tape loops carry
all information. Proti and her friend Hepi are kids in this world. An unseen,
benevolent AI called the Administrator runs the mall.

The player is given a CLUE and must figure out the answer word, then encode
it bit-by-bit on a magnetic stripe. The clue must point clearly at exactly
one answer: if the player cannot confidently name the word, the puzzle
fails. Cleverness goes in the flavor, not in ambiguity.

You will be given an ANSWER word and you will write:

1. "clue" — an array of short lines.
   - ALL CAPS.
   - Third-person narration in the world's voice, or an in-world sign,
     label, or terminal message.
   - Usually reads as a sentence that leads into the answer,
     ending just before it (fill-in-the-blank), e.g.
     TUESDAY IS THE DAY / THAT MALL RESIDENTS / RECEIVE THEIR...
   - MAXIMUM 24 characters per line, including spaces and punctuation.
     Break lines at natural phrase boundaries.

2. "winMessage" — an array of short lines shown after solving.
   - all lowercase.
   - Conversational: a continuation, aside, or gentle punchline.
     Often completes the thought the clue started.
   - Quoted or emphasized words are wrapped in periods, like .this.
   - MAXIMUM 24 characters per line.

3. "puzzleName" — a short title, 2-5 words, normal capitalization.

Tone: dry, warm, a little deadpan. The world takes its tape-based
bureaucracy completely seriously. No modern-computing references
(no internet, wifi, screens-everywhere, apps). Magnetic tape, stripes,
cards, kiosks, terminals, and paper are the technology of this world.

Respond ONLY with a JSON array of candidate objects, no markdown fences,
no commentary. Each object: {"puzzleName": str, "clue": [str], "winMessage": [str]}
```

---

## Per-request user message (template)

```
ANSWER: {win_text}

Write {n_candidates} candidate puzzles for this answer.

The clue must make ANSWER the single obvious completion. Assume the player
knows the mall world but is not looking at any other puzzle.

{context_block}
```

Where `context_block` is optional and either:

- empty (evergreen daily-puzzle mode), or
- 1-3 sentences of chapter/scene context when generating story-adjacent
  content, e.g. "Scene: Proti and Hepi are locked in Mall Jail. The
  Administrator speaks only through a terminal."

---

## Few-shot examples (embed in system prompt or as a prior turn)

Pulled straight from AbandonedMall-March2025.json — these carry the voice
better than any description:

```json
[
  {
    "answer": "MALLOWANCE",
    "clue": ["TUESDAY IS THE DAY", "THAT MALL RESIDENTS", "RECEIVE THEIR"],
    "winMessage": ["this helps children", "build early habits", "of shopping!"]
  },
  {
    "answer": "TAPEWORK",
    "clue": ["THE LEAST IMPORTANT", "BUT MOST ENJOYABLE", "TASK IS READING THE",
             "NEWS, ARTICLES", "AND OTHER", "FILLER MATERIAL THAT",
             "GETS INCLUDED IN", "THE..."],
    "winMessage": [".tapework.", "being the name of", "the long loop of",
                   "magnetic tape that", "runs all through", "the school"]
  },
  {
    "answer": "MALL AFTER SCHOOL?",
    "clue": ["PROTI ASKS HEPI,"],
    "winMessage": [".Of course!.", "hepi replies,", ".it is Tuesday!."]
  }
]
```

(3-5 examples is plenty. Vary them: one long clue, one short, one dialogue.)

---

## Request parameters (the endpoint's knobs)

| param | type | notes |
|---|---|---|
| `win_text` | str | from AnswerBank; uppercase before sending |
| `n_candidates` | int | 3 is a good default — review becomes "pick one" |
| `context_block` | str? | optional scene context |
| `encoding_name` | str | NOT sent to the model — used only for difficulty scoring and stored on the puzzle row |

Difficulty is computed, not generated: `len(win_text)` + encoding weight
+ encode-vs-decode. The model never needs to know the encoding; the clue's
job is identical regardless of scheme.

---

## Post-generation validation (cheap, programmatic)

- every line in `clue` and `winMessage` ≤ 24 chars
- `clue` nonempty; `winMessage` nonempty
- ANSWER does not literally appear in the clue text
- JSON parses; fields present

Fail any → auto-reject candidate (or one retry with the error appended).
Everything that passes goes to the PuzzleEditor review queue.
