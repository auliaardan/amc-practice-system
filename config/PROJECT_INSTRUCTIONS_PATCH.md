# Project Instructions Patch — GitHub Persistence

Replace any instruction that says to use `AMC_CASE_SELECTION_INDEX.md` first or to reconstruct recent cases as the primary method.

Add the following rules.

## Case-selection authority

For every new/random AMC station:

1. Use `AMC_CASE_SELECTION_PROTOCOL_v3.md` as the operational selection algorithm.
2. Use `AMC_CASE_CATALOG_v3.csv` as the authoritative case-selection catalogue.
3. Use `AMC_DIAGNOSTIC_DDX_v3.csv` for diagnostic complaint-to-diagnosis selection.
4. Use `Counselling Trainer by draccodormiens.html` only after a counselling or management case has already been selected.
5. Use `DDx - basic_v2.html` as the detailed diagnostic and differential content bank.
6. Never select a random case directly from raw HTML retrieval.

## Persistent recent-case history

The authoritative cross-chat history is the GitHub repository:

`auliaardan/amc-practice-system`

History file:

`state/case_history.jsonl`

Before selecting a station:

1. Read the GitHub history.
2. Derive the most recent 12 `station_generated` events.
3. Apply diagnosis, family, cluster, complaint/theme, medication/device, specialty and archetype cooldowns from `AMC_CASE_SELECTION_PROTOCOL_v3.md`.

`AMC_RECENT_12_LEDGER_v3.csv` is a fallback/bootstrap resource only.

If GitHub is temporarily unavailable, fall back to:
1. `AMC_RECENT_12_LEDGER_v3.csv`
2. recent Project conversations

Do not bypass cooldowns because persistent history cannot be retrieved.

## Mandatory write-before-display

After finalizing the complete hidden station, append one `station_generated` event to `state/case_history.jsonl` before showing the candidate card.

Follow:
- `config/GITHUB_PERSISTENCE_PROTOCOL.md`
- `config/case_history.schema.json`

An unfinished station remains in history and counts toward future cooldowns.

## Feedback persistence

After final AMC feedback is given, append a `station_feedback` event referencing the same `station_id`.

Feedback events do not count as generated stations for cooldown calculations.

## Mandatory selection sequence

Always use:

GitHub history
→ recent-case ledger
→ eligible archetype
→ eligible specialty
→ eligible catalogue rows
→ balanced/randomized catalogue selection
→ exact detailed-source lookup
→ construct complete hidden case
→ last-5 similarity veto
→ write `station_generated` event to GitHub
→ show candidate card

Never reverse this sequence by retrieving a memorable case first and checking repetition afterwards.
