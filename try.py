import streamlit as st
import pandas as pd
from jamaibase import JamAI, protocol as p
from tempfile import NamedTemporaryFile
from PIL import Image

# Initialize JamAI client
jamai = JamAI(token="jamai_pat_14fd749c672579a73c16bedbb89128e74436ac4c4341d3cc", project_id="proj_e91a0d1a8de587573d87d334")

# Streamlit page config
st.set_page_config(page_title="AI-Powered ATS", page_icon="📄", layout="wide")

# Title
st.markdown('<h2 style="text-align:center;">AI-Powered Applicant Tracking System</h2>', unsafe_allow_html=True)

# Job Description Input
st.subheader("📌 Enter Job Description:")
job_description = st.text_area("Enter job description for the role", height=150)
st.markdown("---")

# Upload Resume Files
st.subheader("📤 Upload Resumes (JPG, JPEG, PNG)")
uploaded_files = st.file_uploader("Select resume files:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with NamedTemporaryFile(delete=False, suffix=".jpeg") as temp_file:
            image = Image.open(uploaded_file)
            image.convert("RGB").save(temp_file, format="JPEG")
            temp_file_path = temp_file.name

        with st.spinner(f"⏳ Processing {uploaded_file.name}..."):
            try:
                upload_response = jamai.file.upload_file(temp_file_path)
                file_uri = upload_response.uri
                row_data = [{"Job Description": job_description, "Resume": file_uri}]
                completion = jamai.table.add_table_rows("action", p.RowAddRequest(table_id="Resume", data=row_data, stream=False))
                if completion.rows:
                    st.success(f"✅ {uploaded_file.name} uploaded and stored in JamAI Base!")
            except Exception as e:
                st.error(f"❌ Error storing data in JamAI Base: {e}")

st.markdown("---")

# Candidate Evaluation Summary
st.subheader("📊 Candidate Evaluation Summary")

try:
    rows = jamai.table.list_table_rows("action", "Resume")
    if not rows.items:
        st.info("No resumes found. Please upload resumes.")
    else:
        # Extract values correctly and fix Decision field
        def extract_values(row):
            decision_text = row["Decision"]["value"].strip()
            decision = "Rejected" if "Rejected" in decision_text else "Accepted" if "Accepted" in decision_text else "Pending"
            return {
                "Candidate Name": row["Candidate Information"]["value"].strip(),
                "Experience": row["Experience"]["value"].replace("Experience:", "").strip(),
                "Education": row["Education"]["value"].replace("Education:", "").strip(),
                "Skills": row["Skills"]["value"].replace("Skills:", "").strip(),
                "Projects": row["Projects"]["value"].replace("Projects:", "").strip(),
                "Overall Assessment": row["Overall Assessment"]["value"].replace("Overall Assessment:", "").strip(),
                "Decision": decision
            }

        candidate_data = [extract_values(row) for row in rows.items]
        df = pd.DataFrame(candidate_data)

        # Normalize Decision column
        df["Decision"] = df["Decision"].astype(str).str.strip().str.lower()

        # Filters
        st.sidebar.subheader("🔍 Filter Candidates")
        experience_filter = st.sidebar.selectbox("Filter by Experience:", ["All"] + df["Experience"].unique().tolist())
        decision_filter = st.sidebar.selectbox("Filter by Decision:", ["All", "Accepted", "Rejected"])

        # Apply filters
        if experience_filter != "All":
            df = df[df["Experience"] == experience_filter]
        if decision_filter != "All":
            df = df[df["Decision"] == decision_filter.lower()]

        # Sorting
        sort_by = st.sidebar.selectbox("Sort by:", ["Candidate Name", "Experience", "Decision"])
        df = df.sort_values(by=sort_by)

        # Summary Metrics
        total_candidates = len(df)
        accepted_candidates = len(df[df["Decision"] == "accepted"])
        rejected_candidates = len(df[df["Decision"] == "rejected"])
        st.markdown(f"**Total Candidates:** {total_candidates} | **Accepted:** {accepted_candidates} | **Rejected:** {rejected_candidates}")

        # Display Candidates
        for _, row in df.iterrows():
            with st.expander(f"📌 {row['Candidate Name']}"):
                st.write(f"**Experience:** {row['Experience']}")
                st.write(f"**Education:** {row['Education']}")
                st.write(f"**Skills:** {row['Skills']}")
                st.write(f"**Projects:** {row['Projects']}")
                st.write(f"**Overall Assessment:** {row['Overall Assessment']}")
                st.write(f"**Final Decision:** {row['Decision'].capitalize()}")

        # Download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="candidate_report.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"❌ Error fetching data from JamAI Base: {e}")

st.markdown("---")
st.caption("📍 Powered by AI-driven resume screening")
