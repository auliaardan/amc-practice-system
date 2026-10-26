# Australia hospital prospect list (reconstructed)

This folder holds a **working directory of candidate Australian hospital sites** for medical-workforce/JMO outreach.

## Files
- `hospital_additions_reconstructed_2026-10-26.csv`: **1028 candidate hospital sites**, excluding 86 records matched to physical hospitals already named in the user's 96-row original list (conservative name/alias matching); 2 duplicate source identities were also collapsed.
- `hospital_coverage_summary_2026-10-26.csv`: state × public/private counts.

The owner's original 96-row CSV and its personal outreach notes/statuses have **not** been published because this repository is public.

## Provenance and limitations

This is a **reconstruction**, not a copy of the original Deep Research export that reported 600 or 1,030 additions. The complete underlying output from that research session was unavailable for transfer to GitHub. The hospital identity data come from a public GitHub mirror of an AIHW MyHospitals mapping extract:
https://github.com/virani-ea/fit3179-assignment-2/blob/main/data/myhosp-mapping-details-extract.csv

Official dataset origin: https://www.aihw.gov.au/hospitals/other-resources/myhospitals-api

AIHW content and naming may have changed since the mirrored snapshot. The current 3 October 2026 republished mapping is available at https://publicdata.au/d/au-hospitals-myhospitals/v/2026-10-03/ ; it was **not** possible to directly import that site's export in this run. The dataset here therefore must be checked against current official hospital directories before using it for bulk outreach.

- Only source rows labelled **Open** and **Hospital** were retained. This includes day-procedure and specialty units, not all suitable RMO employers.
- **102 rows** have a shared network/HHS/LHN email from official sources discussed in the original research report; many rows may share the same inbox. These are **not** 102 unique email addresses. Blank email cells mean *not verified*.
- A hospital or HHS contact does **not** establish that the facility accepts IMGs, AHPRA provisional registration, visa sponsorship, or the supervision needed for the Standard Pathway.
- Original outreach records were used for conservative exclusions by hospital name, but **network-only** records were not treated as covering every associated campus.
- Avoid sending mass duplicate emails to shared recruitment inboxes.

Attribution: Based on Australian Institute of Health and Welfare material, sourced via an independently published GitHub mirror. AIHW's own copyright and data licensing apply. No claim of official government endorsement.


## Actionable recruitment emails / mail-merge

The earlier hospital-site CSV is **not email-ready**. For an actual outreach workflow, use:
- [contacts_new_departmental_inboxes.csv](./contacts_new_departmental_inboxes.csv): 13 *additional*, publicly published team/corporate email addresses from NSW HETI, QLD Health and Calvary. This is the same 12-column format as the owner's original local `contacts.csv`. Not all routes recruit RMOs; the source links permit verification.
- [rmo_email_outreach.py](./rmo_email_outreach.py): review-first CLI that only selects `include=yes` and `status=not_contacted`, deduplicates by email across input files, excludes recipients already marked `contacted`, and records a local send log.

**Setup**: keep the original 96-contact `contacts.csv` private on your computer; download only the new file and script from GitHub. From the directory containing them:

```bash
python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv
python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv --draft --limit 5
# AFTER reviewing draft content, to explicitly send a controlled batch:
# GMAIL_APP_PASSWORD is obtained from your own Gmail account, never store it in source control.
python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv --send --confirm-send YES --limit 5 --cv Aulia_RMO_CV.pdf
```

Do not set `--send` without reviewing targets and content. The `--draft` switch creates local .eml files, **not** drafts inside Gmail. The `--send` switch delivers directly via Gmail SMTP; it requires an application password. Keep `rmo_sent_log.csv` locally to avoid re-sending. Never publish CV, passwords, sending logs or the original contacts file in this public repository.

A published JMO email does not establish IMG eligibility, an available January 2027 vacancy, provisional-registration supervision, or visa sponsorship. First replies should confirm those facts. For NSW, the main 2027 JMO hiring pathway remains its formal online recruitment process; email enquiry is not a substitute for applying.
