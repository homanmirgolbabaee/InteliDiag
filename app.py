import datetime
import streamlit as st
from PIL import Image
from fpdf import FPDF
# Assuming generate_prediction and summarize_pdf are defined in predictor.py
from predictor import generate_prediction
import time
from streamlit_lightweight_charts import renderLightweightCharts
import os

# Function to visualize data
def visualize_data():
    st.title("📈 Visualize Data")
    chart_type = st.selectbox("Select Chart Type", ["Line", "Area", "Bar", "Candlestick", "Histogram", "Baseline"])

    # Sample data - you might want to replace this with real financial data
    data = [
        {"time": "2023-01-01", "value": 100},
        {"time": "2023-01-02", "value": 110},
        {"time": "2023-01-03", "value": 105},
        {"time": "2023-01-04", "value": 120},
        {"time": "2023-01-05", "value": 100},
    ]

    chart_options = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    series_options = {
        "type": chart_type,
        "data": data,
        "options": {}
    }

    st.subheader(f"{chart_type} Chart")
    renderLightweightCharts([{"chart": chart_options, "series": [series_options]}], key=f"{chart_type}_chart")



# Define a function to create a PDF report
def create_pdf_report(selected_currency, prediction_text):
    # Initialize filename to None for error handling
    filename = None
    
    # Check if prediction_text contains text items and process the first item
    if prediction_text and len(prediction_text) > 0 and prediction_text[0].type == 'text':
        prediction_details = prediction_text[0].text  # Use prediction_details instead of prediction_text
        
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, 'Cryptocurrency Prediction Report', 0, 1, 'C')
        pdf.ln(20)  # Add a line break
        pdf.set_font("Arial", size=12)
        
        now = datetime.datetime.now()
        date_string = now.strftime("%B %d, %Y")
        pdf.cell(0, 10, f'Report Generated on: {date_string}', 0, 1, 'C')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f'Prediction for {selected_currency}', 0, 1)
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, prediction_details)  # Use prediction_details here
        filename = f"prediction_report_{selected_currency}.pdf"
        pdf.output(filename)
    
    # Ensure to return filename, which could be None if the if condition is not met
    return filename

def price_prediction():
    st.title("🔮 Predict Cryptocurrency Prices")
    st.markdown("Provide an image of a chart and additional information, then receive a price prediction report with confidence scores for each scenario.")
    
    selected_currency = st.selectbox("Choose a pair 💸", ["BTC-USD", "ETH-USD 💎" , "USD/EUR 💵"])
    
    filename_ex = None
    response = None

    photo = st.file_uploader("Upload a chart image", type=["png", "jpg", "jpeg"])

    if photo is not None:
        file_path = "input/" + photo.name
        print(file_path)
        # BTC - USD
        if selected_currency == "BTC-USD":
            st.image("icons/Bitcoin.png", width = 100)
            prompt = st.text_input("Enter a prompt for the prediction")
            if prompt:
                response = generate_prediction(file_path , prompt)
            
    
                
            if response and len(response) > 0 and response[0].type == 'text':
                prediction_text = response[0].text
                # Use fpdf to create a PDF document
                pdf = FPDF()
                pdf.add_page()
                # Title Page
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, 'Cryptocurrency Prediction Report', 0, 1, 'C')
                pdf.ln(20)  # Add a line break

                # Report generated date
                pdf.set_font("Arial", size=12)
                
                #now = datetime.now()
                #date_string = now.strftime("%B %d, %Y")
                #pdf.cell(0, 10, f'Report Generated on: {date_string}', 0, 1, 'C')
                pdf.add_page()

                # Report Content
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, f'Prediction for {selected_currency}', 0, 1)
                pdf.ln(10)  # Add some space

                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, prediction_text)

                # Optionally, if you want to add a visual
                # Ensure you have the graph image saved as 'graph.png' in your directory
                # pdf.add_page()
                # pdf.set_font("Arial", 'B', 14)
                # pdf.cell(0, 10, 'Graphical Analysis', 0, 1)
                # pdf.ln(10)
                # pdf.image('graph.png', x = None, y = None, w = 190, h = 160)

                # Save the PDF document
                filename = f"output/prediction_report_{selected_currency}.pdf"
                pdf.output(filename)
                
                return filename    
    else : 
        st.write("Please upload a chart image to continue.")
        return None


def main():
    st.sidebar.title("🚀 Navigation")
    st.sidebar.markdown("Explore the different functionalities of Claude Crypto Assistant.")
    page = st.sidebar.radio("Go to", ["Home 🏠", "Price Predictor 🔮","Visualize Data 📈"])

    if page == "Home 🏠":
        st.title("Welcome to Claude Crypto Assistant!")
        st.markdown("Where magic happens for traders & stock traders. Get started by selecting an option from the sidebar.")
    elif page == "Price Predictor 🔮":
        price_prediction()
    elif page == "Visualize Data 📈":
        visualize_data()
if __name__ == "__main__":
    main()
