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
