### SHA-256 Integrity Verification Test

**Evidence ID:** REDIRECT-001

**Test date/time:** 2026-10-19T17:27:48.870600+00:00

**Procedure:** The toolkit recalculated the SHA-256 hashes of the saved HTTP request and response evidence files and compared them against the original hashes recorded in the evidence register.

**Results:**
- `REDIRECT-001_request.txt` — PASS
- `REDIRECT-001_response.txt` — PASS

**Conclusion:** Both files matched their recorded SHA-256 hashes at the time of verification. No hash mismatch was detected.

**Justification:** SHA-256 hash comparison provides a repeatable method for detecting changes to evidence files after their reference hashes have been recorded.

**Limitation:** A successful comparison confirms a match with the recorded hashes; it does not independently prove the authenticity of the original evidence collection.

### Chain-of-Custody Collection Logging Test

**Test date:** October 19, 2026  
**Investigator:** Drew  
**Target:** `http://127.0.0.1:3000`

**Procedure:** Executed the Automated Web Penetration Testing Toolkit against the authorized OWASP Juice Shop lab. Inspected the generated chain-of-custody CSV to confirm that evidence collection events were recorded automatically.

**Results:** The toolkit recorded collection events for the initial GET request, external redirect test, SQL injection baseline test, Boolean-true test, Boolean-false test, and SQL injection error test. Each event included a UTC timestamp, investigator identification, action, reason, source location, destination location, and collection-time hash status.

**Conclusion:** Automatic collection logging is operational for the tested request/response evidence workflows.

**Limitations:** Collection logging does not by itself prove that evidence is authentic or that the log cannot be altered. Additional integrity-failure testing and appropriate access controls are needed to strengthen the evidence-preservation process.

# Forensic Investigation Log

## Investigation Details

- **Project:** Python-Based Automated Web Penetration Testing Toolkit
- **Investigator/handler:** Drew
- **Test environment:** OWASP Juice Shop
- **Target:** `http://127.0.0.1:3000`
- **Date:** October 19, 2026
- **Evidence storage:** `evidence/`
- **Chain-of-custody log:** `evidence/logs/chain_of_custody.csv`

## Activity Log

| Date and time (UTC) | Activity | Evidence / record | Outcome |
|---|---|---|---|
| 2026-10-19 18:04:32 | Collected HTTP request and response evidence for the SQL injection error test | `SQLI-ERROR-003_request.txt`, `SQLI-ERROR-003_response.txt` | Files saved; evidence register and chain-of-custody log updated |
| 2026-10-19 18:08:11 | Verified the SQL injection error test evidence using SHA-256 | `SQLI-ERROR-003` | Both files passed verification |
| 2026-10-19 18:14:13 | Created synthetic evidence for a controlled integrity test | `COC-TEST-001_request.txt`, `COC-TEST-001_response.txt` | Files saved and registered |
| 2026-10-19 18:14:29 | Verified the original synthetic test evidence | `COC-TEST-001` | Both files passed verification |
| 2026-10-19 18:14:52 | Modified the disposable synthetic response file and repeated verification | `COC-TEST-001_response.txt` | Request passed; response failed with `FAIL - HASH MISMATCH` |

## Method and Observations

The evidence manager calculated SHA-256 hashes at collection and recorded them in the evidence register. Subsequent verification recalculated the file hashes and compared them with the recorded reference values.

The SQL injection error test evidence passed verification, indicating that both files matched their recorded reference hashes at the time of the check.

For the controlled tamper-detection test, the synthetic response file was deliberately modified after initial verification. The subsequent verification detected a different SHA-256 hash and reported `FAIL - HASH MISMATCH`. The request file remained unchanged and passed verification.

The verification results were recorded in `evidence/verification_log.csv`, and the corresponding events were appended to `evidence/logs/chain_of_custody.csv`.

## Notes and Limitations

- `COC-TEST-001` is synthetic test evidence, not evidence of an actual HTTP response or vulnerability.
- The deliberate modification was performed only on the disposable test response file.
- A matching hash establishes consistency with the recorded reference hash; it does not independently prove the original evidence's authenticity.
- The CSV logs are records of handling activity but are not inherently tamper-proof.

## Follow-up Actions

- Preserve the original scan evidence without modification.
- Retain the integrity-test results as evidence of control testing.
- Complete the investigation report and document any further handling or validation steps.