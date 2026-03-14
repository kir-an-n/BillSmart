import streamlit as st
import pandas as pd
import easyocr
from datetime import datetime
from PIL import Image
import numpy as np
from utils import extract_amount, extract_date, categorize_expense

st.set_page_config(page_title="BillSmart", page_icon="🧾", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
    [data-testid="stSidebar"] {
        background-color: #f8f9ff;
        border-right: 1px solid #e0e8ff;
    }
    h1 {color: #1a6be0 !important;}
    [data-testid="stMetric"] {
        background: #f8f9ff;
        border-radius: 10px;
        padding: 0.8rem;
        border: 1px solid #e0e8ff;
    }
    .stButton>button {
        background-color: #1a9e5c !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["📤 Scan Receipt", "📊 My History"], label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.caption("BillSmart · Scan any receipt. Track every rupee.")

st.title("🧾 BillSmart")
st.divider()

if page == "📤 Scan Receipt":
    uploaded_file = st.file_uploader("Drop your receipt here", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        col_img, col_info = st.columns([1, 1])
        
        with col_img:
            st.image(uploaded_file, use_column_width=True)
        
        with col_info:
            with st.spinner("Reading receipt..."):
                image = Image.open(uploaded_file)
                image_array = np.array(image)
                reader = easyocr.Reader(['en'])
                result = reader.readtext(image_array)
                full_text = ' '.join([d[1] for d in result])
            
            amounts = extract_amount(full_text)
            dates = extract_date(full_text)
            category = categorize_expense(full_text)
            date = dates[0] if dates else datetime.now().strftime('%d-%m-%Y')
            total = amounts[-1] if amounts else '0'
            
            st.metric("Category", category)
            st.metric("Total", f"₹{total}")
            st.metric("Date", date)
            
            if st.button("💾 Save to History", type="primary"):
                data = {
                    'date': [date],
                    'amounts': [', '.join(amounts)],
                    'total': [total],
                    'category': [category],
                    'saved_at': [datetime.now().strftime('%d-%m-%Y %H:%M')]
                }
                df = pd.DataFrame(data)
                df.to_csv('expenses.csv', mode='a', header=not pd.io.common.file_exists('expenses.csv'), index=False)
                st.success("Saved!")

if page == "📊 My History":
    try:
        df = pd.read_csv('expenses.csv')
        col1, col2 = st.columns(2)
        col1.metric("Total Receipts", len(df))
        col2.metric("Top Category", df['category'].mode()[0])
        st.divider()
        st.bar_chart(df.groupby('category')['total'].count())
        st.dataframe(df, use_container_width=True)
    except:
        st.info("No expenses yet. Scan your first receipt!")