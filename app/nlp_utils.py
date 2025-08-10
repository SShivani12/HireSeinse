from sentence_transformers import SentenceTransformer, util

# Load a lightweight transformer model (fast & accurate)
model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_resumes(job_description, resumes):
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    results = []
    for filename, resume_text in resumes:
        res_embedding = model.encode(resume_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(jd_embedding, res_embedding).item()
        results.append({
            "filename": filename,
            "similarity": round(similarity * 100, 2)  # percentage match
        })

    # Sort by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results
