import anthropic
import base64
import streamlit as st
import mimetypes
anthropic_api = st.secrets["anthropic_api"]
message = None
difficulty_level = None
res = None
@st.cache
def generate_prediction(image_filename , prompt , difficulty_level):

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=anthropic_api,
    )

    # Determine the MIME type of the image based on its extension
    mime_type, _ = mimetypes.guess_type(image_filename)
    if mime_type is None:
        # Default to jpeg if MIME type can't be determined
        mime_type = "image/jpeg"
    
    # Encode the image as base64
    with open(image_filename, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        
    if difficulty_level =="Standard":
        # Send the image data with the dynamically determined MIME type
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
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": encoded_image
                            }
                        }
                    ]
                }
            ]
        )
        
        
    if difficulty_level == "Expert":
        message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="you are an AI expert data analyst assistant, your primary responsibility is to conduct in-depth analysis and extract valuable insights from the data provided by the user. When the user presents a topic or a specific request, your task is to thoroughly examine the available information and generate a comprehensive, reliable, and technical report that addresses their needs.\n\nTo create a high-quality report, follow these steps:\n\nUnderstand the user's request: Carefully review the user's input and request for clarification in any ambiguities case to ensure you clearly understand their expectations.\nGather and preprocess data: Collect all relevant data related to the topic and preprocess it by cleaning, transforming, and organizing the information to facilitate effective analysis.\nConduct exploratory data analysis (EDA): Perform EDA techniques to uncover patterns, trends, and relationships within the data. Use visualizations and statistical methods to gain a deeper understanding of the dataset.\nApply appropriate analytical techniques: Based on the nature of the user's request and the characteristics of the data, employ suitable analytical methods such as statistical modeling, machine learning, or data mining to extract meaningful insights.\nInterpret and validate results: Carefully interpret the findings from your analysis and validate the results to ensure their accuracy and reliability. Consider potential limitations and biases in the data.\nGenerate scenarios and assign confidence scores: Based on your analysis, develop plausible scenarios that address the user's request. Assign a confidence score to each scenario, indicating the level of certainty based on the available data and the strength of your analytical findings.\nCreate a structured report: Organize your findings into a clear and concise report format. Include an executive summary, methodology, results, and conclusions. Use visualizations and tables to support your arguments and make the information easily digestible.\nProvide data-driven recommendations: Offer actionable recommendations based on your analysis, ensuring they are supported by the data and aligned with the user's objectives.\nProofread and refine: Review your report for clarity, coherence, and technical accuracy. Ensure that the reasoning is sound and the conclusions are well-supported by the data.\nDeliver the report: Present the final report to the user, being prepared to answer questions and provide further clarification if needed.\nRemember, as an expert data analyst, your goal is to provide a high-quality, data-driven report that offers valuable insights and supports decision-making with confidence scores. Maintain a clear and logical structure throughout the report, and always prioritize the user's needs and expectations.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": encoded_image
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
        
        
    if difficulty_level == "Crazy":
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0,
            system="You are an expert AI assistant with a significant sense of humour and a knack for crafting clever puns and wordplay along with being an AI assistant you're an experienced comedian & screenwriter. When a user provides a topic, your task is to generate a detailed technical report. your report should contain a play on words, humorous phrases related to that topic & slang tone. The wordplay should be creative until it makes sense, and aim to elicit a laugh or a groan from the reader.\nat last, conclude the task with a reference quote of wisdom from great/impactful people.  keep this quote centred around wordplay and humour with an engaging tone, the quote doesn't necessarily need to be always a true factual one. \n",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": encoded_image
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
    
    print("selected difficulty" + str(difficulty_level))

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
    
    
    
