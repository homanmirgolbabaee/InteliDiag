import datetime
from numpy import empty
import streamlit as st
# Import other necessary libraries like pandas, numpy, matplotlib, etc.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

from predictor import generate_prediction,summarize_pdf
from fpdf import FPDF





def home():
    st.title("Claude Crypto Assistant")
    st.text("Magic Happens Here")

def price_prediction():
    st.title("Predict Cryptocurrency Prices")
    # UI for input parameters
    selected_currency = st.selectbox("Choose a cryptocurrency", ["DOT", "Ethereum", "Ripple"])

    response = generate_prediction("DOT2.jpg")
    if selected_currency == "DOT":
        if st.button("Generate Report"):
            # Assuming prediction_result returns a list of ContentBlock and you need the text from the first one
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
                filename = f"prediction_report_{selected_currency}.pdf"
                pdf.output(filename)
                
                return filename

    # Display the image to the user
    image = Image.open("DOT2.jpg")
    st.image(image, caption="DOT2.jpg")
    #summarize_pdf("prediction_report_DOT.pdf")   

def data_visualization():
    st.title("Cryptocurrency Data Visualization")
    st.text("Visualize historical price data and trends here.")
    # Placeholder for data visualization logic




def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Price Predictor 🛠️"])

    if page == "Home":
        home()
        
    elif page == "Price Predictor 🛠️":
        price_prediction()





if __name__ == "__main__":
    main()
