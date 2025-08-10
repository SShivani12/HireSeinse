import streamlit as st
import requests
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Resume Screener", layout="centered")

st.markdown("<h1 style='text-align: center;'>📄 Smart Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a job description and resumes to find the best matches.</p>", unsafe_allow_html=True)

with st.form("upload_form"):
    job_desc_file = st.file_uploader("📑 Upload Job Description (.pdf or .docx)", type=["pdf", "docx"])
    resume_files = st.file_uploader("👥 Upload Resume(s) (.pdf or .docx)", type=["pdf", "docx"], accept_multiple_files=True)
    submitted = st.form_submit_button("🔍 Rank Resumes")

if submitted:
    if not job_desc_file or not resume_files:
        st.warning("Please upload both a job description and at least one resume.")
    else:
        with st.spinner("Processing..."):
            upload_files = [("job_desc", (job_desc_file.name, job_desc_file, job_desc_file.type))]
            for resume in resume_files:
                upload_files.append(("resumes", (resume.name, resume, resume.type)))

            response = requests.post("http://127.0.0.1:8000/rank/", files=upload_files)

        # Preview Job Description text
        with st.expander("📑 Preview Job Description Text"):
            try:
                job_desc_text = job_desc_file.read().decode("utf-8")
            except:
                job_desc_file.seek(0)
                job_desc_text = job_desc_file.read().decode("latin1")
            job_desc_file.seek(0)
            st.text(job_desc_text[:2000])

        # Preview Resumes text
        with st.expander("📄 Preview Resumes Text"):
            for resume in resume_files:
                st.markdown(f"**{resume.name}**")
                try:
                    resume_text = resume.read().decode("utf-8")
                except:
                    resume.seek(0)
                    resume_text = resume.read().decode("latin1")
                resume.seek(0)
                st.text(resume_text[:1000])

        if response.status_code == 200:
            results = response.json()["results"]
            df = pd.DataFrame(results)
            st.success("✅ Resume ranking complete!")
            st.markdown("### 🏆 Top Matching Resumes:")
            st.table(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV Results",
                data=csv,
                file_name="resume_rankings.csv",
                mime="text/csv"
            )

            # Job Description word cloud
            with st.expander("☁️ Job Description Word Cloud"):
                wordcloud = WordCloud(width=600, height=400, background_color="white").generate(job_desc_text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)

            # Resumes word clouds
            with st.expander("☁️ Resumes Word Clouds"):
                for resume in resume_files:
                    try:
                        text = resume.read().decode("utf-8")
                    except:
                        resume.seek(0)
                        text = resume.read().decode("latin1")
                    resume.seek(0)
                    st.markdown(f"**{resume.name}**")
                    wc = WordCloud(width=600, height=400, background_color="white").generate(text)
                    fig, ax = plt.subplots()
                    ax.imshow(wc, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
        else:
            st.error(f"❌ Failed to get response from backend. Status code: {response.status_code}")
