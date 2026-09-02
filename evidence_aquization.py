import os
import hashlib
import mimetypes
from datetime import datetime, timezone


def calculate_sha256(file_path, chunk_size=1024 * 1024):
    """
    Calculate SHA-256 hash without loading the entire file into RAM.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def extract_metadata(file_path):
    """
    Extract basic forensic metadata from the evidence file.
    """

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        mime_type = "application/octet-stream"

    created_time = os.path.getctime(file_path)
    modified_time = os.path.getmtime(file_path)

    metadata = {
        "file_name": file_name,
        "file_size_bytes": file_size,
        "file_size_mb": round(file_size / (1024 * 1024), 4),
        "mime_type": mime_type,
        "file_extension": os.path.splitext(file_name)[1],
        "created_time": datetime.fromtimestamp(
            created_time, timezone.utc
        ).isoformat(),

        "modified_time": datetime.fromtimestamp(
            modified_time, timezone.utc
        ).isoformat(),

        "acquisition_time": datetime.now(timezone.utc).isoformat(),

        "sha256": calculate_sha256(file_path)
    }

    return metadata


def acquire_evidence(file_path):
    """
    Complete Module 2 evidence acquisition.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Evidence file not found: {file_path}"
        )

    metadata = extract_metadata(file_path)

    return metadata


if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("python evidence_acquisition.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        metadata = acquire_evidence(file_path)

        print("\nEvidence Acquisition Successful")
        print("-" * 50)

        for key, value in metadata.items():
            print(f"{key}: {value}")

    except Exception as error:
        print(f"Error: {error}")
