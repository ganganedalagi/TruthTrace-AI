import os
import json
import uuid
import shutil
from datetime import datetime, timezone

from .evidence_acquisition import acquire_evidence
from .cloud_storage import compress_and_upload


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

EVIDENCE_DIR = os.path.join(
    BASE_DIR,
    "evidence"
)

ARCHIVES_DIR = os.path.join(
    BASE_DIR,
    "archives"
)

RECORDS_DIR = os.path.join(
    BASE_DIR,
    "records"
)


# Create directories
os.makedirs(EVIDENCE_DIR, exist_ok=True)
os.makedirs(ARCHIVES_DIR, exist_ok=True)
os.makedirs(RECORDS_DIR, exist_ok=True)


def save_uploaded_file(
    uploaded_file,
    destination_path
):
    """
    Save Streamlit uploaded file to disk.
    """

    with open(
        destination_path,
        "wb"
    ) as file:

        while True:

            chunk = uploaded_file.read(
                1024 * 1024
            )

            if not chunk:
                break

            file.write(chunk)


def process_evidence(
    uploaded_file,
    delete_local=True
):
    """
    Complete evidence processing pipeline.

    Module 2:
        Evidence Acquisition
        Metadata
        SHA-256

    Module 3:
        ZIP
        Cloud Upload
        Cloud Reference
        Record
    """

    original_name = uploaded_file.name

    # Generate unique evidence ID
    evidence_id = str(uuid.uuid4())

    # Remove unsafe path components
    safe_name = os.path.basename(
        original_name
    )

    evidence_path = os.path.join(
        EVIDENCE_DIR,
        f"{evidence_id}_{safe_name}"
    )

    zip_filename = (
        f"{evidence_id}.zip"
    )

    zip_path = os.path.join(
        ARCHIVES_DIR,
        zip_filename
    )

    # Save evidence temporarily
    save_uploaded_file(
        uploaded_file,
        evidence_path
    )

    try:

        # -----------------------------
        # MODULE 2
        # -----------------------------

        metadata = acquire_evidence(
            evidence_path
        )

        # -----------------------------
        # MODULE 3
        # -----------------------------

        cloud_path = (
            f"evidence/{evidence_id}/{zip_filename}"
        )

        upload_result = compress_and_upload(
            evidence_path=evidence_path,
            zip_path=zip_path,
            cloud_path=cloud_path
        )

        cloud_reference = upload_result[
            "cloud_reference"
        ]

        # -----------------------------
        # FORENSIC RECORD
        # -----------------------------

        record = {

            "evidence_id": evidence_id,

            "original_filename":
                original_name,

            "acquisition": metadata,

            "compression": {
                "format": "ZIP",
                "archive_name": zip_filename
            },

            "cloud_storage":
                cloud_reference,

            "chain_of_custody": [

                {
                    "event":
                        "Evidence Acquired",

                    "timestamp":
                        datetime.now(
                            timezone.utc
                        ).isoformat(),

                    "sha256":
                        metadata["sha256"]
                },

                {
                    "event":
                        "Evidence Compressed",

                    "timestamp":
                        datetime.now(
                            timezone.utc
                        ).isoformat()
                },

                {
                    "event":
                        "Evidence Uploaded",

                    "timestamp":
                        datetime.now(
                            timezone.utc
                        ).isoformat(),

                    "cloud_path":
                        cloud_path
                }
            ],

            "status": "Cloud Stored"
        }

        # Save JSON record
        record_path = os.path.join(
            RECORDS_DIR,
            f"{evidence_id}.json"
        )

        with open(
            record_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                record,
                file,
                indent=4
            )

        # -----------------------------
        # DELETE LOCAL FILES
        # -----------------------------

        if delete_local:

            if os.path.exists(
                evidence_path
            ):
                os.remove(
                    evidence_path
                )

            if os.path.exists(
                zip_path
            ):
                os.remove(
                    zip_path
                )

        return {
            "success": True,
            "evidence_id": evidence_id,
            "metadata": metadata,
            "cloud_reference":
                cloud_reference,
            "record": record,
            "record_path":
                record_path
        }

    except Exception:

        # Cleanup if processing fails
        if os.path.exists(
            evidence_path
        ):
            os.remove(
                evidence_path
            )

        if os.path.exists(
            zip_path
        ):
            os.remove(
                zip_path
            )

        raise


if __name__ == "__main__":

    print("=" * 60)
    print("TTAI - Evidence Acquisition & Cloud Storage")
    print("=" * 60)

    print(
        "\nModule 2 + Module 3 ready."
    )

    print(
        f"\nEvidence directory: {EVIDENCE_DIR}"
    )

    print(
        f"Archives directory: {ARCHIVES_DIR}"
    )

    print(
        f"Records directory: {RECORDS_DIR}"
    )
