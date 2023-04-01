from pickletools import float8
from tkinter.font import names
from turtle import title, width
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import PyPDF2
import os
import plotly.express as px
import seaborn as sns
from streamlit_option_menu import option_menu
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plost
import altair as alt
import base64
from numerize.numerize import numerize
from datetime import date, datetime
from flask import redirect


st.set_page_config(
    page_title="Dashboard",
    page_icon="🌏",
    layout="wide"
)


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

# if selected == "Home"
#     st.write("Home")
#     st.write("About")
#     st.write("Services")
#     st.write("Contacts")
#     st.write("Logout")


# def extract_insert_to_xlsx_file():
#     # counting number of processed documents
#     count = 0
#     # Extracting data from the multiple pdf files
#     for file_name in os.listdir('invoices'):
#         # st.write(file_name)
#         load_pdf = open(r'C:\\Users\\KOLOTSANE\\PycharmProjects\\DataExtraction\\invoices\\' + file_name, 'rb')
#         read_pdf = PyPDF2.PdfFileReader(load_pdf, strict=False)
#         count += 1
#     st.subheader("Documents Processed  " + str(count))
#     # st.pyplot(plot_pie(accurately_processed, notgood))

#with st.sidebar:
     #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
     #df1=pd.read_excel(excel_file)
     #invoice_filter = st.multiselect(label='Select Invoice Filter',
        #                  options=df1['Invoice Number'].unique(),
         #                   default=df1['Invoice Number'].unique())
#df1=df1.query("Invoice Number == @invoice_filter")

# NEW MODIFICATION
def doc_table():
    # Get current directory path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Create file path for CSV file
    xlsx_file_path = os.path.join(dir_path, 'style.css')
    with open(xlsx_file_path) as f:
         # Get current directory path
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Create file path for CSV file
        xlsx_file_path_1 = os.path.join(dir_path, 'pages/sample_excel.xlsx')
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
        df1=pd.read_excel(xlsx_file_path_1)
        all_documents = int(len(df1.index))
        df1.dropna(inplace=True)
        df1["Total Amount"] = df1["Total Amount"].str.replace("R","",regex=False)
        df1["Total Amount"] = df1["Total Amount"].str.replace(" ","",regex=True).astype(float)
        accurately_processed = int(len(df1.index))
        inaccurately_processed = all_documents - accurately_processed
        col1, col2, col3 = st.columns(3)
        col1.metric("All Processed Documents", all_documents,"100%")
        col2.metric("Accurately Processed Documents", accurately_processed,str(round(float(accurately_processed/all_documents * 100),1)) + "%")
        col3.metric("Inaccurately Processed Documents", inaccurately_processed,str(round(float(inaccurately_processed/all_documents *100),1)) +"%")
        #st.dataframe(df1)

def doc_table_1():
    col4,col5,col6 = st.columns(3)
    col4.metric("Time saving",50,"seconds per document")
    col5.metric("Cost saving","$57348",'per hour saved')
    col6.metric("Document type",'100%',"Only pdf documents supported")
def total_by_date():
    Q1,Q2=st.columns(2)
    with Q1:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #Create file path for CSV file
        xlsx_file_path = os.path.join(dir_path, 'pages/sample_excel.xlsx')
        #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
        df1=pd.read_excel(xlsx_file_path)
        df1["Total Amount"] = df1["Total Amount"].str.replace("R","",regex=False)
        df1["Total Amount"] = df1["Total Amount"].str.replace(" ","",regex=True).astype(float)
        tot_by_date = df1.groupby(by=['Company Name']).sum([['Total Amount']])
        fig_total = px.bar(tot_by_date,x=tot_by_date.index,y='Total Amount',title='<b>Total Amount by Date</b>',color_discrete_sequence=['#008388'] * len(tot_by_date),template='plotly_white')
        fig_total.update_layout(xaxis=dict(tickmode='linear'),plot_bgcolor='rgba(0,0,0,0)',yaxis=(dict(showgrid=False)),)
        st.plotly_chart(fig_total)
    with Q2:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #Create file path for CSV file
        xlsx_file_path = os.path.join(dir_path, 'pages/sample_excel.xlsx')
        #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
        df1=pd.read_excel(xlsx_file_path)
        df1["Total Amount"] = df1["Total Amount"].str.replace("R","",regex=False)
        df1["Total Amount"] = df1["Total Amount"].str.replace(" ","",regex=True).astype(float)
        df4 = df1.groupby(by='Company Name').sum()[['Total Amount']].reset_index()
        fig_spend_by_gender = px.pie(df4,names='Company Name',values='Total Amount',title='<b>Total Amount by Due Date</b>')
        fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
        st.plotly_chart(fig_spend_by_gender,use_container_width=True)
    
def due_by_invoice():
    Q3,Q4=st.columns(2)
    with Q3:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #Create file path for CSV file
        xlsx_file_path = os.path.join(dir_path, 'pages/sample_excel.xlsx')
        #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
        df1=pd.read_excel(xlsx_file_path)
        tot_by_date = df1.groupby(by=['Company Name']).sum([['Invoice Number']])
        fig_total = px.bar(tot_by_date,x=tot_by_date.index,y='Invoice Number',title='<b>Total Invoices by Due Date</b>',color_discrete_sequence=['#25AAD5'] * len(tot_by_date),template='plotly_white')
        fig_total.update_layout(xaxis=dict(tickmode='linear'),plot_bgcolor='rgba(0,0,0,0)',yaxis=(dict(showgrid=False)),)
        st.plotly_chart(fig_total)
    with Q4:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #Create file path for CSV file
        xlsx_file_path = os.path.join(dir_path, 'pages/sample_excel.xlsx')
        #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
        df1=pd.read_excel(xlsx_file_path)
        df1["Total Amount"] = df1["Total Amount"].str.replace("R","",regex=False)
        df1["Total Amount"] = df1["Total Amount"].str.replace(" ","",regex=True).astype(float)
        df4 = df1.groupby(by='Invoice Number').sum()[['Total Amount']].reset_index()
        fig_spend_by_gender = px.pie(df4,names='Invoice Number',values='Total Amount',title='<b>Total Amount by Invoice Number</b>')
        fig_spend_by_gender.update_layout(title = {'x':0.5}, plot_bgcolor = "rgba(0,0,0,0)")
        st.plotly_chart(fig_spend_by_gender,use_container_width=True)
        
def last_analysis():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    #Create file path for CSV file
    xlsx_file_path = os.path.join(dir_path, 'pages/sample_excel.xlsx')
    #excel_file= 'C:\\Users\\Majoro\\Videos\\major skul\\Leriba\\tool\\StreamlitDataExtraction-main\\sample_docs\\sample_excel.xlsx'
    df1=pd.read_excel(xlsx_file_path)
    all_documents = int(len(df1.index))
    df1.dropna(inplace=True)
    df1["Total Amount"] = df1["Total Amount"].str.replace("R","",regex=False)
    df1["Total Amount"] = df1["Total Amount"].str.replace(" ","",regex=True).astype(float)
    accurately_processed = int(len(df1.index))
    inaccurately_processed = all_documents - accurately_processed
    pending_documents= all_documents - accurately_processed
    total1,total2,total3 = st.columns(3,gap='large')

    with total1:
        #st.image('lg.png',use_column_width='Auto')
        st.metric(label = 'Uploaded Documents', value= numerize(accurately_processed))
        
    with total2:
        #st.image('images/tap.png',use_column_width='Auto')
        st.metric('Average accuracy','95%')

    with total3:
        #st.image('images/hand.png',use_column_width='Auto')
        st.metric(label= 'Pending Documents',value=numerize(pending_documents,2))


# st.subheader("Number Of Processed Documents")
# extract_insert_to_xlsx_file()
# pie_chart_create()
doc_table()
doc_table_1()
#area_analys()
total_by_date()
due_by_invoice()
last_analysis()
#chart_label()
#doc_table_2()
#pie_chart()
#chart_label()
#line_chart_plot()

#image_function()

def graph_refiner(df4, x="date", y="documents"):
    # Create a selection that chooses the nearest point & selects based on x-value
    hover = alt.selection_single(
        fields=[x],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(df4)
        .mark_line(point="transparent")
        .encode(x=x, y=y)
        .transform_calculate(color='datum.delta < 0 ? "red" : "green"')
    )

    # Draw points on the line, highlight based on selection, color based on delta
    points = (
        lines.transform_filter(hover)
        .mark_circle(size=65)
        .encode(color=alt.Color("color:N", scale=None))
    )

    # Draw an invisible rule at the location of the selection
    tooltips = (
        alt.Chart()
        .mark_rule(opacity=0)
        .encode(
            x=x,
            y=y,
            tooltip=[x, y, alt.Tooltip("delta", format=".2%")],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()
st.sidebar.write("Logout")
if st.sidebar.button("Click to Logout"):
    # Clear session state
    session_state = st.session_state
    session_state.clear()
    redirect("https://example.com/login.html")
