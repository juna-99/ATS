import streamlit as st
import pandas as pd
from jamaibase import JamAI, protocol as p
from tempfile import NamedTemporaryFile
from PIL import Image

# Initialize JamAI client
jamai = JamAI(token="jamai_pat_14fd749c672579a73c16bedbb89128e74436ac4c4341d3cc", project_id="proj_e91a0d1a8de587573d87d334")

# Streamlit page config
st.set_page_config(page_title="AI-Powered Applicant Tracking System", page_icon="📄", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .title { text-align: center; font-size: 32px; font-weight: bold; }
        .big-font { font-size:24px !important; font-weight: bold; }
        .stDataFrame { border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9; }
        .stDataFrame table tbody tr { height: 50px !important; }
    </style>
""", unsafe_allow_html=True)

# **Title**
st.markdown('<p class="title">AI-Powered Applicant Tracking System</p>', unsafe_allow_html=True)

# **1️⃣ Job Description Input**
st.markdown('<p class="big-font">📌 Enter Job Description:</p>', unsafe_allow_html=True)
job_description = st.text_area("Enter job description for the role", height=150)
st.markdown("---")

# **2️⃣ Upload Resume Files**
st.markdown('<p class="big-font">📤 Upload Resumes (JPG, JPEG, PNG)</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("Select resume files:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# **Process New Uploads and Store in JamAI**
if uploaded_files:
    for uploaded_file in uploaded_files:
        with NamedTemporaryFile(delete=False, suffix=".jpeg") as temp_file:
            image = Image.open(uploaded_file)
            image.convert("RGB").save(temp_file, format="JPEG")
            temp_file_path = temp_file.name

        with st.spinner(f"⏳ Processing {uploaded_file.name}..."):
            try:
                # Upload to JamAI Base
                upload_response = jamai.file.upload_file(temp_file_path)
                file_uri = upload_response.uri  # Store URI

                # Insert into JamAI Base
                row_data = [{
                    "Job Description": job_description,
                    "Resume": file_uri
                }]

                # Add data to JamAI Table
                completion = jamai.table.add_table_rows(
                    "action",
                    p.RowAddRequest(
                        table_id="Resume",
                        data=row_data,
                        stream=False,
                    ),
                )

                if completion.rows:
                    st.success(f"✅ {uploaded_file.name} uploaded and stored in JamAI Base!")
                else:
                    st.error("⚠️ Failed to store resume in JamAI Base.")

            except Exception as e:
                st.error(f"❌ Error storing data in JamAI Base: {e}")

st.markdown("---")

# **3️⃣ Display Processed Resumes**
st.markdown('<p class="big-font">📊 Candidate Evaluation Summary</p>', unsafe_allow_html=True)

# Fetch latest resumes from JamAI
try:
    rows = jamai.table.list_table_rows("action", "Resume")

    if not rows.items:
        st.info("No resumes found. Please upload resumes.")
    else:
        # **Extract & Format Data**
        data = []
        for row in rows.items:
            data.append([
                row.get("Candidate Information", {}).get("value", "Unknown"),
                row.get("Experience", {}).get("value", "N/A"),
                row.get("Education", {}).get("value", "N/A"),
                row.get("Skills", {}).get("value", "N/A"),
                row.get("Projects", {}).get("value", "N/A"),
                row.get("Overall Assessment", {}).get("value", "N/A"),
                row.get("Decision", {}).get("value", "Pending"),
            ])

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=[
            "Candidate Name", "Experience", "Education", "Skills", "Projects", "Overall Assessment", "Final Decision"
        ])
        
        # Display DataFrame
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error fetching data from JamAI Base: {e}")

st.markdown("---")
st.caption("📍 Powered by AI-driven resume screening")
