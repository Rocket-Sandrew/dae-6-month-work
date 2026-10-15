import csv
from pathlib import Path
import hashlib

# Locate the evidence folder containing this file.
EVIDENCE_DIR = Path(__file__).resolve().parent

# Store the register in the same folder.
REGISTER_FILE = EVIDENCE_DIR / "evidence_register.csv"

def initialize_evidence_storage():
    """Create the evidence folder and register if needed."""

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    if not REGISTER_FILE.exists():
        with REGISTER_FILE.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
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
                "Notes",])


def save_request_response(
    evidence_id,
    request_data,
    response_data,
    test_name="HTTP Request Test",
    url="",
    status_code="",
    notes=""
):
    """Save request/response files and register the evidence."""

    from datetime import datetime, timezone

    initialize_evidence_storage()

    # Avoid overwriting evidence from earlier scans.
    base_evidence_id = evidence_id
    counter = 1

    while (
        (EVIDENCE_DIR / f"{evidence_id}_request.txt").exists()
        or (EVIDENCE_DIR / f"{evidence_id}_response.txt").exists()
        ):
            evidence_id = f"{base_evidence_id}-{counter:03d}"
            counter += 1



    request_file = EVIDENCE_DIR / f"{evidence_id}_request.txt"
    response_file = EVIDENCE_DIR / f"{evidence_id}_response.txt"
    
    # Save request evidence.
    with request_file.open("w", encoding="utf-8") as file:
        file.write(str(request_data))

    # Save response evidence.
    with response_file.open("w", encoding="utf-8") as file:
        file.write(str(response_data))

    # Calculate SHA-256 hashes after saving the files.
    request_hash = calculate_sha256(request_file)
    response_hash = calculate_sha256(response_file)
    combined_hashes = f"{request_hash}; {response_hash}"    
    
    # Add the evidence record to the CSV register.
    timestamp = datetime.now(timezone.utc).isoformat()

    with REGISTER_FILE.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            evidence_id,           # Evidence_ID
            timestamp,             # Timestamp
            test_name,             # Test_ID
            "",                    # Finding_ID (not assigned yet)
            "Request/Response",    # Evidence_Type
            url,                   # Target
            notes,                 # Description
            f"{request_file.name}; {response_file.name}",  # Filename
            combined_hashes,  # SHA256
            "",                    # Collected_By
            "Pending Validation",  # Validation_Status
            "Captured by automated scanner"  # Notes
        ])

    print(f"[+] Request evidence saved: {request_file.name}")
    print(f"[+] Response evidence saved: {response_file.name}")
    print(f"[+] Evidence register updated: {REGISTER_FILE.name}")

    return request_file, response_file

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of an evidence file."""
    sha256 = hashlib.sha256()

    with Path(file_path).open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

if __name__ == "__main__":
    initialize_evidence_storage()
    print(f"[+] Evidence directory: {EVIDENCE_DIR}")
    print(f"[+] Evidence register: {REGISTER_FILE}")

    # save_request_response(
    #     "EV-002",
    #     "GET http://127.0.0.1:3000/\nHost: 127.0.0.1:3000",
    #     "HTTP/1.1 200 OK\nContent-Type: text/html\n\nSample response body",
    #     test_name="Juice Shop GET Test",
    #     url="http://127.0.0.1:3000/",
    #     status_code=200,
    #     notes="Test evidence collection"
    # )
