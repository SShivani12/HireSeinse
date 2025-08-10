from fastapi import FastAPI, UploadFile, File
from typing import List
import shutil

from app.resume_parser import extract_text
from app.nlp_utils import rank_resumes

app = FastAPI()

@app.post("/rank/")
async def rank_resumes_api(job_desc: UploadFile = File(...), resumes: List[UploadFile] = File(...)):
    # Save job description
    jd_path = f"job_descriptions/{job_desc.filename}"
    with open(jd_path, "wb") as f:
        shutil.copyfileobj(job_desc.file, f)

    # Extract JD text
    jd_text = extract_text(jd_path)

    # Save and extract resumes
    resume_texts = []
    for resume in resumes:
        res_path = f"resumes/{resume.filename}"
        with open(res_path, "wb") as f:
            shutil.copyfileobj(resume.file, f)
        text = extract_text(res_path)
        resume_texts.append((resume.filename, text))

    # Rank resumes
    results = rank_resumes(jd_text, resume_texts)
    return {"results": results}
