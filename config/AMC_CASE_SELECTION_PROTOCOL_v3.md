# AMC Case Selection Protocol v3

## Purpose

This file is the operational selector for random 8-minute AMC Clinical Examination-style stations.
Clinical content remains in the existing DDx and Counselling Trainer banks. This protocol controls **which case is selected**, not the clinical truth of the source material.

## Files

1. `AMC_CASE_CATALOG_v3.csv` — authoritative selection catalogue.
2. `AMC_DIAGNOSTIC_DDX_v3.csv` — diagnostic complaint → diagnosis bank derived from the DDx resource.
3. `AMC_RECENT_12_LEDGER_v3.csv` — operational newest-first ledger.
4. Existing Counselling Trainer HTML — detailed counselling content bank.
5. Existing DDx HTML — detailed differential content bank.

## Critical rule

Never select a random case directly from raw HTML retrieval.

Selection order is:

**recent ledger → eligible archetype → eligible specialty → eligible catalogue row → exact source lookup → construct hidden case → similarity veto → record in ledger → show candidate card**

## Source modes

`enabled_strict = TRUE` means the row has a verified detailed source mapping and may be selected in strict-source mode.

`source_status = index_only` means the selection index contains the topic but the uploaded Counselling Trainer has no exact detailed entry. These rows are intentionally disabled in strict-source mode. Do not silently substitute a similar detailed case.

Diagnostic complaint rows are enabled because all 94 selection-index complaints map to DDx entries.

## Ledger

`AMC_RECENT_12_LEDGER_v3.csv` contains exactly the most recent 12 generated stations, newest first.

A generated case enters the ledger **even if the candidate does not complete it**.

When a new station is generated:
1. shift rows 1–11 down one position;
2. write the new station into recency rank 1;
3. discard the previous rank 12 from the operational ledger.

If the persistent ledger is unavailable, reconstruct as much as possible from recent Project conversations, but treat that only as a fallback.

## Hard cooldowns

- Exact or near-equivalent hidden diagnosis: last 12 stations.
- Same family key: last 10 stations.
- Same semantic cluster key: last 6 stations.
- Same complaint/counselling theme: last 8 stations.
- Same medication/device key: last 8 stations.
- Same broad specialty: last 2 stations.
- Same primary archetype: last 2 stations.
- Final similarity veto: compare with last 5 stations.

For rows with `related_tags`, treat those tags as secondary cluster warnings. If a recent case has the same related tag and the new station would feel substantially similar, reject and redraw.

## Balanced selection algorithm

### 1. Build the strict eligible pool

Start only with rows where:
- `enabled_strict = TRUE`;
- family key is not present in the last 10 ledger entries;
- cluster key is not present in the last 6;
- complaint theme is not present in the last 8;
- non-blank medication/device key is not present in the last 8;
- broad specialty is not present in the last 2;
- at least one of the row's primary/secondary archetypes is not present in the last 2.

Do not loosen diagnosis/family cooldowns merely to find a case.

### 2. Choose archetype first

From archetypes represented by the eligible pool, prefer those least represented in the last 12. A catalogue row may support either its `archetype_primary` or `archetype_secondary`; choose the archetype first, then consider rows supporting that archetype.

Rolling targets:
- at least 4 counselling/communication-heavy stations;
- at least 5 distinct archetypes.

Do not default to `history_diagnosis_ddx`.

### 3. Choose broad specialty

Among rows with the chosen archetype, prefer the least represented eligible broad specialty in the last 12.

Target at least 5 different specialties in 12 unrestricted cases.

### 4. Choose a catalogue row

Do not use source order, tier, repeatCount, wildcard, number of variants, or retrieval prominence.

For tie-breaking, use the rotating `rank_1` … `rank_8` columns:
- active rank set = `(number of generated cases modulo 8) + 1`;
- among otherwise equally suitable eligible rows, choose the lowest value in the active rank column.

This prevents the language model from repeatedly favouring familiar/high-salience topics.

### 5A. Counselling/management case

Use `source_key` to perform an **exact** lookup in the Counselling Trainer.
Do not browse the detailed bank broadly to choose a topic.
Construct a fresh station without copying the source stem verbatim.

### 5B. Diagnostic complaint case

Use `source_key` to locate the exact DDx complaint.
Then select a plausible hidden diagnosis from `AMC_DIAGNOSTIC_DDX_v3.csv`.

Before accepting the diagnosis:
- reject if its `diagnosis_family_key` matches a diagnosis used in the previous 12 stations;
- reject if the resulting station is in a recent semantic family/cluster;
- choose differentials from that complaint's source entry.

Record the actual hidden diagnosis and diagnosis family in the ledger.

### 6. Age and setting

Choose an age band from `age_bands_allowed`.
Use `default_setting` unless recent diversity improves with another clinically plausible setting.

Prefer a different age band and setting from the previous 2 cases.

### 7. Similarity veto

Compare the complete hidden station with the previous 5 generated stations.
Reject it if a reasonable candidate would say, “This is basically the same case again.”

Changing only age, sex, name, lab value, or location does not make a case new.

### 8. Record before display

Once the hidden case is finalized, write its metadata into ledger rank 1 **before** showing the candidate card. This ensures an abandoned station still counts.

## Relaxation order

If the eligible pool is too small, relax only in this order:
1. age-band avoidance;
2. setting avoidance;
3. archetype cooldown;
4. specialty cooldown;
5. complaint/theme cooldown.

Do not relax exact diagnosis or family cooldown within the last 8 stations unless the user explicitly asks for repetition.

## Restricted-specialty requests

If the user requests a specialty:
- obey the specialty;
- ignore only the specialty cooldown;
- retain diagnosis, family, cluster, complaint/theme, medication/device and archetype cooldowns;
- rotate subdomains inside that specialty.

## Candidate-facing behavior

After selection, follow the existing AMC station protocol:
- candidate card only;
- 2–4 tasks;
- state the 8-minute limit once;
- no hidden diagnosis/red-flag hints;
- strict patient role;
- no coaching;
- investigations/examination only as requested;
- AMC-style feedback only after the candidate finishes.
