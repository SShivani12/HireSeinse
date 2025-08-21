# 📄 Smart Resume Screener Pro

An advanced AI-powered resume screening tool that ranks resumes against job descriptions using NLP, semantic similarity, and intelligent parsing. Built with FastAPI backend and Streamlit frontend.

## 🚀 Features

### Core Functionality
- **AI-Powered Matching**: Uses state-of-the-art sentence transformers for semantic similarity
- **Multi-format Support**: Handles PDF and DOCX files seamlessly
- **Batch Processing**: Process multiple job descriptions and resumes simultaneously
- **Real-time Analysis**: Fast processing with instant results

### Advanced Analytics
- **Skills Extraction**: Automatically identifies technical and soft skills
- **Experience Detection**: Extracts years of professional experience
- **Education Parsing**: Identifies degrees, certifications, and institutions
- **Visual Dashboard**: Interactive charts and similarity distributions
- **Smart Filtering**: Customizable similarity thresholds

### Professional Features
- **Export Capabilities**: Download results as CSV or JSON reports
- **Text Previews**: Preview extracted content before processing
- **Color-coded Rankings**: Visual indicators for match quality
- **Detailed Insights**: Comprehensive candidate analysis
- **Responsive UI**: Modern, intuitive interface

## 🛠️ Technical Stack

- **Backend**: FastAPI with async processing
- **Frontend**: Streamlit with Plotly visualizations
- **AI/ML**: SentenceTransformers (all-MiniLM-L6-v2 model)
- **NLP**: spaCy for advanced text processing
- **File Processing**: PyMuPDF, python-docx for document parsing
- **Visualization**: Plotly, Matplotlib for interactive charts

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/SShivani12/HireSeinse.git
cd HireSeinse
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
source venv/Scripts/activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Install spaCy language model (optional, for enhanced skill extraction)
python -m spacy download en_core_web_sm
```

### Step 4: Start the Application

**Terminal 1 - Backend:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py
```

## 🎯 Usage

1. **Access the Application**: Navigate to `http://localhost:8501`
2. **Upload Job Description(s)**: Upload one or more job postings (PDF/DOCX)
3. **Upload Resumes**: Upload candidate resumes (PDF/DOCX)
### Advanced Parsing
- **Skills Database**: 100+ technical and soft skills recognition
- **Experience Timeline**: Automatic years of experience calculation
- **Education Detection**: Degree levels, fields of study, institutions
- **Certification Tracking**: Professional certifications and licenses

### Export & Reporting
- **CSV Reports**: Spreadsheet-compatible ranking data
- **JSON Export**: Complete analysis data for further processing
- **Timestamped Files**: Organized exports with date/time stamps

## 🔧 Configuration Options

### Similarity Threshold
Adjust the minimum similarity percentage to filter results (default: 30%)

### Analysis Options
- **Extract Skills**: Identify technical and soft skills
- **Extract Experience**: Calculate years of professional experience
- **Detailed Analysis**: Include education, certifications, and resume structure analysis

### Preview Settings
- **Text Previews**: Toggle document content previews
- **Preview Length**: Customize preview text length (100-1000 characters)

## 🏗️ Project Structure

```
HireSeinse/
├── app/
│   ├── main.py              # FastAPI backend
│   ├── nlp_utils.py         # Core NLP and ranking logic
│   ├── resume_parser.py     # Text extraction from documents
│   ├── advanced_parser.py   # Skills and experience extraction
│   └── test_app.py          # API tests
├── frontend/
│   └── app.py               # Streamlit frontend interface
├── resumes/                 # Sample resume files
├── job_descriptions/        # Sample job description files
├── requirements.txt         # Python dependencies
└── README.MD               # This file
```

## 🧪 Sample Data

The repository includes sample files for testing:
- **Resumes**: `R_FD.pdf`, `Resume_BSF.pdf`
- **Job Descriptions**: `BellaBeat_CL.pdf`, `R_FD.pdf`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
- Check the [API documentation](http://localhost:8000/docs) when running
- Review the sample files for proper format examples
- Ensure all dependencies are installed correctly

## 🎖️ Acknowledgments

- Built with [Sentence Transformers](https://www.sbert.net/) for semantic similarity
- Powered by [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/)
- Uses [spaCy](https://spacy.io/) for advanced NLP processing

---

