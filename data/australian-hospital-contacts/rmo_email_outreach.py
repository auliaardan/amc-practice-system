#!/usr/bin/env python3
"""Review, draft or send Australian hospital JMO eligibility enquiries.

Examples:
  python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv
  python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv --draft
  python rmo_email_outreach.py --csv contacts.csv contacts_new_departmental_inboxes.csv \
    --send --confirm-send YES --limit 5 --cv "/path/to/CV.pdf"

Requires only Python's standard library. Direct sending uses Gmail SMTP and
an app password supplied through the GMAIL_APP_PASSWORD environment variable.
Never commit passwords, personal CVs or the user's contact-status CSV.
"""
import argparse
import csv
from email.message import EmailMessage
from email.utils import formataddr
import getpass
import os
from pathlib import Path
import re
import smtplib
import ssl
import time

SENDER = "auliarahmanardan@gmail.com"
SIGNATURE = "Aulia Rahman Ardan\nMedical Officer\n" + SENDER
EMAIL_RE = re.compile(r"^[^@\s,;]+@[^@\s,;]+\.[^@\s,;]+$")


def rows_from_files(paths):
    seen = set()
    already_contacted = set()
    rows = []
    for file in paths:
        with open(file, newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                email = (row.get("email") or "").strip().lower()
                if not EMAIL_RE.fullmatch(email):
                    continue
                if (row.get("status") or "").strip().lower() == "contacted":
                    already_contacted.add(email)
                rows.append(row)
    selected = []
    for row in rows:
        email = row["email"].strip().lower()
        if email in seen or email in already_contacted:
            continue
        if (row.get("include") or "").strip().lower() != "yes":
            continue
        if (row.get("status") or "").strip().lower() not in ("", "not_contacted"):
            continue
        seen.add(email)
        selected.append(row)
    return selected, len(already_contacted)


def create_message(row, sender, cv=None):
    hospital = (row.get("hospital") or "your health service").strip()
    msg = EmailMessage()
    msg["From"] = formataddr(("Aulia Rahman Ardan", sender))
    msg["To"] = row["email"].strip()
    msg["Subject"] = "Enquiry: supervised RMO/JMO opportunities in 2027 — " + hospital
    message = (
        "Dear Medical Workforce Team,\n\n"
        f"I am enquiring about supervised Resident Medical Officer or Junior Medical Officer "
        f"opportunities commencing in or after January 2027 at {hospital}.\n\n"
        "I hold an AMC Certificate, having passed both the AMC CAT MCQ and AMC Clinical "
        "examinations. I graduated in medicine from Universitas Indonesia and currently "
        "work as a General Medical Officer in Indonesia. My clinical experience includes "
        "a 12-month Indonesian internship with Emergency Department, inpatient ward "
        "and ICU rotations, followed by outpatient and on-site emergency-room care.\n\n"
        "I am eligible to apply for provisional registration under the AMC Standard "
        "Pathway, subject to Medical Board of Australia/Ahpra assessment, a suitable "
        "supervised position and all other requirements. I do not yet hold Australian "
        "medical registration or Australian work rights.\n\n"
        "Could you please advise whether your service considers applicants in my "
        "position, whether suitable clinical supervision may be available, and whether "
        "employer visa sponsorship might be considered? If an appropriate vacancy or "
        "recruitment process exists, I would appreciate the relevant link.\n\n"
        "Kind regards,\n" + SIGNATURE
    )
    msg.set_content(message)
    if cv:
        data = Path(cv).read_bytes()
        msg.add_attachment(data, maintype="application", subtype="pdf",
                           filename=Path(cv).name)
    return msg


def sent_emails(path):
    if not Path(path).exists():
        return set()
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["email"].lower() for row in csv.DictReader(handle)}


def log_send(path, row):
    new = not Path(path).exists()
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["email", "hospital", "sent_utc"])
        if new:
            writer.writeheader()
        from datetime import datetime, timezone
        writer.writerow({
            "email": row["email"].lower(),
            "hospital": row.get("hospital", ""),
            "sent_utc": datetime.now(timezone.utc).isoformat()
        })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", nargs="+", required=True, help="Existing list first, new contacts second")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--draft", action="store_true", help="Create local .eml files for manual review")
    group.add_argument("--send", action="store_true", help="Send through Gmail SMTP, requires confirmation")
    parser.add_argument("--confirm-send", default="", help="Must equal YES to use --send")
    parser.add_argument("--limit", type=int, default=5, help="Maximum emails per invocation (default: 5)")
    parser.add_argument("--delay", type=float, default=20, help="Seconds between sent emails")
    parser.add_argument("--cv", help="Optional PDF CV attachment, kept off GitHub")
    parser.add_argument("--sender", default=SENDER)
    parser.add_argument("--log", default="rmo_sent_log.csv")
    parser.add_argument("--draft-dir", default="rmo_email_drafts")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.cv and (not Path(args.cv).is_file() or Path(args.cv).suffix.lower() != ".pdf"):
        parser.error("--cv must point to an existing PDF")
    if args.send and args.confirm_send != "YES":
        parser.error("Sending requires --confirm-send YES")
    selected, previously_contacted = rows_from_files(args.csv)
    logged = sent_emails(args.log)
    selected = [r for r in selected if r["email"].lower() not in logged][:args.limit]
    print(f"Previously contacted addresses in source CSVs: {previously_contacted}")
    print(f"Eligible unique recipients in this batch: {len(selected)}")
    if not selected:
        return
    for i, row in enumerate(selected, 1):
        print(f"{i}. {row.get('hospital','')} <{row['email']}>")
    if not args.send and not args.draft:
        print("PREVIEW ONLY. Add --draft to create .eml files or --send --confirm-send YES to deliver.")
        return
    if args.draft:
        target = Path(args.draft_dir)
        target.mkdir(parents=True, exist_ok=True)
        for i, row in enumerate(selected, 1):
            filename = target / f"{i:03d}_{re.sub(r'[^A-Za-z0-9_-]', '_', row['email'])}.eml"
            filename.write_bytes(create_message(row, args.sender, args.cv).as_bytes())
        print(f"Created {len(selected)} EML files in {target}/. These are not Gmail Drafts.")
        return
    password = os.environ.get("GMAIL_APP_PASSWORD") or getpass.getpass("Gmail app password: ")
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as client:
        client.starttls(context=ssl.create_default_context())
        client.login(args.sender, password)
        for i, row in enumerate(selected):
            message = create_message(row, args.sender, args.cv)
            client.send_message(message)
            log_send(args.log, row)
            print("Sent to", row["email"])
            if i != len(selected) - 1:
                time.sleep(max(args.delay, 5))
    print("Completed. Keep the sent log to prevent repeat emails.")


if __name__ == "__main__":
    main()
