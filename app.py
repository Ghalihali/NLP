import streamlit as st

# إعداد الصفحة
st.set_page_config(
    page_title="تحليل المشاعر العربي",
    page_icon="💬",
    layout="centered"
)

# 🖼️ عرض شعار المشروع
st.image("logo.png", width=120)

# عنوان رئيسي بتنسيق جميل
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50; margin-top:20px;'>تحليل المشاعر في وسائل التواصل الاجتماعي</h1>
    <p style='text-align: center; font-size:18px; color:#555;'>ابدأ بتحليل مشاعر النصوص العربية بسهولة واحترافية!</p>
    """,
    unsafe_allow_html=True
)

# تهيئة حالة الجلسة
if 'text' not in st.session_state:
    st.session_state['text'] = ""
if 'navigate' not in st.session_state:
    st.session_state['navigate'] = False

# تقسيم الصفحة لاختيار طريقة البداية
st.markdown("<h3 style='text-align: center; margin-top:40px;'>🎯 اختر طريقة البداية:</h3>", unsafe_allow_html=True)

# مساحة فارغة صغيرة
st.write("")

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        st.markdown(
            """
            <div style="background-color:#f0f9f5; padding:20px; border-radius:10px; text-align:center;">
                <h4 style="color:#066d66;">✍️ كتابة نص جديد</h4>
                <p style="color:#555;">أدخل نصًا أو تغريدة تريد تحليل مشاعرها</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")
    text_input = st.text_area("✍️ أدخل التغريدة أو النص هنا:", height=150, placeholder="اكتب هنا...")
    if st.button("🔍 تحليل النص", use_container_width=True):
        if text_input.strip() != "":
            st.session_state['text'] = text_input
            st.session_state['navigate'] = True
            st.success("✅ تم حفظ النص! يتم الانتقال إلى صفحة التحليل...")
        else:
            st.warning("⚠️ يرجى إدخال نص قبل الضغط على زر التحليل.")

with col2:
    with st.container():
        st.markdown(
            """
            <div style="background-color:#f0f5f9; padding:20px; border-radius:10px; text-align:center;">
                <h4 style="color:#054a77;">🌟 استخدام تغريدة جاهزة</h4>
                <p style="color:#555;">اختر من أمثلة تغريدات معدة مسبقًا</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.write("")
    if st.button("📋 عرض أمثلة تغريدات", use_container_width=True):
        st.switch_page("pages/page_0_examples.py")

# التنقل التلقائي إلى صفحة التحليل
if st.session_state.get('navigate', False):
    st.switch_page("pages/page_2_analysis.py")
