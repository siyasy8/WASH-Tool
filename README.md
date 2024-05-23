The WASH Tool is a web application that allows users to extract text from selected PDF files, process the text to create a searchable knowledge base, and query this knowledge base using OpenAI's language models. This tool is built using Streamlit, PyPDF2, and LangChain libraries. It requires Python 3.7 or higher and access to an OpenAI API key.

**Key Features**

PDF Text Extraction: Extracts text from PDF files selected by the user.

Text Processing: Splits extracted text into manageable chunks and creates a searchable knowledge base.

Query Interface: Allows users to input questions and receive answers based on the content of the selected PDFs.

OpenAI Integration: Utilizes OpenAI's language models for question answering.

**How to Use the Tool:**

1. Ensure your PDFs are in the specified directory (default is /Users/siyayeolekar/Downloads/output). You can change this path in the code if needed.

2. Run the Streamlit application: 
<code>streamlit run main.py</code>

3. Open the provided URL (usually http://localhost:8501) in your web browser.

4. Select the PDFs you want to query from the list.

5. Extract text from the selected PDFs by clicking on the extraction button.

6. Enter your query in the text input field and get answers based on the content of the PDFs.



