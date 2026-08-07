import streamlit as st
import pandas as pd

SHEET_ID = '1hyWigWYiVsRPQH3tYz2Oxyilo9yDs4p_Q0R0AHk_SGU'
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Products'

st.title("👑 النظام العالمي لإدارة العمليات")

@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()

# اختيار المنتج
product_name = st.selectbox("اختر المنتج:", df['Product_Name'].unique())

# تصفية البيانات لعرض تفاصيل المنتج المختار
product_details = df[df['Product_Name'] == product_name].iloc[0]

st.write(f"### تفاصيل المنتج: {product_name}")
st.write(f"- **السعر:** {product_details['Price']} دينار")
st.write(f"- **المقاسات:** {product_details['Dimensions']}")
st.write(f"- **اللون:** {product_details['Color']}")
