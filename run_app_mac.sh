#!/bin/bash
cd "$(dirname "$0")"

# Check if pip is installed
if ! command -v pip &>/dev/null; then
    echo "pip is not installed. Installing now..."
    # Assume Python3 is installed and get pip
    # This varies by OS, below is a common approach for Unix-like systems
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

echo "pip is installed."

# Install dependencies
# Replace 'requirements.txt' with your actual requirements file if needed
# or specify packages directly
pip install python-dotenv PyPDF2 streamlit langchain langchain-openai langchain-community

# Run Streamlit app
# Replace 'app.py' with the path to your Streamlit script
streamlit run ./main.py
read