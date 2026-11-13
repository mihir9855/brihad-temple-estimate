# Brihad Temple Estimate

App to compute every part of a temple (prasad) from the garbhagruh size — measurements and stone
quantity (CFT) and cost — based on "Shilp Ratnakar" (the owner's CAD drawings are design examples only).
Owner: a temple contractor; only user; uses it on computer and phone (must work offline).

Read first: `docs/PLAN.md` (the agreed plan) and the `shilp-ratnakar` skill (book rules, Gujarati).

Hard rules from the owner:
- UI in Gujarati. **Never show gaj or angul** — only inches and feet (convert internally, 1 gaj = 18″, 1 angul = ¾″).
- Main unit is inches, also show feet-inch; running feet for lengths, sq.ft for areas, CFT for stone.
- **Every displayed size is rounded UP to a whole inch** (11⅛″ → 12″). No fractions anywhere.
- Stone: CFT = L × W × H × Nang ÷ 1728 (from rounded sizes); cost = CFT × rate. No wastage, no block size.
- Whole temple in one stone (one rate per project).
- Thar depth: brick backing → stone facing + nikalo; full stone → full wall + nikalo.
- **All calculations follow Shilp Ratnakar.** The owner's CAD drawings (Dhuliya, Ambaji) are only design/look examples, not calculation sources. Other book methods stay selectable. Show ⚠ where the book is missing or doubtful. Changes will be revised later.
- Ask the owner before guessing on anything structural; record decisions in `docs/PLAN.md`.

Status: planning done, no code yet. Build in phases (PLAN section 10).
