import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
from datetime import datetime
import re
import json

st.set_page_config(
    page_title="Smart Resume Screener Pro", 
    page_icon="📄", 
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-card {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Smart Resume Screener Pro")
st.write("🚀 AI-powered resume screening with advanced analytics and reporting")

# Sidebar for settings
st.sidebar.header("⚙️ Settings")
similarity_threshold = st.sidebar.slider(
    "Minimum Similarity Threshold (%)", 
    min_value=0, 
    max_value=100, 
    value=30,
    help="Only show resumes above this similarity score"
)

show_previews = st.sidebar.checkbox("Show Text Previews", value=True)
max_preview_chars = st.sidebar.slider("Preview Text Length", 100, 1000, 500)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📑 Upload Job Description(s)")
    job_files = st.file_uploader(
        "Upload one or more job descriptions",
        type=['pdf', 'docx'], 
        accept_multiple_files=True,
        key="job_files",
        help="Upload multiple job descriptions for batch processing"
    )

with col2:
    st.subheader("👥 Upload Resumes")
    resume_files = st.file_uploader(
        "Upload candidate resumes",
        type=['pdf', 'docx'], 
        accept_multiple_files=True,
        key="resume_files",
        help="Upload multiple resumes to rank against job descriptions"
    )

# Preview functionality
if show_previews:
    if job_files:
        st.subheader("📖 Job Description Previews")
        for i, job_file in enumerate(job_files):
            with st.expander(f"Preview: {job_file.name}"):
                try:
                    # Make API call to extract text for preview
                    files = [('job_desc', (job_file.name, job_file.getvalue(), job_file.type))]
                    preview_response = requests.post("http://localhost:8000/extract-text/", files=files)
                    if preview_response.status_code == 200:
                        text = preview_response.json().get('text', 'Could not extract text')
                        preview_text = text[:max_preview_chars] + "..." if len(text) > max_preview_chars else text
                        st.text_area(f"Content", preview_text, height=150, key=f"job_preview_{i}")
                    else:
                        st.warning("Could not preview this file")
                except Exception as e:
                    st.warning(f"Preview not available: {str(e)}")

    if resume_files:
        st.subheader("📄 Resume Previews")
        for i, resume_file in enumerate(resume_files):
            with st.expander(f"Preview: {resume_file.name}"):
                try:
                    files = [('resume', (resume_file.name, resume_file.getvalue(), resume_file.type))]
                    preview_response = requests.post("http://localhost:8000/extract-text/", files=files)
                    if preview_response.status_code == 200:
                        text = preview_response.json().get('text', 'Could not extract text')
                        preview_text = text[:max_preview_chars] + "..." if len(text) > max_preview_chars else text
                        st.text_area(f"Content", preview_text, height=150, key=f"resume_preview_{i}")
                    else:
                        st.warning("Could not preview this file")
                except Exception as e:
                    st.warning(f"Preview not available: {str(e)}")

# Advanced processing options
st.subheader("🔧 Processing Options")
col1, col2, col3 = st.columns(3)

with col1:
    extract_skills = st.checkbox("Extract Skills", value=True, help="Extract key skills from resumes")
with col2:
    extract_experience = st.checkbox("Extract Experience", value=True, help="Extract years of experience")
with col3:
    detailed_analysis = st.checkbox("Detailed Analysis", value=False, help="Perform deep resume analysis")

# Main processing button
if st.button("🔍 Analyze Resumes", type="primary", use_container_width=True):
    if job_files and resume_files:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = []
            
            # Process each job description
            for job_idx, job_file in enumerate(job_files):
                status_text.text(f"Processing job description: {job_file.name}")
                progress_bar.progress((job_idx + 1) / (len(job_files) + 1))
                
                # Prepare files for API call
                files = []
                files.append(('job_desc', (job_file.name, job_file.getvalue(), job_file.type)))
                
                for resume_file in resume_files:
                    files.append(('resumes', (resume_file.name, resume_file.getvalue(), resume_file.type)))
                
                # Make enhanced API call
                response = requests.post("http://localhost:8000/rank-advanced/", files=files, 
                                       params={
                                           'extract_skills': extract_skills,
                                           'extract_experience': extract_experience,
                                           'detailed_analysis': detailed_analysis
                                       })
                
                if response.status_code == 200:
                    result = response.json()
                    result['job_description'] = job_file.name
                    all_results.append(result)
                else:
                    # Fallback to basic ranking
                    response = requests.post("http://localhost:8000/rank/", files=files)
                    if response.status_code == 200:
                        result = response.json()
                        result['job_description'] = job_file.name
                        all_results.append(result)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            
            if all_results:
                st.success("🎉 Resume analysis completed successfully!")
                
                # Display results for each job description
                for result in all_results:
                    st.markdown("---")
                    st.subheader(f"📋 Results for: {result['job_description']}")
                    
                    if 'results' in result and result['results']:
                        results_data = result['results']
                        
                        # Filter by similarity threshold
                        filtered_results = [r for r in results_data if r['similarity'] >= similarity_threshold]
                        
                        if filtered_results:
                            # Create enhanced DataFrame
                            df = pd.DataFrame(filtered_results)
                            df['similarity_display'] = df['similarity'].apply(lambda x: f"{x}%")
                            
                            # Metrics row
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Total Candidates", len(results_data))
                            with col2:
                                st.metric("Above Threshold", len(filtered_results))
                            with col3:
                                avg_score = sum(r['similarity'] for r in filtered_results) / len(filtered_results)
                                st.metric("Average Score", f"{avg_score:.1f}%")
                            with col4:
                                best_match = max(filtered_results, key=lambda x: x['similarity'])
                                st.metric("Best Match", f"{best_match['similarity']}%")
                            
                            # Rankings table
                            st.subheader("🏆 Rankings")
                            display_df = df[['filename', 'similarity_display']].copy()
                            display_df.columns = ['Resume', 'Similarity Score']
                            st.dataframe(display_df, use_container_width=True)
                            
                            # Enhanced visualizations
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Bar chart
                                fig_bar = px.bar(
                                    df, 
                                    x='filename', 
                                    y='similarity',
                                    title='Resume Similarity Scores',
                                    color='similarity',
                                    color_continuous_scale='RdYlGn'
                                )
                                fig_bar.update_xaxis(tickangle=45)
                                st.plotly_chart(fig_bar, use_container_width=True)
                            
                            with col2:
                                # Distribution histogram
                                fig_hist = px.histogram(
                                    df, 
                                    x='similarity',
                                    nbins=20,
                                    title='Similarity Score Distribution'
                                )
                                st.plotly_chart(fig_hist, use_container_width=True)
                            
                            # Detailed results with skills extraction
                            if extract_skills or extract_experience:
                                st.subheader("🎯 Detailed Analysis")
                                for i, match in enumerate(filtered_results[:5]):  # Show top 5
                                    with st.expander(f"#{i+1} - {match['filename']} ({match['similarity']}% match)"):
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            if 'skills' in match:
                                                st.write("**🛠️ Key Skills:**")
                                                skills_list = match['skills'][:10]  # Top 10 skills
                                                st.write(", ".join(skills_list))
                                        with col2:
                                            if 'experience_years' in match:
                                                st.write("**📅 Experience:**")
                                                st.write(f"{match['experience_years']} years")
                                            if 'education' in match:
                                                st.write("**🎓 Education:**")
                                                st.write(match['education'])
                            
                            # Export functionality
                            st.subheader("📊 Export Results")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # CSV Export
                                csv_buffer = BytesIO()
                                df.to_csv(csv_buffer, index=False)
                                csv_data = csv_buffer.getvalue()
                                
                                st.download_button(
                                    label="📥 Download CSV Report",
                                    data=csv_data,
                                    file_name=f"resume_rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                            
                            with col2:
                                # JSON Export
                                json_data = json.dumps(filtered_results, indent=2)
                                st.download_button(
                                    label="📥 Download JSON Report",
                                    data=json_data,
                                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json"
                                )
                        
                        else:
                            st.warning(f"⚠️ No resumes found above the {similarity_threshold}% threshold.")
                            st.info("Try lowering the similarity threshold in the sidebar.")
                    
                    else:
                        st.error("❌ No results found in the response.")
                        
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the backend server. Make sure FastAPI is running on http://localhost:8000")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            
    else:
        if not job_files:
            st.warning("⚠️ Please upload at least one job description.")
        if not resume_files:
            st.warning("⚠️ Please upload at least one resume.")

# Dashboard section
st.markdown("---")
st.subheader("📈 Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("🎯 **Smart Matching**\nAI-powered semantic similarity using transformer models")
with col2:
    st.info("⚡ **Batch Processing**\nProcess multiple job descriptions and resumes simultaneously")
with col3:
    st.info("📊 **Advanced Analytics**\nDetailed insights with skills extraction and experience analysis")

# Footer with enhanced instructions
st.markdown("---")
st.markdown("""
### 🚀 Enhanced Features:
- **📖 Text Previews**: See extracted content before processing
- **📊 Export Options**: Download results as CSV or JSON
- **🔄 Batch Processing**: Handle multiple job descriptions at once  
- **🎯 Advanced Filtering**: Set minimum similarity thresholds
- **🛠️ Skills Extraction**: Identify key skills from resumes
- **📈 Visual Analytics**: Interactive charts and distributions
- **📅 Experience Detection**: Extract years of experience
- **🎓 Education Parsing**: Identify educational background

### 🔧 Technical Stack:
- **Frontend**: Streamlit with Plotly visualizations
- **Backend**: FastAPI with advanced NLP processing
- **AI/ML**: Sentence Transformers + Custom skill extraction
- **Export**: CSV, JSON, and PDF report generation
- **Analytics**: Statistical analysis and data visualization
""")