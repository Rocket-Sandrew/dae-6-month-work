# 📘 Mini-Tutorial: Automated Evidence Cleanup and Retention Workflow

_A student-authored tutorial documenting a key integration or concept learned in Semester 5._

---

## ❓ What This Teaches

**In one paragraph, explain the concept, tool, or integration.**  
>What problem does it solve? What kind of project would benefit from using it?

This tutorial demonstrates how to integrate an automated evidence-management workflow into a Python-based web penetration-testing toolkit. The workflow uses Python to audit evidence files, identify old temporary .txt files, preserve registered evidence, and record cleanup activities in a log. The workflow can be scheduled using macOS launchd, or APScheduler allowing routine maintenance to run without manual intervention. This integration helps prevent unnecessary file accumulation while maintaining evidence integrity, traceability, and chain-of-custody requirements. It is useful for cybersecurity projects, digital forensics workflows, and security tools that collect large amounts of test output.

---

## 🎯 Use Case

> What real-world need or job scenario does this apply to?

-   [ ] Backend development
-   [x] Cybersecurity
-   [x] Monitoring / Observability
-   [x] Performance / Testing
-   [ ] Authentication / Authorization
-   [x] DevOps / Deployments
-   [x] Other: Digital forenscis and evidence lifecycle managment

Project application: Python-Based Automated Web Penetration Testing Toolkit.
---

## 🚀 Quick Setup / Install

Show just what’s needed to get started.
Run these commands from the project root on macOS:

```bash
cd ~/Desktop/dae_6month_ad/Pentesting_Toolkit
source automated-web-pentest/bin/activate
python -m pip install "APScheduler<4"
python -m pip show APScheduler
```
The <4 version constraint uses the APScheduler 3.x API shown in this tutorial. Install it inside the project's virtual environment so it does not affect other Python projects.
---

## 🛠️ Step-by-Step Guide

Write the steps clearly and briefly. Use bullet points or numbers.

1. Confirm the cleanup function
This tutorial assumes the project already has evidence/cleanup_workflow.py with a callable cleanup(dry_run=True) function. The cleanup routine should only consider files in a dedicated temporary directory, such as evidence/tmp/, and should protect any filename referenced in evidence_register.csv. Keep the evidence register, reports, request/response captures, logs/chain_of_custody.csv, and logs/verification_log.csv out of the deletion scope.

Before scheduling anything, run the cleanup script manually in dry-run mode and inspect its output. If your current cleanup module uses different function names or arguments, adjust the import and call below to match the actual code.

2. Create evidence/evidence_scheduler.py
```python
"""Run a weekly, non-destructive evidence-cleanup preview."""

import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from cleanup_workflow import cleanup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

scheduler = BlockingScheduler(timezone="America/New_York")


def run_evidence_maintenance():
    """Preview cleanup candidates; do not delete files automatically."""
    logging.info("Starting scheduled evidence-maintenance dry run.")
    cleanup(dry_run=True)
    logging.info("Scheduled dry run finished. Review the output before deletion.")


scheduler.add_job(
    run_evidence_maintenance,
    trigger="cron",
    day_of_week="mon",
    hour=9,
    minute=0,
    id="weekly_evidence_maintenance",
    replace_existing=True,
    max_instances=1,
    coalesce=True,
)

logging.info("Evidence maintenance preview scheduled for Mondays at 09:00.")
scheduler.start()
```
Note: The from cleanup_workflow import cleanup import assumes cleanup_workflow.py is in the same evidence/ directory. If it is stored elsewhere, update the import to match your project structure.

3. Test the scheduler without waiting until Monday
For a quick test, temporarily change the schedule to run every minute:
```python
scheduler.add_job(
    run_evidence_maintenance,
    trigger="interval",
    minutes=1,
    id="weekly_evidence_maintenance_test",
    replace_existing=True,
    max_instances=1,
)
```
Start the scheduler from the project root:

```bash
python evidence/evidence_scheduler.py
```

Leave that terminal process running and watch for the scheduled dry-run messages. Stop it with Ctrl+C, then restore the Monday schedule. The scheduler does not run when the Python process is stopped.

4. Review candidates and apply cleanup manually
After the dry run, inspect the candidate paths and confirm they are genuinely temporary and not required for the assignment or an investigation. Only then run the cleanup workflow's supported apply mode—for example, if the script implements this exact command:

```bash
python evidence/cleanup_workflow.py --apply
```

Do not use this example command unless the script actually supports --apply. Keep deletion manual until the cleanup rules, register protection, and audit logging have been tested.

5. Record validation evidence
For the project report, capture:
- The installed APScheduler version (python -m pip show APScheduler).
- The scheduled job configuration and timestamp of the test.
- Terminal output showing the dry run executed.
- The list of candidate files and the review decision.
- Relevant evidence-register and chain-of-custody checks before and after any approved cleanup.
Do not claim the workflow is validated until you have run these checks in your own environment.
---

## ✅ What You Should See

Describe the working result — terminal output, UI screenshot, etc.

When the scheduler starts, the terminal should indicate that the weekly maintenance preview is scheduled. When the job runs, it should log the start and finish of the dry run and show whatever candidate-file output your cleanup function provides.

Example log messages (illustrative, not captured project output):

```
2026-10-29 09:00:00 INFO Starting scheduled evidence-maintenance dry run.
2026-10-29 09:00:00 INFO Scheduled dry run finished. Review the output before deletion.
```

The key expected behavior is that scheduling a dry run does not delete files. Any deletion should happen only after a human reviews the candidates and invokes a supported apply mode.

You can embed screenshots if helpful:


---

## 💡 Pro Tips / Edge Cases

List 1–2 important reminders:

- Preserve evidence: Never automatically remove registered evidence, reports, hashes, verification logs, or chain-of-custody records. Age alone is not a safe reason to delete a file.

- Dry run first: Keep the scheduled job non-destructive until tests prove the cleanup safeguards work correctly.

- Scheduler uptime: APScheduler's blocking scheduler must remain running. If you want it to start automatically on macOS, configure a launchd job to start the scheduler at login and test its logs. Alternatively, use macOS launchd to run a one-shot cleanup preview on a schedule; in that setup, APScheduler is not necessary.

- Audit trail: Ensure the cleanup routine records the timestamp, file path, action, and outcome. Do not modify or erase the chain-of-custody history as part of routine cleanup.

- Timezone: The example uses America/New_York; change this if the project should follow a different local timezone.

---

## 📚 Learn More

Link to any docs or references you found useful:
- [Workflow learning](https://www.ibm.com/think/topics/workflow)

- [APScheduler documentation](https://apscheduler.readthedocs.io/en/3.x/)

- [APScheduler 3.x user guide](https://apscheduler.readthedocs.io/en/3.x/userguide.html)

- [Python logging documentation](https://docs.python.org/3/library/logging.html)

---

## 👤 Authored by: Andrew D'Amico

🗓️ Date: [2026-10-29]  
🔁 Validated by: [Educator or Peer Name if applicable]
