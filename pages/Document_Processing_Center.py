import PyPDF2
import os
import re
import openpyxl
import xlsxwriter
import streamlit as st
from PIL import Image
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as se
#new libraries
import glob                      # generates lists of files matching given patterns
import pdfplumber                # extracts information from .pdf documents
import numpy as np
import base64
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import time
import tempfile
from flask import redirect
from io import BytesIO
import base64
import io
import math
hide_streamlit_style = """
            <style>
            
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


@st.cache_data
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
        png_file,
        background_position="50% 10%",
        margin_top="10%",
        image_width="100%",
        image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )


add_logo("lg.png")


# with st.sidebar:
#     # images
#     img = Image.open("logo.png")
#     st.image(img, width=300)
#     # Text/Title
#     st.write("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Fascinate');
#     html, body, [class*="css"]  {
#    font-family: 'Verdana', cursive;
#    background: white;
#     }
#     </style>
#     """, unsafe_allow_html=True)



pdf_dir="pdf_files"

def save_pdf_file(uploaded_file):
    # Get the current working directory
    cwd = os.getcwd()

    # Create the directory if it doesn't already exist
    pdf_dir_path = os.path.join(cwd, pdf_dir)
    #st.write(pdf_dir_path)
    os.makedirs(pdf_dir_path, exist_ok=True)
    # If a file was uploaded, save it to the pdf_dir directory using a relative path
    if uploaded_file is not None:
        pdf_path = os.path.join(pdf_dir, uploaded_file.name)
        #st.write(pdf_path)
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        #st.success(f"Saved file ")

        # Return the directory path
        return pdf_dir_path
    # If no file was uploaded, return None
    return None


def get_processing_time(start_time):
    end_time = datetime.now()
    processing_time = end_time - start_time
    processing_time.total_seconds()
    seconds = processing_time.total_seconds()
    # Round the float value to 1 significant figure
    rounded_seconds = round(seconds, -int(math.floor(math.log10(abs(seconds))))+1)
    # Create a new timedelta object using the rounded number of seconds
    rounded_processing_time = float(rounded_seconds)
    # Format the float value as a string with one digit after the decimal point
    formatted_processing_time = "{:.1f}".format(rounded_processing_time)
    return formatted_processing_time

#NEW EXTRACTION OF DATA
def get_keyword(start, end, text):
    for i in range(len(start)):
        try:
            field=((text.split(start[i]))[1].split(end[i])[0])
            return field
        except:
            continue
#extracting....
def extract_content_keyword(pdf_dir_path):
    start_time = datetime.now()
    # data extraction code
    my_dataframe = pd.DataFrame()
    for file_name in os.listdir(pdf_dir_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(pdf_dir_path, file_name)
            #st.write("Processing file {file_path}")
        with pdfplumber.open(file_path) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            text = " ".join(text.split())
                
            start = [' ']
            end = ['DUE','DUE ']
            keyword1 = get_keyword(start, end, text)
                
            start = ['R:']
            end = ['F']
            keyword2 = get_keyword(start, end, text)
                
            start = ['DATE: ']
            end = [' ']
            keyword3 = get_keyword(start, end, text)
                
            start = ['DUE DATE: ']
            end = [' ']
            keyword4 = get_keyword(start, end, text)
                
            start = ['FNB']
            end = ['DATE:']
            keyword6 = get_keyword(start, end, text)
                
                
            start = ['subtotal:']
            end = [' TOTAL']
            keyword7 = get_keyword(start, end, text)
            
            processing_time = get_processing_time(start_time)
                
            # create a list with the keywords extracted from current document.
            my_list = [keyword1, keyword2,keyword3,keyword4,keyword6,keyword7,processing_time]
            # append my list as a row in the dataframe.
            my_list = pd.Series(my_list)

            # append the list of keywords as a row to my dataframe.
            my_dataframe = my_dataframe.append(my_list, ignore_index=True)
    progress_text = "Data extraction in progress..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    st.write("Data extraction complete")
        # rename dataframe columns using dictionaries.
    my_dataframe = my_dataframe.rename(columns={0:'Company Name',
                                                1:'Invoice Number',
                                                2:'Date',
                                                3:'Due Date',
                                                4:'Account Number',
                                                5:'Total Amount',
                                                6:'Processing Time(s)'})
    #save_path = ('C:\\Users\\Majoro\\Videos\\major skul\\leriba\\tool\\StreamlitDataExtraction-main\\sample_docs')
    #os.chdir(save_path)
    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create file path for CSV file
    xlsx_file_path = os.path.join(dir_path, 'sample_excel.xlsx')

        # extract my dataframe to an .xlsx file!
    my_dataframe.to_excel(xlsx_file_path, sheet_name = 'my dataframe')
    #st.write("")
    #st.table(my_dataframe)
    # delete the PDFs after extracting data
    for file_name in os.listdir(pdf_dir_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(pdf_dir_path, file_name)
            os.remove(file_path)
    #st.write("PDF files deleted.")
    return my_dataframe
 # Press Ctrl+F8 to toggle the breakpoint.

# files
uploaded_files = st.file_uploader(" ", type=['pdf'], accept_multiple_files=True)
st.markdown('''
                    <style>
                    .uploadedFile {display: none}
                    </style>''',
                    unsafe_allow_html=True)
for uploaded_file in uploaded_files:
    if uploaded_file.type == "application/pdf":
        
        # Read the data of the PDF file
        pdf_dir_path = save_pdf_file(uploaded_file)
        if pdf_dir_path is not None:
            pdf_dir = pdf_dir_path
        # Pass the directory path to the other function
        
            
    # Press the green button in the gutter to run the script.


# adding a button
if st.button('Start Data extraction'):
    if pdf_dir == "pdf_files":
        st.write("No PDF files uploaded.")
    else:
        extracted_data = extract_content_keyword(pdf_dir)
        # convert DataFrame to Excel format
        excel_file = io.BytesIO()
        extracted_data.to_excel(excel_file, index=False, sheet_name='Sheet1')
        excel_file.seek(0)

        # generate download link
        b64 = base64.b64encode(excel_file.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="extracted_data.xlsx">Download Excel File</a>'

        # create download button
        st.download_button(label='Export Data as Excel', data=excel_file, file_name='extracted_data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        st.write("")
        st.table(extracted_data)
else:
    st.write('Click above button to start')
    
    
st.sidebar.write("Logout")
if st.sidebar.button("Click to Logout"):
    # Clear session state
    redirect("https://leribaai.000webhostapp.com/")
