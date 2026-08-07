import streamlit as st
import pandas as pd

# إعدادات النظام العالمي
st.set_page_config(page_title="النظام العالمي لأمين مبروك", layout="wide")

st.title("👑 النظام العالمي لإدارة العمليات")

# ملاحظة: سنقوم لاحقاً بتفعيل الربط المباشر مع Google Sheets
# حالياً النظام يقرأ من البيانات التي أدخلتها يدوياً للسرعة
products_db = {"طرابيزة تلفزيون": 60, "خزانة 4 رفوف": 85}

menu = st.sidebar.selectbox("اختر القسم:", ["إدارة التصميم", "إدارة الحسابات", "دليل حل المشكلات"])

if menu == "إدارة الحسابات":
    st.header("إدارة الحسابات (البيانات المحدثة)")
    
    # اختيار المنتج من القائمة الثابتة
    selected_product = st.selectbox("اختر المنتج:", list(products_db.keys()))
    price = products_db[selected_product]
    
    st.write(f"السعر المعتمد: **{price} دينار**")
    
    # تسجيل الطلبات
    with st.form("order_form"):
        client_name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        submit = st.form_submit_button("إصدار الفاتورة")
        
        if submit:
            st.success(f"تم تسجيل طلب {client_name} بنجاح!")
            # هنا سنربط لاحقاً بملف Google Sheets ليحفظ البيانات فيه

st.sidebar.write("إصدار النظام: 2.1 (جاهز للربط السحابي)")
