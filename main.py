import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# إعداد الصفحة لتكون دائمًا مفتوحة (expanded)
st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide", initial_sidebar_state="expanded")

# تنسيق CSS عشان القائمة تبقى "شيك" زي تطبيقات الذكاء الاصطناعي
st.markdown("""
    <style>
    /* تغيير عرض القائمة الجانبية */
    [data-testid="stSidebar"] {
        min-width: 280px;
        max-width: 280px;
        background-color: #f8f9fa; /* لون خلفية هادي */
        border-right: 1px solid #ddd;
    }
    /* جعل الأزرار تبدو مثل قوائم الدردشة */
    div.stRadio > label {
        font-weight: bold;
        font-size: 16px;
        padding: 10px;
    }
    /* إضافة لمسة احترافية للزرار */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# باقي الكود البرمجي بتاعك هنا...
