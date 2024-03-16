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



def price_prediction():
    
    response = None
    st.title("🔮 Predict Cryptocurrency Prices")
    st.markdown("Provide an image of a chart and additional information, then receive a price prediction report with confidence scores for each scenario.")
    
    


    # Create two columns
    col1, col2 = st.columns(2)

    # Code for the first column
    with col1:
        report_difficulty_level = "Standard"
        report_difficulty_level = st.selectbox("Choose a level report 💸", ["Standard", "Expert" , "Crazy"])
        with st.spinner("This should take a few seconds ... "): 
            time.sleep(1.5)
            if report_difficulty_level == "Standard":
                st.success(f'✅ Report Difficulty set to {report_difficulty_level}  🕵️‍♂️')
            if report_difficulty_level == "Expert":
                st.success(f'✅ Report Difficulty set to {report_difficulty_level}  🧠')  
            if report_difficulty_level == "Crazy":
                st.success(f'✅ Report Difficulty set to {report_difficulty_level}  🤯')   
            
    # Code for the second column
    with col2:
        photo = st.file_uploader("Upload a chart image (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"], help="Upload a chart image for prediction")
        if photo is not None:
            file_path = "input/" + photo.name
            print(file_path)
            
            prompt = st.text_input("Enter a prompt for the prediction")
            if prompt:
                response = generate_prediction(file_path , prompt , report_difficulty_level)
    
                if response and len(response) > 0 and response[0].type == 'text':
                    prediction_text = response[0].text
                    # Use fpdf to create a PDF document
                    pdf = FPDF()
                    pdf.add_page()
                    # Title Page
                    pdf.set_font("Helvetica", 'B', 16)
                    pdf.cell(0, 10, 'Cryptocurrency Prediction Report', 0, 1, 'C')
                    pdf.set_y(pdf.get_y() + 20)

                    # Report generated date
                    pdf.set_font("Helvetica", size=12)
                    
                    #now = datetime.now()
                    #date_string = now.strftime("%B %d, %Y")
                    #pdf.cell(0, 10, f'Report Generated on: {date_string}', 0, 1, 'C')
                    pdf.add_page()

                    # Report Content
                    pdf.set_font("Helvetica", 'B', 14)
                    #pdf.cell(0, 10, f'Prediction for {selected_currency}', 0, 1)
                    pdf.set_y(pdf.get_y() +10)

                    pdf.set_font("Helvetica", size=12)
                    pdf.multi_cell(0, 10, prediction_text)

                    # Optionally, if you want to add a visual
                    # Ensure you have the graph image saved as 'graph.png' in your directory
                    # pdf.add_page()
                    # pdf.set_font("Arial", 'B', 14)
                    # pdf.cell(0, 10, 'Graphical Analysis', 0, 1)
                    # pdf.ln(10)
                    # pdf.image('graph.png', x = None, y = None, w = 190, h = 160)

                    # Save the PDF document
                    filename = f"reports/prediction_report.pdf"
                    pdf.output(filename)
                    
                    return filename    
            else : 
                st.info("Please upload a chart image to continue.")
                return None

st.set_page_config(
    page_title="Claude Crypto Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com',
        'Report a bug': "https://www.example.com",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)





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
