import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.MCQsgenerator.utils import read_file, get_table_data
from src.MCQsgenerator.mcqgenerator import generate_evaluate_chain

# Set the Response JSON file path
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'Response.json')

if os.path.exists(json_path):
    with open(json_path, 'r') as file:
        RESPONSE_JSON = json.load(file)
else:
    st.error("Response.json file not found. Please check the file path.")
    RESPONSE_JSON = {}

st.title('MCQs Creator Application with Langchain')

with st.form("user input"):
    uploaded_file = st.file_uploader('Upload PDF or Text File')
    mc_count = st.number_input('Number of MCQs', min_value=3, max_value=50)
    subject = st.text_input('Enter Subject', max_chars=20)
    tone = st.text_input(
        "Complexity Level",
        max_chars=20,
        placeholder="Simple"
    )
    button = st.form_submit_button('Create MCQs')

    if button and uploaded_file is not None:
        with st.spinner('AI is generating MCQs...'):
            try:
                text_content = read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text_content,
                            "number": mc_count,
                            "subject": subject,
                            "tone": tone,
                            "RESPONSE_JSON": json.dumps(RESPONSE_JSON)
                        }
                    )

                # Display token usage information
                st.success(f"Tokens Used: {cb.total_tokens}")

                # Handle AI response
                if isinstance(response, dict):
                    quiz = response.get('quiz', None)

                    if quiz:
                        table_data = get_table_data(quiz)

                        # Validate data and display table
                        if isinstance(table_data, list) and len(table_data) > 0:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            st.text_area(
                                label='Review',
                                value=response.get('review', "")
                            )
                        else:
                            st.error("There is an issue with the table data format.")
                            st.write("AI Quiz Response (Debug):", quiz)
                    else:
                        st.error("Quiz content was not found in the response.")

            except Exception as e:
                st.error("An error occurred in the application.")
                st.exception(e)