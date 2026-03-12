import streamlit as st
import pandas as pd
import easyocr
import re
from main import extract_amount, extract_date, categorize_expense

st.title("🧾 BillSmart")
page = st.sidebar.selectbox("Menu", ["📤 Scan Receipt", "📊 My History"])

if page == "📤 Scan Receipt":
    st.subheader("Upload your receipt")
    uploaded_file = st.file_uploader("Choose a receipt image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        st.image(uploaded_file, width=300)
        
        if st.button("🔍 Process Receipt"):
            with st.spinner("Reading your receipt...."):
                from PIL import Image
                import numpy as np
                image = Image.open(uploaded_file)
                image_array = np.array(image)
                reader = easyocr.Reader(['en'])
                result = reader.readtext(image_array)
                full_text = ' '.join([d[1] for d in result])
            
            amounts = extract_amount(full_text)
            dates = extract_date(full_text)
            category = categorize_expense(full_text)
            
            st.success("Done!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Category", category)
            col2.metric("Date", dates[0] if dates else "Today")
            col3.metric("Total", f"{amounts[-1] if amounts else '0'}")