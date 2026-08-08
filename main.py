st.markdown("""
    <style>
    /* إجبار القائمة الجانبية على الظهور دائماً وعدم الاختفاء */
    [data-testid="stSidebar"] {
        display: flex !important;
        flex-direction: column !important;
        position: fixed !important;
        top: 0;
        left: 0;
        height: 100vh;
        width: 280px !important;
        background-color: #f8f9fa !important;
        z-index: 9999;
        border-right: 1px solid #e0e0e0;
        padding-top: 20px;
    }
    
    /* إزاحة المحتوى الرئيسي لليمين عشان القائمة متغطيش عليه */
    section[data-testid="stSidebar"] + div {
        margin-left: 280px !important;
        width: calc(100% - 280px) !important;
    }

    /* إخفاء زرار القفل أو السهم اللي بيقفل القائمة */
    button[data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
