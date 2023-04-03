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
from datetime import date as dt
import time
import tempfile
from flask import redirect
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
# save uploaded file
def save_uploaded_file(pdf_files):
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.join(FILE_DIR,os.pardir)
    with open(os.path.join(PARENT_DIR,'invoices', pdf_files.name), "wb") as f:
        f.write(pdf_files.getbuffer())
    return st.success("File saved")

def read_pdf(file):
    pdf_reader = PyPDF2.PdfFileReader(file)
    page_count = pdf_reader.getNumPages()
    text = ""
    for i in range(page_count):
        page = pdf_reader.getPage(i)
        text += page.extractText()
    return text


        # Display the data
        #st.write(f"**{uploaded_file.name}**")
        
    
            #st.write(text)
    # file_details = {"filename":uploaded_files.name, "filetype":uploaded_files.type}
    #save_uploaded_file(uploaded_files)


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
                
            # create a list with the keywords extracted from current document.
            my_list = [keyword1, keyword2,keyword3,keyword4,keyword6,keyword7]
            # append my list as a row in the dataframe.
            my_list = pd.Series(my_list)

            # append the list of keywords as a row to my dataframe.
            my_dataframe = my_dataframe.append(my_list, ignore_index=True)
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    st.write("Data Extracted Successfully")
        # rename dataframe columns using dictionaries.
    my_dataframe = my_dataframe.rename(columns={0:'Company Name',
                                                1:'Invoice Number',
                                                2:'Date',
                                                3:'Due Date',
                                                5:'Account Number',
                                                5:'Total Amount'})
    #save_path = ('C:\\Users\\Majoro\\Videos\\major skul\\leriba\\tool\\StreamlitDataExtraction-main\\sample_docs')
    #os.chdir(save_path)
    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create file path for CSV file
    xlsx_file_path = os.path.join(dir_path, 'sample_excel.xlsx')

        # extract my dataframe to an .xlsx file!
    my_dataframe.to_excel(xlsx_file_path, sheet_name = 'my dataframe')
    st.write("")
    st.table(my_dataframe)

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
        # Pass the directory path to the other function
        
            
    # Press the green button in the gutter to run the script.


# adding a button
if st.button('Start Data extraction'):
    extract_content_keyword(pdf_dir)

    # video
    # video_file = open("Analytics.mp4", "rb").read()
    # st.video(video_file)

else:
    st.write('Click above button to start')
    
    
st.sidebar.write("Logout")
if st.sidebar.button("Click to Logout"):
    # Clear session state
    redirect("https://leribaai.000webhostapp.com/")
