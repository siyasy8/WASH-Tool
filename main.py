import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from langchain_community.callbacks import get_openai_callback

load_dotenv()

# Enter your OpenAI API key here
api_key = ''
with open('./API_KEY.txt', 'r') as file:
  api_key = file.read()
#api_key = "enter api key here"

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = api_key

def process_text(text):
    # Split the text into chunks using langchain
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    embeddings = OpenAIEmbeddings()
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    
    return knowledgeBase

def main():
    st.title("Enter query about your PDFs")
    
    # Enter the pathname of your output folder
    pdf_folder = './output' 
    #pdf_folder = 'enter pathname here'

    if not os.path.exists(pdf_folder):
        st.error("The specified folder does not exist.")
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

    if pdf_files:
        selected_pdfs = st.multiselect('Select PDFs to query from the Output folder', pdf_files)
        if selected_pdfs:
            text = ""
            for pdf_file in selected_pdfs:
                st.write(pdf_file[:-4].replace('>', '/').replace('<', '.'))
                pdf_path = os.path.join(pdf_folder, pdf_file)
                try:
                    pdf_reader = PdfReader(pdf_path)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text
                        else:
                            st.warning(f"Could not extract text from page {pdf_reader.pages.index(page)} of {pdf_file}")
                except Exception as e:
                    st.error(f"Error reading {pdf_file}: {e}")

            if text:
                st.write("Text successfully extracted from the selected PDFs.")
                # Create the knowledge base object
                knowledgeBase = process_text(text)
                query = st.text_input('Ask a question to the PDF')
                cancel_button = st.button('Cancel')
                
                if cancel_button:
                    st.stop()
                
                if query:
                    docs = knowledgeBase.similarity_search(query)
                    llm = OpenAI()
                    chain = load_qa_chain(llm, chain_type='stuff')
                    
                    with get_openai_callback() as cost:
                        response = chain.run(input_documents=docs, question=query)
                        print(cost)
                    
                    st.write(response)
                else:
                    st.write("Please enter a query.")
            else:
                st.error("No text could be extracted from the selected PDFs.")
        else:
            st.write("Please select at least one PDF file to query.")
    else:
        st.write("No PDF files found in the specified directory.")

if __name__ == "__main__":
    main()
