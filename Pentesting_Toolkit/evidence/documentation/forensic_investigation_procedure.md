# Forensic Investigation Procedure
## Automated Web Penetration Testing Toolkit

### 1. Purpose

This procedure documents how my Automated Web Penetration Testing Toolkit collects, preserves, verifies, and tracks digital evidence during authorized web application security testing. The purpose is to maintain evidence integrity, support reliable analysis, and establish a repeatable investigation process.

### 2. Scope and Authorization

Testing is conducted only against authorized targets, including my local OWASP Juice Shop lab at `http://127.0.0.1:3000`.

Before testing begins, the following information should be documented:

- Investigation or test ID
- Target application and URL
- Testing objectives
- Authorized testing boundaries
- Date and time testing begins
- Investigator or evidence handler
- Permitted testing methods

Testing must remain within the approved scope. Evidence containing credentials, session tokens, personal data, or other sensitive information must be protected and handled appropriately.

### 3. Initial Response and Preparation

Before collecting evidence, the following steps should be completed:

1. Confirm that the target is authorized and within the approved testing scope.
2. Record the target URL, test purpose, date, time, and investigator.
3. Confirm that the evidence directory and evidence register are available.
4. Identify the test that will generate the evidence.
5. Avoid unnecessarily modifying the target application or existing evidence.
6. Use unique evidence identifiers to distinguish collection events.
7. Record any errors, unexpected behavior, or limitations encountered.

**Justification:** These steps establish the context of the investigation, reduce the risk of collecting evidence from an unauthorized target, and help make the results repeatable.

### 4. Evidence Collection

My toolkit collects HTTP request and response evidence during selected tests. For example, the external redirect check records the request sent to the application and the response received.

For each collection event, the following information should be recorded where available:

- Evidence ID
- Associated test and finding ID
- Target URL
- HTTP method and relevant request parameters
- HTTP response status
- Relevant response headers and response body
- Collection timestamp in UTC
- Evidence filenames
- Evidence handler
- Reason for collection

The toolkit saves request and response information as separate text files in the `evidence/` directory and records the collection in `evidence/evidence_register.csv`.

**Justification:** Preserving request and response information helps the investigator examine the input sent to the application and the resulting behavior. It also provides supporting evidence for findings reported by the toolkit.

### 5. Evidence Preservation and Integrity

After evidence is collected, the following procedures should be followed:

1. Preserve the original evidence files.
2. Calculate the SHA-256 hash of each evidence file.
3. Record the calculated hashes in the evidence register.
4. Recalculate the hashes during subsequent integrity verification.
5. Compare the recalculated hashes with the original recorded values.
6. Document whether each comparison passed or failed.
7. Restrict unnecessary access to evidence files.
8. Perform analysis on copies when practical, retaining the original files unchanged.

A matching SHA-256 hash indicates that the file matches the version previously hashed. It does not independently prove the authenticity of the original collection or establish that the evidence was never modified before the original hash was calculated.

**Justification:** Cryptographic hashes help identify changes to evidence files after a reference hash has been recorded. Preserving original files and documenting verification results improves the reliability and traceability of the investigation.

### 6. Chain of Custody

A chain-of-custody record should document each relevant collection, access, verification, transfer, or handover of evidence.

The record should contain:

- Evidence ID
- Date and time in UTC
- Person handling or releasing the evidence
- Person receiving the evidence, when applicable
- Action performed
- Reason for the action
- Evidence location before and after the action, when applicable
- Integrity verification result, when performed
- Additional notes

For a single-investigator lab investigation, the record should identify the investigator and document the handling activities that actually occurred. Transfers or additional handlers must not be recorded unless they took place.

**Justification:** Chain-of-custody documentation establishes a traceable history of evidence handling and helps identify who handled the evidence, when it was handled, and what actions were performed.

### 7. Evidence Examination and Analysis

Evidence should be analyzed in the context of the test that generated it.

For web application testing, the investigator should:

1. Review the saved HTTP request and response.
2. Examine the response status, headers, body, and redirect destination where relevant.
3. Compare test results with a baseline when appropriate.
4. Distinguish confirmed vulnerabilities from potential indicators and inconclusive results.
5. Record limitations and alternative explanations.
6. Link the analysis to the relevant finding ID when available.
7. Document the reasoning used to reach each conclusion.

An HTTP error, unusual response, or redirect does not by itself prove a vulnerability. Additional validation may be necessary to establish whether a security weakness exists and determine its impact.

**Justification:** Examining evidence in context reduces the risk of false positives and supports conclusions based on observed behavior rather than assumptions.

### 8. Reporting

The investigation report should document:

- Investigation objective and authorization
- Target and testing scope
- Tools and methods used
- Evidence collection and preservation procedures
- Evidence IDs and filenames
- SHA-256 hashes and verification results
- Chain-of-custody records
- Findings and supporting evidence
- Limitations, errors, and unresolved questions
- Conclusions and recommended remediation

The report should distinguish between completed procedures, outstanding work, and planned improvements. Findings should be classified according to the available evidence and the level of validation performed.

### 9. Completion and Storage

At the end of testing, the investigator should:

1. Confirm that collected evidence is listed in the evidence register.
2. Verify the hashes of evidence selected for examination.
3. Review the chain-of-custody records for completeness.
4. Document missing files, failed integrity checks, or other discrepancies.
5. Store evidence and reports in the designated project directory with appropriate access controls.
6. Record the investigation completion date and investigator.
7. Document any outstanding tasks or limitations.

**Justification:** These steps help ensure that the investigation is documented, that evidence discrepancies are visible, and that the results can be reviewed later.

### 10. Limitations

This project demonstrates evidence-handling principles in an authorized cybersecurity lab. The toolkit captures selected web application HTTP requests and responses; it does not perform a complete forensic acquisition of a computer, memory image, disk, or network.

The scope of the evidence is limited to the information captured by the implemented tests. Conclusions depend on the collection method, available evidence, integrity verification, and validation performed. Automated findings may require manual investigation before a vulnerability can be considered confirmed.