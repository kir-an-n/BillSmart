import streamlit as st
import pandas as pd
import easyocr
import re
from utils import extract_amount, extract_date, categorize_expense

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
            col3.metric("Total", f"₹{amounts[-1] if amounts else '0'}")
            
            if st.button("💾 Save to History"):
                from datetime import datetime
                data = {
                    'date': [dates[0] if dates else datetime.now().strftime('%d-%m-%Y')],
                    'amounts': [', '.join(amounts)],
                    'total': [amounts[-1] if amounts else '0'],
                    'category': [category]
                }
                df = pd.DataFrame(data)
                df.to_csv('expenses.csv', mode='a', header=not pd.io.common.file_exists('expenses.csv'), index=False)
                st.success("Saved to history!")
                if page == "📊 My History":
                        st.subheader("My Expense History")
    
                try:
                    df = pd.read_csv('expenses.csv')
                    st.dataframe(df, use_container_width=True)
                    st.bar_chart(df.groupby('category')['total'].count())
                except FileNotFoundError:
                    st.info("No expenses yet! Go scan your first receipt.")