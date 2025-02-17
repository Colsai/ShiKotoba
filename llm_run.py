import openai
import os
import configparser
import chromadb
from chromadb.utils import embedding_functions
import json

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load configuration from ini file
config = configparser.ConfigParser()
config.read("config.ini")

# Extract OpenAI model parameters
model = config["openai"].get("model", "gpt-4-turbo")
max_tokens = config["openai"].getint("max_tokens", 1000)
temperature = config["openai"].getfloat("temperature", 0.7)

# Get resume folder path
resume_folder = config["files"].get("resume_folder", "documents")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./resume_db")  # Persistent storage
embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
collection = chroma_client.get_or_create_collection(name="resumes", embedding_function=embedding_function)

#Load resumes into main 
def load_resumes():
    """Reads all text documents from the 'documents' folder and adds them to the database."""
    resume_files = [f for f in os.listdir(resume_folder) if f.endswith(".txt") or f.endswith(".docx")]
    for resume_file in resume_files:
        file_path = os.path.join(resume_folder, resume_file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            collection.add(documents=[text], ids=[resume_file])
    print(f"Loaded {len(resume_files)} resumes into ChromaDB.")


def find_best_resume(job_description):
    """Finds the most relevant resume based on job description using ChromaDB similarity search."""
    results = collection.query(query_texts=[job_description], n_results=1)
    if results["documents"]:
        best_resume = results["documents"][0][0]  # Retrieve best-matching resume
        return best_resume
    return None


def generate_resume(job_description):
    """Creates a tailored resume based on a job description."""
    best_resume = find_best_resume(job_description)
    if not best_resume:
        return "No resumes found. Please add a resume to the 'documents' folder."

    prompt = f"""
    Given the job description below, tailor the resume content to emphasize relevant skills and experience.

    Job Description:
    {job_description}

    Current Resume:
    {best_resume}

    Please rewrite the resume to be highly relevant to the job posting while maintaining professionalism.
    """

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are an expert resume writer helping job seekers."},
                      {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    # Load resumes on startup
    load_resumes()

    # Example Job Description
    job_description = """
    We are looking for a Data Analyst proficient in Python, SQL, and Power BI.
    Experience with geospatial tools and Microsoft Power Automate is a plus.
    """

    # Generate a tailored resume
    updated_resume = generate_resume(job_description)
    print("\nGenerated Resume:\n", updated_resume)