####################################################################################################
#SkillSiftPro                                                                                      # 
#Author: Majdi M. S. Awad                                                                          #
#Version: 1.0                                                                                      # 
#license: MIT                                                                                      # 
####################################################################################################

import fitz
import docx
from spellchecker import SpellChecker
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# NLTK stopwords resource
nltk.download('stopwords')

# spaCy model for general language understanding
# domain-specific model if available
import spacy
nlp = spacy.load("en_core_web_md")

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    
    # Correct spelling and handle cases where the correction is None
    corrected_text = ' '.join(spell.correction(word) if spell.correction(word) is not None else word for word in words)
    
    return corrected_text

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()

def calculate_similarity_percentage(text1, text2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([text1, text2])
    
    # Calculate cosine similarity between the two vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    
    similarity_percentage = cosine_sim[0][0] * 100
    return similarity_percentage

# List to store CV contents
cv_contents = []

# Prompt user for job description
job_description = input("Enter the job description: ")

# Loop to accept CVs until the user types "done" or reaches the limit
cv_count = 0
while cv_count < 20:
    # Prompt user for CV file path
    cv_path = input("Enter the full file path of your CV (PDF or Word file), or type 'done' to stop: ")

    # Check if the user wants to stop
    if cv_path.lower() == 'done':
        break

    # Check the file format and read the CV content
    if cv_path.lower().endswith('.pdf'):
        cv_content = read_pdf(cv_path)
    elif cv_path.lower().endswith('.docx'):
        cv_content = read_docx(cv_path)
    else:
        print("Unsupported file format. Please provide a valid PDF or Word file path.")
        continue  

    # Correct spelling
    corrected_cv_content = correct_spelling(cv_content)

    # Extract keywords
    cv_keywords = extract_keywords(corrected_cv_content)

    # Calculate similarity using keywords
    similarity_percentage = calculate_similarity_percentage(" ".join(cv_keywords), job_description)
    
    # Display similarity percentage
    print(f"\nSimilarity Percentage for CV {cv_count + 1}: {similarity_percentage:.2f}%")

    # Increment the CV count
    cv_count += 1

####################################################################################################
#SkillSiftPro                                                                                      # 
#Author: Majdi M. S. Awad                                                                          #
#Version: 1.0                                                                                      # 
#license: MIT                                                                                      # 
####################################################################################################
