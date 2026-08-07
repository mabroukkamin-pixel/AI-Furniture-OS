import streamlit as st
import pandas as pd
import requests

SHEET_ID = '1hyWigWYiVsRPQH3tYz2Oxyilo9yDs4p_Q0R0AHk_SGU'
WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbxQJ4VEzVOaChGCrRP9fdFlQjcCH41By2VrTWPt_jdgh9Tq26UGBQO7RVXDmL8PAVJA/exec'

st.set_page_config(page_title="نظام الإدارة العالمي", layout="wide")
st.title("👑 النظام العالمي لإدارة العمليات")

@st.cache_data(ttl=60)
def load_data():
    products_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Products'
    orders_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Orders'
    return pd.read_csv(products_url), pd.read_csv(orders_url)

df_products, df_orders = load_data()

tab1, tab2 = st.tabs(["إصدار فاتورة", "لوحة الإحصائيات والمبيعات"])

with tab1:
    product_name = st.selectbox("اختر المنتج:", df_products['Product_Name'].unique())
    product_details = df_products[df_products['Product_Name'] == product_name].iloc[0]
    st.write(f"السعر: {product_details['Price']} دينار")
    
    with st.form("order_form", clear_on_submit=True):
        client_name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        
        submitted = st.form_submit_button("حفظ الطلب في النظام")
        
        if submitted:
            if client_name and phone:
                with st.spinner('جاري إرسال الطلب للسحابة...'):
                    order_data = {
                        "client_name": client_name,
                        "phone": phone,
                        "product_name": product_name,
                        "price": str(product_details['Price'])
                    }
                    try:
                        response = requests.post(WEB_APP_URL, json=order_data)
                        if response.status_code == 200:
                            st.success(f"تم تسجيل طلب العميل {client_name} بنجاح!")
                        else:
                            st.error("خطأ في الاتصال بقاعدة البيانات.")
                    except Exception as e:
                        st.error(f"خطأ في الإرسال: {e}")
            else:
                st.error("الرجاء إدخال اسم العميل ورقم الهاتف.")

with tab2:
    st.subheader("📊 ملخص حركة العمليات")
    if not df_orders.empty:
        col1, col2 = st.columns(2)
        col1.metric("إجمالي عدد الطلبات", len(df_orders))
        price_col = 'الإجالى' if 'الإجالى' in df_orders.columns else df_orders.columns[-1]
        total_revenue = pd.to_numeric(df_orders[price_col], errors='coerce').sum()
        col2.metric("إجمالي المبيعات", f"{total_revenue} دينار")
        
        st.write("---")
        st.subheader("سجل الطلبات المسجلة سحابياً:")
        st.dataframe(df_orders, use_container_width=True)
    else:
        st.info("لا توجد طلبات مسجلة حتى الآن. قم بتسجيل أول طلب من تبويب إصدار فاتورة!")
