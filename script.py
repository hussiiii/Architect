from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os 

load_dotenv()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Define a simple Document class with metadata
class Document:
    def __init__(self, page_content, metadata={}):
        self.page_content = page_content
        self.metadata = metadata

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

# Extract text from PDF
pdf_text = extract_text_from_pdf("context_data.pdf")

# Initialize the embedding model with API key
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Wrap the extracted text from PDF in Document objects
documents = [Document(page_content=pdf_text)]

# Split the text into smaller chunks/documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500)
documents = text_splitter.split_documents(documents)

# Build the FAISS index
vector_store = FAISS.from_documents(documents, embeddings)

# Initialize the Chat model with the API key
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Create the prompt and document chain
prompt = ChatPromptTemplate.from_template("""I am making a map in minecraft that has a mod called CustomNPCS, and this mod allows me to add scripts to things like blocks, players, entities, etc. to make some really cool stuff. View the context for some working examples of scripts so you can see how it works. Each script in the context begins with a comment explaining what it does. I'm going to now ask you to help me create a simple script from scratch. 

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

# Create a retriever from the vector store
retriever = vector_store.as_retriever()

# Create the retrieval chain
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json['question']
    response = retrieval_chain.invoke({"input": question})
    
    # Check if the response is a Document and convert to a dictionary if so
    if isinstance(response, Document):
        response = {
            'answer': response.page_content,
            'metadata': response.metadata
        }
    elif not isinstance(response, dict) or 'answer' not in response:
        # If response is not a Document and does not have 'answer' key, wrap it in a dictionary
        response = {
            'answer': str(response)
        }
    
    # Extract the 'answer' from the response to send to the frontend
    answer = response.get('answer', 'No answer provided by the AI.')
    
    # Send only the 'answer' part to the frontend
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(port=5000)
