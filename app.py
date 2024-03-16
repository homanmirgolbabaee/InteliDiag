import datetime
import streamlit as st
from PIL import Image
from fpdf import FPDF
# Assuming generate_prediction and summarize_pdf are defined in predictor.py
from predictor import generate_prediction
import time
from streamlit_lightweight_charts import renderLightweightCharts
import yfinance as yf
import pandas as pd



def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    # Prepare the data in the required format
    price_data = data[['Date', 'Close']].rename(columns={'Date': 'time', 'Close': 'value'})
    volume_data = data[['Date', 'Volume']].rename(columns={'Date': 'time', 'Volume': 'value'})
    # Format the date for the chart
    price_data['time'] = price_data['time'].dt.strftime('%Y-%m-%d')
    volume_data['time'] = volume_data['time'].dt.strftime('%Y-%m-%d')
    return price_data.to_dict('records'), volume_data.to_dict('records')






# Function to visualize data
def visualize_data():
    st.title("📈 Visualize Data")

    # User inputs for the ticker symbol and date range
    ticker = st.text_input("Enter Ticker Symbol", value='AAPL')
    start_date = st.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
    end_date = st.date_input("End Date", value=pd.to_datetime('2023-03-31'))
    
    if st.button('Fetch Data'):
        price_data, volume_data = fetch_data(ticker, start_date, end_date)
        
        priceVolumeChartOptions = {
            "height": 400,
            "layout": {
                "background": {
                    "type": 'solid',
                    "color": '#131722'
                },
                "textColor": '#d1d4dc',
            },
            "grid": {
                "vertLines": {
                    "color": 'rgba(42, 46, 57, 0)',
                },
                "horzLines": {
                    "color": 'rgba(42, 46, 57, 0.6)',
                }
            }
        }

        priceVolumeSeries = [
            {
                "type": 'Area',
                "data": price_data,
                "options": {
                    "topColor": 'rgba(38,198,218, 0.56)',
                    "bottomColor": 'rgba(38,198,218, 0.04)',
                    "lineColor": 'rgba(38,198,218, 1)',
                    "lineWidth": 2,
                }
            },
            {
                "type": 'Histogram',
                "data": volume_data,
                "options": {
                    "color": '#26a69a',
                    "priceFormat": {
                        "type": 'volume',
                    },
                    "priceScaleId": "",  # Note: Set as an overlay setting
                },
                "priceScale": {
                    "scaleMargins": {
                        "top": 0.8,  # Adjusted for better visualization
                        "bottom": 0,
                    }
                }
            }
        ]

        st.subheader(f"Price and Volume Series Chart for {ticker}")
        renderLightweightCharts([
            {
                "chart": priceVolumeChartOptions,
                "series": priceVolumeSeries
            }
        ], 'priceAndVolume')



def price_prediction():
    st.title("🔮 Predict Cryptocurrency Prices")
    st.markdown("Provide an image of a chart and additional information, then receive a price prediction report with confidence scores for each scenario.")

    # Create two columns for data entry and report download
    data_entry_col, download_report_col = st.columns([2, 1])

    with data_entry_col:
        st.header("Data Entry")
        report_difficulty_level = st.selectbox("Choose a report difficulty level 💸", ["Standard", "Expert", "Crazy"])
        photo = st.file_uploader("Upload a chart image (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"], help="Upload a chart image for prediction")
        prompt = st.text_input("Enter a prompt for the prediction")

    with download_report_col:
        st.header("Download Report")
        if photo and prompt:
            # Logic to handle file upload and prompt submission
            file_path = "input/" + photo.name  # Placeholder for file saving logic
            response = generate_prediction(file_path, prompt, report_difficulty_level)
            
            if response and len(response) > 0 and response[0].type == 'text':
                prediction_text = response[0].text
                
                # Generate PDF report
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", 'B', 16)
                pdf.cell(0, 10, 'Cryptocurrency Prediction Report', 0, 1, 'C')
                pdf.set_y(pdf.get_y() + 20)
                pdf.set_font("Helvetica", size=12)
                #now = datetime.now()
                #date_string = now.strftime("%B %d, %Y")
                #pdf.cell(0, 10, f'Report Generated on: {date_string}', 0, 1, 'C')
                pdf.add_page()
                pdf.set_font("Helvetica", 'B', 14)
                pdf.set_y(pdf.get_y() + 10)
                pdf.set_font("Helvetica", size=12)
                pdf.multi_cell(0, 10, prediction_text)
                filename = f"reports/prediction_report.pdf"
                pdf.output(filename)
                
                # Provide a link for the user to download the report
                with open(filename, "rb") as file:
                    btn = st.download_button(
                        label="Download Prediction Report",
                        data=file,
                        file_name=filename,
                        mime="application/octet-stream"
                    )
                st.success("Report generated successfully. Please download using the button above.")
        else:
            st.warning("Please upload a chart image and enter a prompt to enable report generation.")


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
