import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# 1. إعداد الصفحة (يجب أن يكون أول أمر)
st.set_page_config(page_title="سوق المروة", layout="wide", initial_sidebar_state="expanded")

# 2. تنسيق الـ CSS (لضمان ظهور القائمة وشكل احترافي)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 250px;
        background-color: #f0f2f6;
    }
    .main {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (شكل ChatGPT)
with st.sidebar:
    st.title("🛒 سوق المروة")
    st.write("نظام الإدارة المتكامل")
    st.divider()
    page = st.radio("القائمة الرئيسية:", ["📊 لوحة التحكم", "📦 المخزون", "📈 الصفقات"])

# 4. محتوى الصفحات
if page == "📊 لوحة التحكم":
    st.header("أهلاً بك يا أمين")
    st.write("هنا تجد ملخص العمليات اليومية.")
    
elif page == "📦 المخزون":
    st.header("إدارة المخزون")
    # هنا تقدر تكمل كود عرض الجدول بتاعك

elif page == "📈 الصفقات":
    st.header("الصفقات الجديدة")

# ملاحظة: إذا ظهرت صفحة بيضاء، معناه إن فيه مكتبة مش موجودة أو مسار قاعدة البيانات فيه مشكلة.
