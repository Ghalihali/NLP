import streamlit as st
import re

# إعداد الصفحة
st.set_page_config(
    page_title="اختيار تغريدة جاهزة",
    page_icon="💬",
    layout="centered"
)

# 🖼️ عرض شعار المشروع
st.image("logo.png", width=120)

# عنوان الصفحة مع وصف بسيط
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50; margin-top:20px;'>🌟 اختر تغريدة جاهزة وجرب التحليل!</h1>
    <p style='text-align: center; font-size:18px; color:#555;'>اختر نصًا يعبر بوضوح عن مشاعر إيجابية أو سلبية أو محايدة 👇</p>
    """,
    unsafe_allow_html=True
)

# قائمة أمثلة التغريدات
examples = [
    "لم أتمكن من إنهاء مشروعي الجامعي بالشكل المطلوب، وأشعر بإحباط شديد وخيبة أمل.",
    "الدراسة عن بعد كانت متعبة جدًا وأشعرتني بالإحباط الشديد 😓",
    "أشعر بفرحة غامرة بعد حضور ورشة عمل عن الابتكار اليوم! 🚀",
    "كان الجو اليوم رائعًا في عسير، استمتعت بطلعة برية لا مثيل لها 🌵☀️",
    "أشعر بالحزن الشديد بسبب تأجيل اختبارنا النهائي بدون سبب 😞",
    "استمتعت بكل لحظة اليوم خلال زيارتي لمعرض الكتاب بالرياض، يوم لا ينسى 📚❤️",
    "شعرت بالإرهاق الشديد اليوم بسبب تأخر الحافلة واضطراري للمشي طويلاً 😡",
    "أنا متحمس جدًا لبدء التدريب التعاوني الأسبوع القادم إن شاء الله 🙏",
    "أنا متوتر جدًا بسبب ضغط مشروع التخرج، دعواتكم لي 🤲",
    "الحمد لله أنجزت حفظ جزء جديد من القرآن الكريم، شعور رائع لا يوصف 🌸📖"
]

# قائمة كلمات إيجابية يجب حذفها من النصوص السلبية
positive_words = ['الحمد لله', 'استمتعت', 'فرحة', 'رائع', 'متحمس', 'سعيد', 'نجاح', 'فخور', 'فرحت']

# دالة لحذف الكلمات الإيجابية من النص إذا كان سلبي
def clean_negative_text(text):
    # إذا النص يحتوي كلمات سلبية مع كلمات إيجابية، نحذف الإيجابية
    negative_keywords = ['حزين', 'احباط', 'زعلان', 'متعب', 'ضايق', 'توتر', 'ارهاق', 'ضغوط', 'تأجيل', 'غضب']
    if any(word in text for word in negative_keywords):
        for pos_word in positive_words:
            text = re.sub(r'\b{}\b'.format(re.escape(pos_word)), '', text)
    return text.strip()

# عرض التغريدات لاختيارها
with st.container():
    selected_example = st.radio(
        "📝 اختر تغريدة:",
        examples,
        index=0,
        help="اختر نصًا جاهزًا لتجربة التحليل."
    )

# زر استخدام التغريدة
st.write("")
if st.button("✅ استخدام هذه التغريدة للتحليل", use_container_width=True):
    cleaned_text = clean_negative_text(selected_example)
    st.session_state['text'] = cleaned_text
    st.session_state['navigate'] = True
    st.success("✅ تم اختيار النص! يتم الآن الانتقال إلى صفحة عرض التحليل...")

# زر للرجوع للصفحة الرئيسية
st.write("")
st.markdown(
    """
    <div style="text-align: center; margin-top:20px;">
        <a href="/app" target="_self">
            <button style='background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:8px;font-size:16px;'>⬅️ كتابة تغريدة جديدة</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# التنقل التلقائي إلى صفحة التحليل
if st.session_state.get('navigate', False):
    st.switch_page("pages/page_2_analysis.py")
