import os
import zipfile
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client


# Load .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_BUCKET = os.getenv(
    "SUPABASE_BUCKET",
    "evidence"
)


def get_supabase_client():

    if not SUPABASE_URL:
        raise ValueError(
            "SUPABASE_URL is missing in .env"
        )

    if not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_KEY is missing in .env"
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )


def create_zip_archive(
    evidence_path,
    zip_path
):
    """
    Compress evidence into a ZIP archive.
    """

    os.makedirs(
        os.path.dirname(zip_path),
        exist_ok=True
    )

    with zipfile.ZipFile(
        zip_path,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        zip_file.write(
            evidence_path,
            arcname=os.path.basename(evidence_path)
        )

    return zip_path


def upload_to_supabase(
    zip_path,
    cloud_path
):
    """
    Upload ZIP archive to Supabase Storage.
    """

    supabase = get_supabase_client()

    with open(zip_path, "rb") as file:
        file_data = file.read()

    response = supabase.storage.from_(
        SUPABASE_BUCKET
    ).upload(
        path=cloud_path,
        file=file_data,
        file_options={
            "content-type": "application/zip",
            "upsert": "false"
        }
    )

    return response


def get_public_url(cloud_path):
    """
    Get public URL.

    This only works if the Supabase bucket is public.
    """

    supabase = get_supabase_client()

    response = supabase.storage.from_(
        SUPABASE_BUCKET
    ).get_public_url(cloud_path)

    return response


def create_signed_url(
    cloud_path,
    expires_in=3600
):
    """
    Generate a temporary signed URL.

    Recommended when the bucket is private.
    """

    supabase = get_supabase_client()

    response = supabase.storage.from_(
        SUPABASE_BUCKET
    ).create_signed_url(
        cloud_path,
        expires_in
    )

    return response


def create_cloud_reference(
    cloud_path,
    bucket=None
):
    """
    Create a structured cloud reference.
    """

    if bucket is None:
        bucket = SUPABASE_BUCKET

    return {
        "provider": "Supabase Storage",
        "bucket": bucket,
        "path": cloud_path,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }


def compress_and_upload(
    evidence_path,
    zip_path,
    cloud_path
):
    """
    Module 3 complete pipeline:

    Evidence
        ↓
    ZIP
        ↓
    Supabase
        ↓
    Cloud Reference
    """

    create_zip_archive(
        evidence_path,
        zip_path
    )

    upload_response = upload_to_supabase(
        zip_path,
        cloud_path
    )

    cloud_reference = create_cloud_reference(
        cloud_path
    )

    return {
        "upload_response": upload_response,
        "cloud_reference": cloud_reference
    }


if __name__ == "__main__":

    print("Cloud Storage Module")
    print("--------------------")

    if SUPABASE_URL:
        print("Supabase URL: configured")
    else:
        print("Supabase URL: NOT configured")

    if SUPABASE_KEY:
        print("Supabase Key: configured")
    else:
        print("Supabase Key: NOT configured")

    print(
        f"Bucket: {SUPABASE_BUCKET}"
    )
