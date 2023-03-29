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


selected = option_menu(
    menu_title=None,
    options=["Home", "About Us", "Services", "Contact Us", "Logout"],
    icons=["house", "book", "gear", "envelope", "key"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)


# save uploaded file
def save_uploaded_file(pdf_files):
    FILE_DIR = os.path.dirname(os.path.abspath(__file__))
    PARENT_DIR = os.path.join(FILE_DIR,os.pardir)
    with open(os.path.join(PARENT_DIR,'invoices', pdf_files.name), "wb") as f:
        f.write(pdf_files.getbuffer())
    return st.success("File saved")


# files
uploaded_files = st.file_uploader("", type=['pdf'], accept_multiple_files=False)
if uploaded_files is not None:
    # file_details = {"filename":uploaded_files.name, "filetype":uploaded_files.type}
    save_uploaded_file(uploaded_files)


#NEW EXTRACTION OF DATA
def get_keyword(start, end, text):
    for i in range(len(start)):
        try:
            field=((text.split(start[i]))[1].split(end[i])[0])
            return field
        except:
            continue
#extracting....
def extract_content_keyword():
    my_dataframe = pd.DataFrame()
    for files in glob.glob('C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\invoices\\*.pdf'):
        with pdfplumber.open(files) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            text = " ".join(text.split())
            
            start = ['COMPANY NAME: ']
            end = [' ']
            keyword1 = get_keyword(start, end, text)
            
            start = ['INVOICE NR: ']
            end = [' ']
            keyword2 = get_keyword(start, end, text)
            
            start = ['DATE: ']
            end = [' ']
            keyword3 = get_keyword(start, end, text)
            
            start = ['DUE DATE: ']
            end = [' ']
            keyword4 = get_keyword(start, end, text)
            
            start = ['09/2022 ']
            end = ['63011729168']
            keyword5 = get_keyword(start, end, text)
            
            start = ['FNB ']
            end = ['DUE DATE']
            keyword6 = get_keyword(start, end, text)
            
            
            start = ['TOTAL AMOUNT ']
            end = [' ']
            keyword7 = get_keyword(start, end, text)
            
            # create a list with the keywords extracted from current document.
            my_list = [keyword1, keyword2,keyword3,keyword4,keyword5,keyword6,keyword7]
            # append my list as a row in the dataframe.
            my_list = pd.Series(my_list)

            # append the list of keywords as a row to my dataframe.
            my_dataframe = my_dataframe.append(my_list, ignore_index=True)
    progress_text = "Verification in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    st.write("Verified Successfully")
    # rename dataframe columns using dictionaries.
    my_dataframe = my_dataframe.rename(columns={0:'Company Name',
                                            1:'Invoice Number',
                                            2:'Date',
                                            3:'Due Date',
                                            4:'Bank Name',
                                            5:'Account Number',
                                            6:'Total Amount'})
    save_path = ('C:\\Users\\Majoro\\Videos\\major skul\\leriba\\tool\\StreamlitDataExtraction-main\\sample_docs')
    os.chdir(save_path)    

    # extract my dataframe to an .xlsx file!
    my_dataframe.to_excel('sample_excel.xlsx', sheet_name = 'my dataframe')
    st.write("")
    st.table(my_dataframe)

 # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.


# adding a button
if st.button('Start Verification'):
    extract_content_keyword()

    # video
    # video_file = open("Analytics.mp4", "rb").read()
    # st.video(video_file)

else:
    st.write('Click above button to start')
