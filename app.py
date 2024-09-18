import re
import streamlit as st
import PyPDF2
import docx
import matplotlib.pyplot as plt

# Generalized job roles and keywords
# Example job roles and corresponding keywords
# job_roles_keywords = {
#     "Data Scientist": [
#         "python", "machine learning", "pandas", "scikit-learn", "nlp", "data analysis", "statistics",
#         "deep learning", "tensorflow", "neural networks"
#     ],
#     "Data Analyst": [
#         "sql", "excel", "power bi", "data visualization", "statistics", "python", "r",
#         "data cleaning", "tableau", "dashboard", "reporting"
#     ],
#     "Software Engineer": [
#         "javascript", "react", "node.js", "git", "apis", "python", "java", "c++",
#         "docker", "cloud", "microservices", "agile", "scrum"
#     ],
#     "Web Developer": [
#         "html", "css", "javascript", "react", "vue.js", "node.js", "responsive design",
#         "frontend", "backend", "ui/ux", "bootstrap", "wordpress", "typescript"
#     ],
#     "DevOps Engineer": [
#         "linux", "docker", "kubernetes", "aws", "azure", "ci/cd", "jenkins", "ansible",
#         "infrastructure as code", "terraform", "cloud automation", "bash", "scripting"
#     ],
#     "AI/ML Engineer": [
#         "python", "tensorflow", "pytorch", "scikit-learn", "deep learning", "reinforcement learning",
#         "nlp", "computer vision", "neural networks", "keras", "image processing", "algorithms"
#     ],
#     "Cloud Architect": [
#         "aws", "azure", "google cloud", "cloud architecture", "devops", "cloud security",
#         "virtualization", "containers", "kubernetes", "terraform", "networking", "cloud migration"
#     ],
#     "Cybersecurity Specialist": [
#         "firewalls", "network security", "encryption", "penetration testing", "vulnerability assessment",
#         "incident response", "cloud security", "ethical hacking", "compliance", "malware analysis"
#     ],
#     "Business Analyst": [
#         "business intelligence", "sql", "data analysis", "stakeholder management", "requirements gathering",
#         "reporting", "business process modeling", "kpi", "microsoft office", "agile"
#     ],
#     "Product Manager": [
#         "roadmap", "agile", "scrum", "user stories", "market research", "product lifecycle",
#         "stakeholder management", "prioritization", "ux", "kpi", "mvp", "feature definition"
#     ]
# }
# Expanded job roles and keywords
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
    "Business Analyst": ["requirements gathering", "process analysis", "data analysis", "business modeling", "stakeholder management", "communication skills", "problem-solving"]
}

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
    # Remove special characters, numbers, and extra spaces
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
    ax.bar(['Matched', 'Missing'], [len(matched_keywords), len(missing_keywords)])
    ax.set_ylabel('Number of Keywords')
    ax.set_title('Keyword Match Analysis')
    return fig

def main():
    st.title("Resume ATS Score Checker")

    # Sidebar for job role selection
    job_role = st.sidebar.selectbox("Select Job Role", options=list(job_roles_keywords.keys()))

    # Main content
    st.write("Upload your resume to check its ATS score for the selected job role.")
    resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

    if resume_file:
        file_extension = resume_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            resume_text = extract_text_from_pdf(resume_file)
        elif file_extension == 'docx':
            resume_text = extract_text_from_docx(resume_file)
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            return

        # Clean and display extracted text
        cleaned_text = clean_resume_text(resume_text)
        

        if st.button("Analyze Resume"):
            # Calculate ATS Score
            matched_keywords, matched_count, total_count = match_keywords(job_role, cleaned_text)
            ats_score = calculate_ats_score(matched_count, total_count)

            st.subheader("ATS Score Results")
            st.write(f"**ATS Score**: {ats_score:.2f}%")
            st.write(f"**Matched Keywords**: {', '.join(matched_keywords)}")
            missing_keywords = set(job_roles_keywords[job_role]) - set(matched_keywords)
            st.write(f"**Missing Keywords**: {', '.join(missing_keywords)}")

            # Keyword match visualization
            st.subheader("Keyword Match Visualization")
            fig = plot_keyword_match(matched_keywords, missing_keywords)
            st.pyplot(fig)
                        
            # Resume length analysis
            words = cleaned_text.split()
            st.subheader("Resume Length Analysis")
            word_count = len(words)
            st.write(f"Your resume contains {word_count} words.")
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