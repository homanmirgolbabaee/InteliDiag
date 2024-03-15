import anthropic
import base64
import streamlit as st

anthropic_api = st.secrets["anthropic_api"]

def generate_prediction(image_filename):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=anthropic_api,
    )

    # Encode the image as base64
    with open(image_filename, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.1,
        system="you are an expert data analyst and crypto expert. your task is to analyze deeply and extract meaningful information from the input to generate a valid technical report. the report should have a data-driven approach.\nin the report, you have to consider different scenarios with your confidence score of happening for each scenario.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "i have uploaded 1 image of 1 month price chart of  POLDAK DOT crypto current. can you use all your historic information and give your best prediction that where the price of DOT could be in 6 months? add your own feeling at the end."
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }
        ]
    )
    
    return message.content



def summarize_pdf(file_path):
    with open(file_path, "rb") as file:
        content = file.read().decode("utf-8")
        
    # Your logic to summarize the content goes here
    
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=anthropic_api,
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="you are an ai assistant, when the user provides a content your task is to summarize the content and understand key metrics & numbers that the user provides within the content.\nthe user will provide a price prediction report in the <document> tag.\nyou have to give your answer in the following format: \n- scenario A - (Buillish or Consolidation or Bearish) - {Confidence Score} :\n     - {price Range}\n     - {supporting reason}\n\n- scenario B - (Buillish or Consolidation or Bearish) - {Confidence Score} :\n     - {price Range}\n     - {supporting reason}\n\n",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<document>{content}<document>"
                    }
                ]
            }
        ]
    )
    print(message.content)