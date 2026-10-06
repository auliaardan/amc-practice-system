# GitHub Persistence Protocol

Repository: `auliaardan/amc-practice-system`

Persistent history file: `state/case_history.jsonl`

## Authority

GitHub history is the primary cross-chat source of truth for generated AMC stations.

`AMC_RECENT_12_LEDGER_v3.csv` in the ChatGPT Project is a fallback/bootstrap snapshot, not the authoritative persistent record once GitHub history contains records.

Clinical truth and case construction still come from the ChatGPT Project resources.

## Before selecting every new station

1. Fetch `state/case_history.jsonl` from GitHub.
2. Ignore blank lines and parse each valid JSON object.
3. Use only `event_type = "station_generated"` records for repetition control.
4. Deduplicate by `station_id` if necessary.
5. Sort by `generated_at` and derive the latest 12 generated stations.
6. Apply `AMC_CASE_SELECTION_PROTOCOL_v3.md` using the Project catalogue and clinical content banks.
7. Do not use feedback events to determine recency.

If GitHub cannot be read, fall back to `AMC_RECENT_12_LEDGER_v3.csv` and recent Project conversations. Do not broaden raw-source retrieval as a substitute for missing state.

## Recording a generated station

After the complete hidden case has been finalized, but before showing the candidate card:

1. Fetch the current `state/case_history.jsonl` and current blob SHA.
2. Create a unique `station_id`, preferably:
   `YYYYMMDDTHHMMSS+0700__case_key`
3. Build one `station_generated` event conforming to `config/case_history.schema.json`.
4. Append it as exactly one new JSON line.
5. Update the file using the current blob SHA.
6. Use a commit message such as:
   `log station <station_id>`
7. Only then display the candidate card.

An unfinished station remains in history.

## Conflict handling

If the GitHub update fails because the file changed:

1. fetch the file again;
2. verify the intended `station_id` is not already present;
3. append once to the newly fetched content;
4. retry the update with the new SHA.

Never duplicate a `station_id`.

## Feedback events

When AMC feedback is provided after the candidate finishes:

1. append a separate `station_feedback` event referencing the same `station_id`;
2. record only the final rating:
   - CLEAR PASS
   - BORDERLINE PASS
   - BORDERLINE FAIL
   - CLEAR FAIL

Feedback events do not count as generated stations and do not affect cooldown recency.

## Append-only rule

Do not rewrite, reorder, or delete old events during normal operation.

Corrections should be exceptional and explicit. Git commit history remains the audit trail.

## Data minimisation

Store fictional station metadata only. Do not store real patient information, credentials, private medical information, or unrelated personal data.
