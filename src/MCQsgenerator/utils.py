import os
import pypdf
import json
import traceback
import re

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_read = pypdf.PdfReader(file)
            text = ""
            for page in pdf_read.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise Exception("Error reading the PDF file") from e

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("Unsupported file format. Only PDF and TXT files are supported")


def get_table_data(quiz):
    try:
        # Step 1: If quiz is a string, extract JSON content from it
        if isinstance(quiz, str):
            # Use regex to extract JSON data between { ... }
            json_match = re.search(r'\{.*\}', quiz, re.DOTALL)
            if json_match:
                quiz_str = json_match.group()
                quiz_dict = json.loads(quiz_str)
            else:
                return []  # Return empty list if no JSON is found
        else:
            quiz_dict = quiz

        quiz_table_data = []

        # Step 2: Extract data from dictionary and convert it into a list
        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "N/A")
            options_dict = value.get("options", {})
            options = " | ".join(
                [f"{opt}: {val}" for opt, val in options_dict.items()]
            )
            correct = value.get("correct", "N/A")

            quiz_table_data.append({
                "MCQ": mcq,
                "Choice": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return []