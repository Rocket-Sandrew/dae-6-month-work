
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path


# Locate the evidence folder containing this file.
EVIDENCE_DIR = Path(__file__).resolve().parent

# Store the evidence register and verification log in evidence/.
REGISTER_FILE = EVIDENCE_DIR / "evidence_register.csv"

# Store the chain-of-custody log in evidence/logs/.
LOG_DIR = EVIDENCE_DIR / "logs"
CHAIN_OF_CUSTODY_FILE = LOG_DIR / "chain_of_custody.csv"
VERIFICATION_LOG = LOG_DIR / "verification_log.csv"

# Replace this with your actual name or investigator ID.
INVESTIGATOR_ID = "Drew"

REGISTER_FIELDS = [
    "Evidence_ID",
    "Timestamp",
    "Test_ID",
    "Finding_ID",
    "Evidence_Type",
    "Target",
    "Description",
    "Filename",
    "SHA256",
    "Collected_By",
    "Validation_Status",
    "Notes",
]

CHAIN_OF_CUSTODY_FIELDS = [
    "Evidence_ID",
    "Timestamp_UTC",
    "Handler",
    "Action",
    "Reason",
    "Source_Location",
    "Destination_Location",
    "SHA256_Verification",
    "Notes",
]

VERIFICATION_FIELDS = [
    "Evidence_ID",
    "Timestamp_UTC",
    "Filename",
    "Expected_SHA256",
    "Actual_SHA256",
    "Result",
]


def utc_timestamp():
    """Return the current time as a UTC ISO 8601 timestamp."""
    return datetime.now(timezone.utc).isoformat()


def initialize_evidence_storage():
    """Create evidence folders and CSV files when needed."""

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not REGISTER_FILE.exists() or REGISTER_FILE.stat().st_size == 0:
        with REGISTER_FILE.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(REGISTER_FIELDS)

    if (
        not CHAIN_OF_CUSTODY_FILE.exists()
        or CHAIN_OF_CUSTODY_FILE.stat().st_size == 0
    ):
        with CHAIN_OF_CUSTODY_FILE.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(CHAIN_OF_CUSTODY_FIELDS)

    if not VERIFICATION_LOG.exists() or VERIFICATION_LOG.stat().st_size == 0:
        with VERIFICATION_LOG.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(VERIFICATION_FIELDS)


def record_chain_of_custody(
    evidence_id,
    handler,
    action,
    reason,
    source_location="",
    destination_location="",
    sha256_verification="Not performed",
    notes="",
):
    """Append one evidence-handling event to the chain-of-custody log."""

    initialize_evidence_storage()

    event = {
        "Evidence_ID": evidence_id,
        "Timestamp_UTC": utc_timestamp(),
        "Handler": handler,
        "Action": action,
        "Reason": reason,
        "Source_Location": source_location,
        "Destination_Location": destination_location,
        "SHA256_Verification": sha256_verification,
        "Notes": notes,
    }

    with CHAIN_OF_CUSTODY_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=CHAIN_OF_CUSTODY_FIELDS
        )
        writer.writerow(event)

    print(
        f"[+] Chain-of-custody event recorded: "
        f"{evidence_id} — {action}"
    )


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""

    sha256 = hashlib.sha256()

    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_registered_evidence_ids():
    """Return every evidence ID already present in the register."""
    if not REGISTER_FILE.exists() or REGISTER_FILE.stat().st_size == 0:
        return set()

    with REGISTER_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        return {
            row["Evidence_ID"].strip()
            for row in reader
            if row.get("Evidence_ID", "").strip()
        }


def get_unique_evidence_id(base_id):
    """Avoid reusing IDs found in either the register or evidence files."""
    registered_ids = get_registered_evidence_ids()
    candidate = base_id
    counter = 1

    while (
        candidate in registered_ids
        or (EVIDENCE_DIR / f"{candidate}_request.txt").exists()
        or (EVIDENCE_DIR / f"{candidate}_response.txt").exists()
    ):
        candidate = f"{base_id}-{counter:03d}"
        counter += 1

    return candidate

def save_request_response(
    evidence_id,
    request_data,
    response_data,
    test_name="HTTP Request Test",
    url="",
    status_code="",
    notes="",
    finding_id =""
):
    """Save request/response files and register the evidence."""

    initialize_evidence_storage()

   
    # Avoid overwriting files or reusing a registered evidence ID.
    evidence_id = get_unique_evidence_id(evidence_id)

    request_file = EVIDENCE_DIR / f"{evidence_id}_request.txt"
    response_file = EVIDENCE_DIR / f"{evidence_id}_response.txt"

    # Save request evidence.
    with request_file.open("w", encoding="utf-8") as file:
        file.write(str(request_data))

    # Save response evidence.
    with response_file.open("w", encoding="utf-8") as file:
        file.write(str(response_data))

    # Calculate hashes after saving the files.
    request_hash = calculate_sha256(request_file)
    response_hash = calculate_sha256(response_file)
    combined_hashes = f"{request_hash}; {response_hash}"

    timestamp = utc_timestamp()

    # Register the evidence.
    with REGISTER_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            evidence_id,
            timestamp,
            test_name,
            finding_id,
            "Request/Response",
            url,
            notes,
            f"{request_file.name}; {response_file.name}",
            combined_hashes,
            INVESTIGATOR_ID,
            "Pending Validation",
            "Captured by automated scanner",
        ])

    print(f"[+] Request evidence saved: {request_file.name}")
    print(f"[+] Response evidence saved: {response_file.name}")
    print(f"[+] Evidence register updated: {REGISTER_FILE.name}")

    # Record the actual collection event after files and register are saved.
    record_chain_of_custody(
        evidence_id=evidence_id,
        handler=INVESTIGATOR_ID,
        action="Evidence collected and registered",
        reason=f"Preserve HTTP evidence from test: {test_name}",
        source_location=url,
        destination_location=str(EVIDENCE_DIR.resolve()),
        sha256_verification="Hashes calculated at collection",
        notes=(
            f"Files: {request_file.name}; {response_file.name}. "
            "Reference hashes recorded in evidence register. "
            f"HTTP status: {status_code}"
        ),
    )

    return request_file, response_file


def verify_evidence(evidence_id):
    """Compare saved evidence files against hashes in the register."""

    initialize_evidence_storage()

    # Find all records matching the requested ID.
    with REGISTER_FILE.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)
        matches = [
            row for row in reader
            if row.get("Evidence_ID", "").strip() == evidence_id
        ]

    if not matches:
        raise ValueError(
            f"Evidence ID not found in register: {evidence_id}"
        )

    if len(matches) > 1:
        raise ValueError(
            f"Evidence ID {evidence_id} has {len(matches)} "
            "register entries. Resolve the duplicate records "
            "before verifying this ID."
        )

    record = matches[0]


    # Filenames and hashes are stored in matching order.
    filenames = [
        name.strip()
        for name in record["Filename"].split(";")
        if name.strip()
    ]
    expected_hashes = [
        value.strip()
        for value in record["SHA256"].split(";")
        if value.strip()
    ]

    if not filenames or len(filenames) != len(expected_hashes):
        raise ValueError(
            f"Missing or mismatched filenames/hashes for {evidence_id}"
        )

    results = []

    for filename, expected_hash in zip(filenames, expected_hashes):
        # Evidence files are expected to be stored in EVIDENCE_DIR.
        file_path = EVIDENCE_DIR / Path(filename).name

        if not file_path.is_file():
            actual_hash = ""
            status = "FAIL - FILE MISSING"
        else:
            actual_hash = calculate_sha256(file_path)
            status = (
                "PASS"
                if actual_hash.lower() == expected_hash.lower()
                else "FAIL - HASH MISMATCH"
            )

        result = {
            "Evidence_ID": evidence_id,
            "Timestamp_UTC": utc_timestamp(),
            "Filename": filename,
            "Expected_SHA256": expected_hash,
            "Actual_SHA256": actual_hash,
            "Result": status,
        }
        results.append(result)

        # Record the actual outcome for this specific file.
        record_chain_of_custody(
            evidence_id=evidence_id,
            handler=INVESTIGATOR_ID,
            action="Evidence integrity verification performed",
            reason="Compare current file hash with the registered reference hash",
            source_location=str(file_path.resolve()),
            destination_location=str(file_path.resolve()),
            sha256_verification=status,
            notes=(
                f"File: {filename}. "
                f"Verification details are in {VERIFICATION_LOG.name}."
            ),
        )

    # Append verification results to the verification log.
    with VERIFICATION_LOG.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=VERIFICATION_FIELDS
        )
        writer.writerows(results)

    # Display results.
    for result in results:
        print(f"\nEvidence ID: {result['Evidence_ID']}")
        print(f"File: {result['Filename']}")
        print(f"Result: {result['Result']}")

    if all(result["Result"] == "PASS" for result in results):
        print("\n[+] All evidence files passed hash verification.")
        return True

    print("\n[!] Evidence verification failed. Investigate the results.")
    return False


if __name__ == "__main__":
    initialize_evidence_storage()
    print(f"[+] Evidence directory: {EVIDENCE_DIR}")
    print(f"[+] Evidence register: {REGISTER_FILE}")
    print(f"[+] Verification log: {VERIFICATION_LOG}")
    print(f"[+] Chain-of-custody log: {CHAIN_OF_CUSTODY_FILE}")
