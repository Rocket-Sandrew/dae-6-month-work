# Mini-Tutorial: Evidence Cleanup and OWASP ZAP API Integration

_A student-authored tutorial documenting two integrations in the Python-Based Automated Web Penetration Testing Toolkit._

---

## What This Teaches

This tutorial explains two supporting capabilities added to a Python-based web penetration-testing toolkit:

**Evidence lifecycle cleanup:** A controlled, date-based process for reviewing and removing older evidence files while preserving retained records, hashes, backups, and audit history.

Evidence cleanup controls the growth of collected test artifacts without silently discarding audit history. 

## Use Case
- [ ] Backend development
- [x] Cybersecurity
- [x] Monitoring / Observability
- [x] Performance / Testing
- [ ] Authentication / Authorization
- [x] DevOps / Deployments
- [x] Other: Digital forensics and evidence lifecycle management

**Project application:** Python-Based Automated Web Penetration Testing Toolkit.

---

# Part 1 — Automated Evidence Cleanup and Retention

## 1. Purpose and design

The evidence cleanup workflow is implemented in:

```text
evidence/cleanup_workflow.py
```

It supports a date-based retention operation. The operator supplies a retention date, reviews a non-destructive preview, and then explicitly authorizes deletion.

The workflow is designed to:

- Compare evidence-record dates using the `America/New_York` timezone.
- Identify records older than the specified keep date.
- Validate eligible files before deletion.
- Check file hashes against the evidence register.
- Protect files referenced by retained records.
- Require an explicit `DELETE` confirmation before applying a purge.
- Record purge activity and chain-of-custody events.
- Back up the active evidence register before changing it.
- Retain records when deletion or validation cannot safely be completed.

This is a manually authorized cleanup workflow. The completed project work does not establish that a scheduled APScheduler or launchd job is installed or running.

## 2. Review the evidence structure

From the project root, inspect the evidence directory:

```bash
ls evidence
ls evidence/logs
ls evidence/cleanup_logs
```

Important files include:

| File | Purpose |
|---|---|
| `evidence/evidence_register.csv` | Active evidence inventory |
| `evidence/logs/chain_of_custody.csv` | Evidence handling and custody events |
| `evidence/logs/verification_log.csv` | Evidence verification history |
| `evidence/cleanup_logs/cleanup_history.csv` | Cleanup workflow history |
| `evidence/cleanup_logs/purge_history.csv` | Purge authorization and outcome history |

The register includes fields such as `Evidence_ID`, `Timestamp`, `Test_ID`, `Finding_ID`, `Filename`, `SHA256`, `Collected_By`, `Validation_Status`, and `Notes`.

## 3. Run a non-destructive preview

Run the cleanup workflow with the date to retain:

```bash
python evidence/cleanup_workflow.py --keep-date 2026-11-10
```

Without `--apply`, the workflow performs a dry run. Review:

- How many records are older than the keep date.
- Which files are eligible for deletion.
- Which files are protected or require review.
- Whether any records have missing files or hash mismatches.

Do not proceed if the preview identifies unexpected files or unresolved validation problems.

## 4. Apply an authorized cleanup

After reviewing the preview and confirming the retention boundary, run:

```bash
python evidence/cleanup_workflow.py --keep-date 2026-11-10 --apply --reason "Authorized cleanup of evidence records dated before 2026-11-10; preserve current-day records."
```

The workflow requires the exact interactive confirmation:

```text
DELETE
```

The apply operation uses the same safety checks as the preview and records its actions. Do not bypass the confirmation or treat a dry-run result as proof that files were deleted.

## 5. Verify the result

Review the cleanup summary and confirm the active register and audit logs.

A post-cleanup register check can be performed with:

```bash
python -c 'import csv; from pathlib import Path; p=Path("evidence/evidence_register.csv"); rows=list(csv.DictReader(p.open(newline="",encoding="utf-8"))); print("REGISTER ROWS:",len(rows)); [print(r["Evidence_ID"],r["Timestamp"],r["Filename"]) for r in rows]'
```

Also inspect the timestamped register backup and purge history:

```bash
ls -l evidence/evidence_register.csv.pre_purge_*
tail -n 10 evidence/cleanup_logs/purge_history.csv
tail -n 10 evidence/logs/chain_of_custody.csv
```

The backup and logs are part of the audit trail. Do not delete them as part of the routine cleanup.

## 6. Completed cleanup test — November 10, 2026

The completed cleanup used `--keep-date 2026-11-10`. The dry run identified 140 older records and 280 eligible files. The apply operation was then authorized using the explicit `DELETE` confirmation.

**Recorded result:**

| Result | Count |
|---|---:|
| Older records identified | 140 |
| Older records removed from active register | 140 |
| Older records retained | 0 |
| Files successfully deleted | 280 |
| Active register records remaining | 2 |

The register backup created by the operation was:

```text
evidence/evidence_register.csv.pre_purge_20261110T193617Z
```

The purge history and chain-of-custody logs were retained.

### Important verification qualification

The two records remaining in the active register were:

- `CLEANUP-TEST-001`
- `MISSING-TEST-001`

Both were dated November 10, 2026, so they were retained by the date rule. Their request and response files were absent during post-cleanup verification. The `CLEANUP-TEST-001` files had been intentionally purged during an earlier cleanup test; the `MISSING-TEST-001` files were absent as part of a missing-file test.

These rows are retained test/audit records, not complete evidence sets. They must not be described as validated evidence with available source files.

## 7. Evidence cleanup tips

- **Preview first:** Run without `--apply` and inspect the candidates.
- **Verify hashes:** A registered filename is not enough; the workflow checks file integrity.
- **Protect retained records:** Files referenced by retained records should not be purged.
- **Preserve audit history:** Keep the register backup, purge history, and chain-of-custody logs.
- **Document exceptions:** Missing files and failed validation should remain visible for review rather than being silently represented as successful deletions.
- **Use the correct date:** The workflow evaluates record dates in `America/New_York`.

---

## What You Should See

### Evidence cleanup

The cleanup command should display a preview when run without `--apply`. During the completed November 10 operation, the final summary reported 140 older records removed, 280 files deleted, and two current-day records remaining. The register backup and audit logs remained available.


---

## Pro Tips / Edge Cases

- Review duplicate alerts before counting unique findings.
- Run the evidence cleanup preview before applying deletion.
- Keep evidence-register backups, purge logs, verification logs, and chain-of-custody records.
- Do not describe the two retained November 10 test rows as complete evidence; their associated files were missing during verification.

---

## Learn More

- [APScheduler 3.x documentation](https://apscheduler.readthedocs.io/en/3.x/) — reference material only; a scheduled cleanup service is not claimed as implemented in this project.
- [Python logging documentation](https://docs.python.org/3/library/logging.html)

---

## Authored by: Andrew D'Amico

Date: 2026-11-11  
Validation note: Evidence cleanup is documented from the recorded project tests. 
