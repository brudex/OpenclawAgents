# Image style benchmark (social + articles)

**Purpose:** Fixed **illustration system** for QuizFactor / educational product marketing. Agents merge this with **`post-body.md`**, **`teaser.md`**, or **`article.md`** so pixels match copy—not generic stock.

## Canonical visual system (structure & style)

Use this block as the **stable backbone** of every `prompt-master.txt` (edit only where **brand kit** or **copy-specific** details require it):

> **Professional flat vector illustration** for an educational quiz / learning product. **Composition:** A **hand holding a smartphone** in the foreground; the phone screen shows a **quiz or lesson UI** with **multiple-choice-style buttons or clear lesson steps** (not illegible micro-text). In the **mid/background**, a person **relaxes on a couch** using a **tablet** that echoes the same learning theme. **Floating around the scene**, cute **minimalist** icons (same line weight): **open books**, **lightbulbs with simple brain shapes**, **checkmarks**, and a **graduation cap**—plus **one or two extra icons** tied to the **post/article topic** (see *Content from copy* below). **Default color scheme:** **deep navy blue** background, **bright yellow** accents, **white** linework and key highlights. **Quality:** clean, modern, **corporate educational** aesthetic, **high resolution**, **2D vector art** (not photorealistic), generous negative space, crisp edges.

## Content from copy (mandatory)

The benchmark is **not** a generic scene. **Derive scene meaning from the source document:**

| Source | Minimum extraction |
|--------|--------------------|
| Social **`post-body.md`** | First **hook line** + **must-win message** + any **named topic, course, or outcome** in the `## Publish-ready` block (or equivalent). |
| LinkedIn **`article.md`** | **Title** + **TL;DR** or lede + **first H2 theme** (or strongest concrete example in the opening sections). |

**On-screen text (phone / tablet):** Where the model can render short UI text, use a **paraphrase** of the hook or thesis (**≤8 words per line**, **≤3 lines** on the phone; **no lorem ipsum**). Examples: “Cut study time in half”, “CompTIA Security+ in 20 min/day”—tuned to **this** post. If the API cannot place text reliably, state in `text-overlay.md` and keep the **visual metaphor** (icons, scene) tightly aligned with the same nouns.

**Floating icons:** Keep the **benchmark set** (books, brain-lightbulb, checkmark, cap). **Add or emphasize** 1–2 motifs that mirror the copy (e.g. shield for security, cloud for cloud certs, chart for analytics).

**Anti-generic check:** If the image could apply to **any** edtech post without reading the copy, the prompt is **too weak**—inject specific nouns from the post into `prompt-master.txt`.

## Brand kit precedence

If **`brand-images/`** (or **`BRAND_IMAGES_DIR`**) has **`palette.md`** / **`logo-usage.md`**:

- **Logo** and **wordmark** rules always win (reference image or verbatim description per main skill).
- **Colors:** Prefer **brand hex** for primary accents and logo surrounds; **preserve** the overall **flat vector + white linework** read unless the brand doc forbids white lines. **Navy + yellow** in this file is the **default only when** the brand kit does not specify alternatives.

## Negative prompt hints

Add to **`negative-prompt.txt`** as needed: photorealistic skin, wrong logo, unreadable tiny paragraphs, clutter competing with the phone hero, **celebrity likeness**, **watermarks**, **generic unrelated quiz topic** (if copy is about X, ban visual story about unrelated Y).
