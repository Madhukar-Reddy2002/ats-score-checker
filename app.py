import re
import streamlit as st
import PyPDF2
import docx
import matplotlib.pyplot as plt

job_roles_keywords = {
    "Data Scientist": {
        "python": 3,
        "pandas": 3,
        "numpy": 2,
        "scikit-learn": 3,
        "matplotlib": 2,
        "seaborn": 2,
        "statistics": 3,
        "machine learning": 5,
        "deep learning": 5,
        "tensorflow": 4,
        "pytorch": 4,
        "data cleaning": 3,
        "data visualization": 3,
        "sql": 3,
        "hypothesis testing": 2,
        "data analysis": 3
    },
    "Data Analyst": {
        "sql": 5,
        "excel": 4,
        "power bi": 4,
        "tableau": 4,
        "data visualization": 4,
        "statistics": 3,
        "python": 3,
        "r": 3,
        "data cleaning": 3,
        "data mining": 3,
        "statistical analysis": 4,
        "dashboard creation": 4,
        "microsoft office": 2,
        "critical thinking": 2
    },
    "Software Engineer": {
        "python": 3,
        "java": 4,
        "c++": 3,
        "html": 2,
        "css": 2,
        "javascript": 4,
        "git": 4,
        "github": 3,
        "agile methodology": 3,
        "object-oriented programming": 4,
        "problem-solving": 4,
        "data structures": 5,
        "algorithms": 5,
        "debugging": 3,
        "version control": 4
    },
    "Frontend Developer": {
        "html": 3,
        "css": 3,
        "javascript": 4,
        "react": 4,
        "angular": 3,
        "vue": 3,
        "bootstrap": 3,
        "jquery": 2,
        "user interface": 4,
        "user experience": 4,
        "responsive design": 4,
        "web accessibility": 3
    },
    "Backend Developer": {
        "python": 3,
        "java": 4,
        "nodejs": 4,
        "php": 3,
        "ruby": 3,
        "sql": 4,
        "nosql": 3,
        "api development": 4,
        "microservices": 4,
        "cloud computing": 3,
        "database management": 4,
        "restful apis": 4
    },
    "Full Stack Developer": {
        "html": 3,
        "css": 3,
        "javascript": 4,
        "python": 3,
        "java": 4,
        "nodejs": 4,
        "sql": 4,
        "nosql": 3,
        "api development": 4,
        "microservices": 4,
        "cloud computing": 3,
        "database management": 4,
        "restful apis": 4,
        "user interface": 4,
        "user experience": 4,
        "responsive design": 4,
        "web accessibility": 3
    },
    "DevOps Engineer": {
        "linux": 3,
        "bash": 3,
        "docker": 4,
        "kubernetes": 4,
        "ansible": 3,
        "terraform": 3,
        "ci/cd pipelines": 4,
        "cloud platforms (aws, gcp, azure)": 4,
        "automation": 3,
        "version control": 4
    },
    "Mobile App Developer": {
        "ios": 3,
        "swift": 4,
        "android": 3,
        "kotlin": 3,
        "flutter": 4,
        "react native": 4,
        "mobile development": 4,
        "app store optimization": 3,
        "ui/ux design": 3
    },
    "UI/UX Designer": {
        "user research": 4,
        "wireframing": 4,
        "prototyping": 4,
        "user testing": 3,
        "figma": 3,
        "adobe xd": 3,
        "design thinking": 4,
        "ux writing": 2,
        "accessibility": 3,
        "responsive design": 3
    },
    "Product Manager": {
        "product development": 4,
        "agile": 3,
        "scrum": 3,
        "user stories": 4,
        "roadmap planning": 4,
        "stakeholder management": 4,
        "market research": 3,
        "a/b testing": 3,
        "data analysis": 4,
        "project management": 4,
        "user experience": 4,
        "strategic thinking": 4
    },
    "Business Analyst": {
        "requirements gathering": 4,
        "process analysis": 4,
        "data analysis": 4,
        "business modeling": 3,
        "stakeholder management": 4,
        "communication skills": 4,
        "problem-solving": 4
    },
    "AI Engineer": {
        "large language models": 5,
        "generative ai": 4,
        "prompt engineering": 4,
        "machine learning": 5,
        "deep learning": 5,
        "natural language processing": 5,
        "computer vision": 4,
        "ai ethics": 4,
        "pytorch": 4,
        "tensorflow": 4,
        "hugging face": 3,
        "mlops": 3,
        "vector databases": 3,
        "ai optimization": 4
    },
    "MLOps Engineer": {
        "machine learning operations": 5,
        "model deployment": 5,
        "model monitoring": 4,
        "feature stores": 4,
        "model versioning": 4,
        "automated pipelines": 4,
        "kubernetes": 4,
        "docker": 4,
        "ci/cd for ml": 4,
        "model governance": 4,
        "ml testing": 3,
        "distributed training": 4
    },
    "Cloud Security Engineer": {
        "cloud security architecture": 4,
        "zero trust": 4,
        "identity management": 4,
        "cloud compliance": 4,
        "security automation": 4,
        "threat detection": 4,
        "incident response": 4,
        "devsecops": 3,
        "cloud native security": 3,
        "security frameworks": 3
    },
    "Sustainability Technology Specialist": {
        "green technology": 4,
        "carbon footprint monitoring": 4,
        "environmental data analysis": 4,
        "sustainability metrics": 4,
        "energy efficiency": 3,
        "environmental compliance": 3,
        "sustainable development": 3,
        "green computing": 3,
        "circular economy technologies": 3
    },
    "Blockchain Developer": {
        "smart contracts": 4,
        "web3": 4,
        "ethereum": 4,
        "solidity": 4,
        "cryptocurrency": 4,
        "defi": 3,
        "blockchain security": 4,
        "distributed systems": 4,
        "consensus mechanisms": 3,
        "tokenization": 3,
        "blockchain frameworks": 3
    },
    "AR/VR Developer": {
        "unity": 4,
        "unreal engine": 4,
        "3d modeling": 4,
        "spatial computing": 4,
        "mixed reality": 3,
        "ar frameworks": 3,
        "vr development": 4,
        "3d user interfaces": 4,
        "motion tracking": 3,
        "immersive experiences": 3,
        "webxr": 3
    },
    "Edge Computing Engineer": {
        "iot": 4,
        "edge devices": 4,
        "distributed systems": 4,
        "real-time processing": 4,
        "embedded systems": 4,
        "edge security": 4,
        "5g technologies": 3,
        "sensor networks": 3,
        "edge analytics": 3,
        "low-latency applications": 4
    },
    "Quantum Computing Engineer": {
        "quantum algorithms": 4,
        "quantum programming": 4,
        "qiskit": 3,
        "cirq": 3,
        "quantum machine learning": 4,
        "quantum cryptography": 4,
        "quantum optimization": 4,
        "quantum error correction": 4,
        "quantum circuits": 3
    },
    "Digital Ethics Officer": {
        "ai ethics": 5,
        "privacy compliance": 4,
        "ethical frameworks": 4,
        "bias detection": 4,
        "responsible ai": 4,
        "digital governance": 4,
        "ethical data use": 4,
        "algorithmic fairness": 4,
        "transparency": 4,
        "accountability": 4
    },
    "Cybersecurity AI Specialist": {
        "ai-powered security": 5,
        "threat detection": 5,
        "automated response": 4,
        "security analytics": 4,
        "behavioral analysis": 4,
        "anomaly detection": 4,
        "ai forensics": 4,
        "predictive security": 4,
        "security automation": 4
    }
}

# Custom CSS for Streamlit app with improved keyword visibility
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #F4F4F9;
        }
        .stApp {
            font-family: Arial, sans-serif;
            color: #333;
        }
        .sidebar .sidebar-content {
            background-color: #273746;
            color: white;
        }
        .stFileUploader {
            background-color: white;
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
        }
        .stButton button {
            background-color: #0073e6;
            color: white;
            border-radius: 10px;
        }
        .stButton button:hover {
            background-color: #005bb5;
            color: white;
        }
        .stProgress {
            height: 20px;
        }
        .matched-keywords {
            color: #28a745; /* Green color for matched keywords */
            font-weight: bold;
        }
        .missing-keywords {
            color: #dc3545; /* Red color for missing keywords */
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

# Function to clean resume text
def clean_resume_text(text):
    cleaned_text = re.sub(r'\W+', ' ', text.lower())
    return cleaned_text

# Function to match keywords and calculate weighted score
def match_keywords(job_role, resume_text):
    job_keywords = job_roles_keywords.get(job_role, {})
    
    matched_keywords = []
    total_weight = 0
    matched_weight = 0
    
    for keyword, weight in job_keywords.items():
        if keyword.lower() in resume_text:
            matched_keywords.append(keyword)
            matched_weight += weight
        total_weight += weight

    return matched_keywords, matched_weight, total_weight

# Function to calculate the ATS score based on matched weights
def calculate_ats_score(matched_weight, total_weight):
    if total_weight == 0:
        return 0
    return (matched_weight / total_weight) * 100

# Function to plot keyword match
def plot_keyword_match(matched_keywords, missing_keywords):
    fig, ax = plt.subplots()
    ax.bar(['Matched', 'Missing'], [len(matched_keywords), len(missing_keywords)], color=['#0073e6', '#e67300'])
    ax.set_ylabel('Number of Keywords')
    ax.set_title('Keyword Match Analysis')
    return fig

# Main function
def main():
    add_custom_css()

    st.title("💼 Resume ATS Score Checker")
    st.markdown("#### Optimize your resume for better job match scores.")
    
    # Sidebar: Select job role
    job_role = st.sidebar.selectbox("Select Job Role", options=list(job_roles_keywords.keys()), help="Select the job role you're applying for.")
    
    st.write("Upload your resume to check its ATS score for the selected job role.")
    resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"], help="Only PDF or DOCX files are supported.")

    if resume_file:
        file_extension = resume_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            resume_text = extract_text_from_pdf(resume_file)
        elif file_extension == 'docx':
            resume_text = extract_text_from_docx(resume_file)
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            return

        cleaned_text = clean_resume_text(resume_text)

        if st.button("Analyze Resume"):
            # Calculate Weighted ATS Score
            matched_keywords, matched_weight, total_weight = match_keywords(job_role, cleaned_text)
            ats_score = calculate_ats_score(matched_weight, total_weight)

            st.subheader("📊 ATS Score Results")
            st.write(f"**ATS Score**: {ats_score:.2f}%")

            # Display Progress Bar
            st.progress(ats_score / 100)

            # Display matched and missing keywords with CSS for visibility
            st.write(f"**Matched Keywords**: <span class='matched-keywords'>{', '.join(matched_keywords)}</span>", unsafe_allow_html=True)
            missing_keywords = set(job_roles_keywords[job_role].keys()) - set(matched_keywords)
            st.write(f"**Missing Keywords**: <span class='missing-keywords'>{', '.join(missing_keywords)}</span>", unsafe_allow_html=True)

            # Keyword match visualization
            st.subheader("🔍 Keyword Match Visualization")
            fig = plot_keyword_match(matched_keywords, missing_keywords)
            st.pyplot(fig)

            # Resume length analysis
            words = cleaned_text.split()
            word_count = len(words)

            # Using columns for better organization
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📄 Resume Length Analysis")
                st.write(f"Your resume contains **{word_count} words**.")
            with col2:
                if word_count < 300:
                    st.warning("Your resume might be too short. Consider adding more relevant information.")
                elif word_count > 700:
                    st.warning("Your resume might be too long. Consider condensing it to highlight key information.")
                else:
                    st.success("Your resume length is within a good range.")
    else:
        st.info("Please upload a resume to begin the analysis.")

if __name__ == "__main__":
    main()