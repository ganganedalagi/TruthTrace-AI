import os
import sys
import json
import streamlit as st


# ---------------------------------------
# MODULE PATH
# ---------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODULE_DIR = os.path.join(
    BASE_DIR,
    "module2_module3"
)

if MODULE_DIR not in sys.path:
    sys.path.insert(
        0,
        MODULE_DIR
    )


from module2_module3.main import process_evidence


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Truth Trace AI",
    page_icon="🔎",
    layout="wide"
)


# ---------------------------------------
# HEADER
# ---------------------------------------

st.title("🔎 Truth Trace AI")

st.subheader(
    "AI-Based Digital Forensics Evidence Analysis System"
)

st.write(
    "Securely acquire, hash, compress and "
    "store digital evidence in the cloud."
)


# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.title(
    "Truth Trace AI"
)

st.sidebar.markdown(
    """
### Evidence Pipeline

1. Evidence Upload
2. Evidence Acquisition
3. Metadata Extraction
4. SHA-256 Hash
5. ZIP Compression
6. Secure Cloud Storage
7. Cloud Reference
8. Chain of Custody
9. AI Evidence Analysis
"""
)

st.sidebar.info(
    "Local evidence and ZIP archives are "
    "deleted after successful cloud upload "
    "to reduce disk usage."
)


# ---------------------------------------
# UPLOAD
# ---------------------------------------

st.header(
    "📁 Upload Digital Evidence"
)

uploaded_file = st.file_uploader(
    "Select an evidence file",
    type=None,
    help=(
        "You can upload images, documents, "
        "audio, video, logs or other files."
    )
)


if uploaded_file is not None:

    st.success(
        f"Selected: {uploaded_file.name}"
    )

    # File information
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "File Name",
            uploaded_file.name
        )

    with col2:
        size_mb = (
            uploaded_file.size
            / (1024 * 1024)
        )

        st.metric(
            "File Size",
            f"{size_mb:.2f} MB"
        )

    with col3:
        st.metric(
            "File Type",
            uploaded_file.type or
            "Unknown"
        )

    st.divider()

    process_button = st.button(
        "🚀 Acquire & Secure Evidence",
        type="primary",
        use_container_width=True
    )

    if process_button:

        try:

            with st.spinner(
                "Processing evidence..."
            ):

                result = process_evidence(
                    uploaded_file,
                    delete_local=True
                )

            if result["success"]:

                st.success(
                    "Evidence successfully acquired "
                    "and uploaded to cloud!"
                )

                # --------------------------------
                # EVIDENCE ID
                # --------------------------------

                st.header(
                    "🆔 Evidence Identification"
                )

                st.code(
                    result["evidence_id"]
                )

                # --------------------------------
                # METADATA
                # --------------------------------

                st.header(
                    "📋 Evidence Metadata"
                )

                metadata = result[
                    "metadata"
                ]

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**File Name:**",
                        metadata[
                            "file_name"
                        ]
                    )

                    st.write(
                        "**File Size:**",
                        f"{metadata['file_size_mb']} MB"
                    )

                    st.write(
                        "**MIME Type:**",
                        metadata[
                            "mime_type"
                        ]
                    )

                    st.write(
                        "**Extension:**",
                        metadata[
                            "file_extension"
                        ]
                    )

                with col2:

                    st.write(
                        "**Acquisition Time:**",
                        metadata[
                            "acquisition_time"
                        ]
                    )

                    st.write(
                        "**Created Time:**",
                        metadata[
                            "created_time"
                        ]
                    )

                    st.write(
                        "**Modified Time:**",
                        metadata[
                            "modified_time"
                        ]
                    )

                # --------------------------------
                # SHA-256
                # --------------------------------

                st.header(
                    "🔐 SHA-256 Evidence Hash"
                )

                st.code(
                    metadata["sha256"],
                    language="text"
                )

                st.info(
                    "This SHA-256 value acts as a "
                    "digital fingerprint of the evidence."
                )

                # --------------------------------
                # CLOUD
                # --------------------------------

                st.header(
                    "☁️ Cloud Storage"
                )

                cloud = result[
                    "cloud_reference"
                ]

                st.write(
                    "**Provider:**",
                    cloud["provider"]
                )

                st.write(
                    "**Bucket:**",
                    cloud["bucket"]
                )

                st.write(
                    "**Cloud Path:**",
                    cloud["path"]
                )

                # --------------------------------
                # CHAIN OF CUSTODY
                # --------------------------------

                st.header(
                    "⛓️ Chain of Custody"
                )

                for event in result[
                    "record"
                ]["chain_of_custody"]:

                    st.write(
                        f"**{event['event']}**"
                    )

                    st.write(
                        f"Timestamp: "
                        f"{event['timestamp']}"
                    )

                    if "sha256" in event:

                        st.write(
                            f"SHA-256: "
                            f"`{event['sha256']}`"
                        )

                    if "cloud_path" in event:

                        st.write(
                            f"Cloud Path: "
                            f"`{event['cloud_path']}`"
                        )

                    st.divider()

                # --------------------------------
                # JSON RECORD
                # --------------------------------

                st.header(
                    "📄 Forensic Evidence Record"
                )

                record_json = json.dumps(
                    result["record"],
                    indent=4
                )

                st.download_button(
                    label=(
                        "⬇️ Download Evidence Record"
                    ),
                    data=record_json,
                    file_name=(
                        f"{result['evidence_id']}.json"
                    ),
                    mime="application/json"
                )

                with st.expander(
                    "View Complete JSON Record"
                ):

                    st.json(
                        result["record"]
                    )

                # --------------------------------
                # AI ANALYSIS PLACEHOLDER
                # --------------------------------

                st.header(
                    "🤖 AI Evidence Analysis"
                )

                st.info(
                    "Module 2 and Module 3 are "
                    "complete. AI analysis can now "
                    "process the securely stored evidence."
                )

                st.write(
                    """
                    Future AI processing:

                    • Image analysis
                    • Audio analysis
                    • Video analysis
                    • Document analysis
                    • Anomaly detection
                    • Evidence classification
                    • Evidence prioritization
                    • Explainable AI
                    • Forensic report generation
                    """
                )

        except Exception as error:

            st.error(
                "Evidence processing failed."
            )

            st.exception(error)


# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "Truth Trace AI | Digital Forensics "
    "Evidence Acquisition & Secure Cloud Storage"
)
