import fitz  # PyMuPDF
import google.generativeai as genai
import streamlit as st

# Securely load the API key from Streamlit's secrets dashboard
genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 

# Initialise the free and fast Flash model
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text(pdf_file):
    # Read the PDF directly from the uploaded file stream
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def map_curriculum(syllabus, textbook):
    prompt = f"""
    You are an expert tutor. Cross-reference the syllabus topics with the textbook content below. 
    Output a clear list of chapters and sections from the textbook that cover the syllabus topics.
    
    Syllabus: {syllabus}
    Textbook: {textbook}
    """
    response = model.generate_content(prompt)
    return response.text

# The Web App Interface
st.title("AI Curriculum Mapper")

syllabus_file = st.file_uploader("Upload Syllabus (PDF)", type="pdf")
textbook_file = st.file_uploader("Upload Textbook (PDF)", type="pdf")

if st.button("Analyse") and syllabus_file and textbook_file:
    with st.spinner("Cross-referencing..."):
        # Extract text from the uploaded PDFs
        syllabus_text = extract_text(syllabus_file)
        textbook_text = extract_text(textbook_file)
        
        # Send the text to Gemini for mapping
        results = map_curriculum(syllabus_text, textbook_text)
        
        # Display the final mapped list on the screen
        st.subheader("Your Study Plan")
        st.write(results)