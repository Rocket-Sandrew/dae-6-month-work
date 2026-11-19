# Forensic Investigation Report

## 1. Executive Summary

The evidence-handling and integrity-verification functionality of the Python-Based Automated Web Penetration Testing Toolkit was tested on October 19, 2026, using the local OWASP Juice Shop lab environment.

The evidence manager successfully saved HTTP request and response files, registered their SHA-256 hashes, recorded chain-of-custody events, and verified evidence against its registered hashes.

A controlled test using synthetic evidence also demonstrated detection of a modified response file.

## 2. Scope

This investigation evaluated the toolkit's handling of web assessment evidence. It did not constitute a full disk, memory, or enterprise forensic investigation.

## 3. Evidence and Results

### Test A: Scan Evidence Integrity

**Evidence ID:** `SQLI-ERROR-003`

Files examined:

- `SQLI-ERROR-003_request.txt`
- `SQLI-ERROR-003_response.txt`

Both files returned `PASS` during SHA-256 verification. Their current hashes matched the reference hashes recorded in the evidence register.

The associated verification events were recorded in the chain-of-custody log.

### Test B: Controlled Tamper Detection

**Evidence ID:** `COC-TEST-001`

The synthetic request and response files initially passed verification. The response file was then deliberately modified by appending test text.

On subsequent verification:

- Request file: `PASS`
- Response file: `FAIL - HASH MISMATCH`

The verification log recorded the original and recalculated hashes, and the chain-of-custody log recorded the verification outcomes.

This result demonstrates that the toolkit can detect a file change relative to its registered reference hash.

## 4. Evidence Handling

The evidence manager maintains the following records:

- `evidence/evidence_register.csv` — evidence metadata and reference hashes.
- `evidence/verification_log.csv` — expected hashes, actual hashes, and verification results.
- `evidence/logs/chain_of_custody.csv` — timestamped handling and verification events.

## 5. Limitations

SHA-256 verification detects changes relative to a stored reference hash. It does not independently establish evidence authenticity or prevent an individual with sufficient access from changing both evidence and its records.

The chain-of-custody logs are CSV files and are not inherently tamper-proof. Additional protections, such as restricted write permissions, protected backups, and independently stored audit records, would strengthen the process.

The controlled test used synthetic data and demonstrates integrity-checking behavior, not the authenticity of real-world forensic evidence.

## 6. Conclusion

The tests successfully demonstrated evidence collection, hash registration, successful integrity verification, chain-of-custody logging, and detection of a modified evidence file.

The evidence integrity-checking component can be considered functionally tested based on these results. Completion of the broader forensic investigation requirement also depends on maintaining the documented procedure, recording actual investigation activities, and completing the required reporting and preservation steps.