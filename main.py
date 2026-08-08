import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
import qrcode
import asyncio
import edge_tts

st.set_page_config(page_title="سوق المروة للأثاث والديكور", layout="wide")

# --- CSS للتنسيق ---
st.markdown("""
    <style>
    div[data-testid="stTabs"] > div:first-child { position: fixed !important; top: 50px !important; left: 0 !important; right: 0 !important; background-color: #ffffff; z-index: 99999; padding: 10px 20px 0px 20px; border-bottom: 2px solid #f0f2f6; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); }
    div[data-testid="stTabs"] > div:nth-child(2) { padding-top: 70px !important; }
    </style>
""", unsafe_allow_html=True)

DB_PATH = "sovereign_100_matrix.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    tables = {
        "products_catalog": "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, name TEXT, color TEXT, dims TEXT, price REAL, quantity INTEGER, location TEXT, barcode TEXT, image_path TEXT",
        "product_scripts": "id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, script_text TEXT, audio_path TEXT"
    }
    for table, schema in tables.items():
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({schema})")
    conn.commit()
    conn.close()

init_db()

st.title("🛒 سوق المروة - نظام المنتجات الناطقة (جودة بشرية)")

# --- تبويب المخزون (الجزء اللي عدلناه) ---
st.subheader("📦 إدارة المخزون وتفعيل الصوت الاحترافي")
conn = sqlite3.connect(DB_PATH)
df_p = pd.read_sql("SELECT * FROM products_catalog", conn)
st.dataframe(df_p, use_container_width=True)

if not df_p.empty:
    sel_prod_id = st.selectbox("اختر المنتج لتوليد السكريبت والصوت:", df_p['id'].tolist())
    selected_row = df_p[df_p['id'] == sel_prod_id].iloc[0]
    
    if st.button("✨ توليد السكريبت والصوت (جودة فائقة)"):
        p_name = selected_row.get('name', 'المنتج')
        p_dims = selected_row.get('dims', 'غير محدد')
        p_color = selected_row.get('color', 'طبيعي')
        p_price = selected_row.get('price', 0)
        
        generated_script = f"أهلاً بيك يا غالي.. أنا {p_name}. لوني {p_color} ومقاساتي {p_dims}. أنا قطعة متفصلة لإنسان بيفهم في الجودة.. سعري {p_price}، فـ إيه رأيك تاخدني أنور بيتك؟"
        
        os.makedirs("audio_outputs", exist_ok=True)
        audio_filename = f"audio_outputs/product_{sel_prod_id}.mp3"
        
        # استخدام الصوت البشري (شاكر المصري)
        voice = "ar-EG-ShakirNeural" 
        communicate = edge_tts.Communicate(generated_script, voice)
        asyncio.run(communicate.save(audio_filename))
        
        st.info(generated_script)
        st.audio(audio_filename, format='audio/mp3')
        st.success("تم توليد الصوت بأعلى جودة بشرية!")

conn.close()
