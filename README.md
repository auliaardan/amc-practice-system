# AMC Practice System

Persistent state for an AMC Clinical Examination practice project.

## Purpose

This repository stores case-selection state and practice history. Detailed clinical content remains in the ChatGPT Project resources.

The persistent source of truth for anti-repetition history is:

`state/case_history.jsonl`

The history is append-only. A generated station is recorded before its candidate card is displayed, so unfinished stations still count toward cooldowns.

## Repository layout

```text
amc-practice-system/
├── state/
│   └── case_history.jsonl
└── config/
    ├── case_history.schema.json
    ├── GITHUB_PERSISTENCE_PROTOCOL.md
    └── PROJECT_INSTRUCTIONS_PATCH.md
```

## Source-of-truth split

### ChatGPT Project

Selection and clinical resources:

- `AMC_CASE_SELECTION_PROTOCOL_v3.md`
- `AMC_CASE_CATALOG_v3.csv`
- `AMC_DIAGNOSTIC_DDX_v3.csv`
- `AMC_RECENT_12_LEDGER_v3.csv` (fallback/bootstrap only)
- `Counselling Trainer by draccodormiens.html`
- `DDx - basic_v2.html`

### GitHub

Persistent cross-chat state:

- complete station-generation history
- optional station-feedback events

## Operating rule

For every new station:

1. Read `state/case_history.jsonl`.
2. Derive the most recent generated stations.
3. Apply the v3 cooldown and balancing protocol.
4. Finalise the complete hidden station.
5. Append one `station_generated` event.
6. Only then show the candidate card.

## Privacy

This repository is for fictional AMC practice metadata only.

Do not store:
- real patient information
- credentials or API keys
- personal medical records
- unrelated private information
