import re
import streamlit as st
import PyPDF2
import docx
import matplotlib.pyplot as plt


job_roles_keywords = {
    "Data Scientist": ["python", "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "statistics", "machine learning", "deep learning", "tensorflow", "pytorch", "data cleaning", "data visualization", "sql", "hypothesis testing", "data analysis"],
    
    "Data Analyst": ["sql", "excel", "power bi", "tableau", "data visualization", "statistics", "python", "r", "data cleaning", "data mining", "statistical analysis", "dashboard creation", "microsoft office", "critical thinking"],
    
    "Software Engineer": ["python", "javascript", "java", "c++", "html", "css", "git", "github", "agile methodology", "object-oriented programming", "problem-solving", "data structures", "algorithms", "debugging", "version control"],
    
    "Frontend Developer": ["html", "css", "javascript", "react", "angular", "vue", "bootstrap", "jquery", "user interface", "user experience", "responsive design", "web accessibility"],
    
    "Backend Developer": ["python", "java", "nodejs", "php", "ruby", "sql", "nosql", "api development", "microservices", "cloud computing", "database management", "restful apis"],
    
    "Full Stack Developer": ["html", "css", "javascript", "python", "java", "nodejs", "sql", "nosql", "api development", "microservices", "cloud computing", "database management", "restful apis", "user interface", "user experience", "responsive design", "web accessibility"],
    
    "DevOps Engineer": ["linux", "bash", "docker", "kubernetes", "ansible", "terraform", "ci/cd pipelines", "cloud platforms (aws, gcp, azure)", "automation", "version control"],
    
    "Mobile App Developer": ["ios", "swift", "android", "kotlin", "flutter", "react native", "mobile development", "app store optimization", "ui/ux design"],
    
    "UI/UX Designer": ["user research", "wireframing", "prototyping", "user testing", "figma", "adobe xd", "design thinking", "ux writing", "accessibility", "responsive design"],
    
    "Product Manager": ["product development", "agile", "scrum", "user stories", "roadmap planning", "stakeholder management", "market research", "a/b testing", "data analysis", "project management", "user experience", "strategic thinking"],
    
    "Business Analyst": ["requirements gathering", "process analysis", "data analysis", "business modeling", "stakeholder management", "communication skills", "problem-solving"],
    "AI Engineer": ["large language models", "generative ai", "prompt engineering", "machine learning", "deep learning", "natural language processing", "computer vision", "ai ethics", "pytorch", "tensorflow", "hugging face", "mlops", "vector databases", "ai optimization"],
    
    "MLOps Engineer": ["machine learning operations", "model deployment", "model monitoring", "feature stores", "model versioning", "automated pipelines", "kubernetes", "docker", "ci/cd for ml", "model governance", "ml testing", "distributed training"],
    
    "Cloud Security Engineer": ["cloud security architecture", "zero trust", "identity management", "cloud compliance", "security automation", "threat detection", "incident response", "devsecops", "cloud native security", "security frameworks"],
    
    "Sustainability Technology Specialist": ["green technology", "carbon footprint monitoring", "environmental data analysis", "sustainability metrics", "energy efficiency", "environmental compliance", "sustainable development", "green computing", "circular economy technologies"],
    
    "Blockchain Developer": ["smart contracts", "web3", "ethereum", "solidity", "cryptocurrency", "defi", "blockchain security", "distributed systems", "consensus mechanisms", "tokenization", "blockchain frameworks"],
    
    "AR/VR Developer": ["unity", "unreal engine", "3d modeling", "spatial computing", "mixed reality", "ar frameworks", "vr development", "3d user interfaces", "motion tracking", "immersive experiences", "webxr"],
    
    "Edge Computing Engineer": ["iot", "edge devices", "distributed systems", "real-time processing", "embedded systems", "edge security", "5g technologies", "sensor networks", "edge analytics", "low-latency applications"],
    
    "Quantum Computing Engineer": ["quantum algorithms", "quantum programming", "qiskit", "cirq", "quantum machine learning", "quantum cryptography", "quantum optimization", "quantum error correction", "quantum circuits"],
    
    "Digital Ethics Officer": ["ai ethics", "privacy compliance", "ethical frameworks", "bias detection", "responsible ai", "digital governance", "ethical data use", "algorithmic fairness", "transparency", "accountability"],
    
    "Cybersecurity AI Specialist": ["ai-powered security", "threat detection", "automated response", "security analytics", "behavioral analysis", "anomaly detection", "ai forensics", "predictive security", "security automation"]
}
# Apply custom CSS to enhance UI
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
        </style>
        """,
        unsafe_allow_html=True
    )

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def clean_resume_text(text):
    cleaned_text = re.sub(r'\W+', ' ', text.lower())
    return cleaned_text

def match_keywords(job_role, resume_text):
    job_keywords = job_roles_keywords.get(job_role, [])
    matched_keywords = [word for word in job_keywords if word.lower() in resume_text]
    return matched_keywords, len(matched_keywords), len(job_keywords)

def calculate_ats_score(matched_count, total_count):
    if total_count == 0:
        return 0
    return (matched_count / total_count) * 100

def plot_keyword_match(matched_keywords, missing_keywords):
    fig, ax = plt.subplots()
    ax.bar(['Matched', 'Missing'], [len(matched_keywords), len(missing_keywords)], color=['#0073e6', '#e67300'])
    ax.set_ylabel('Number of Keywords')
    ax.set_title('Keyword Match Analysis')
    return fig

def main():
    add_custom_css()  # Apply CSS

    st.title("💼 Resume ATS Score Checker")
    st.markdown("#### Optimize your resume for better job match scores.")

    # Sidebar for job role selection
    job_role = st.sidebar.selectbox("Select Job Role", options=list(job_roles_keywords.keys()), help="Select the job role you're applying for.")

    # Main content
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
            # Calculate ATS Score
            matched_keywords, matched_count, total_count = match_keywords(job_role, cleaned_text)
            ats_score = calculate_ats_score(matched_count, total_count)

            st.subheader("📊 ATS Score Results")
            st.write(f"**ATS Score**: {ats_score:.2f}%")

            # Display Progress Bar
            st.progress(ats_score / 100)

            # Display matched and missing keywords
            st.write(f"**Matched Keywords**: {', '.join(matched_keywords)}")
            missing_keywords = set(job_roles_keywords[job_role]) - set(matched_keywords)
            st.write(f"**Missing Keywords**: {', '.join(missing_keywords)}")

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