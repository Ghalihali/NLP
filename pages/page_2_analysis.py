import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

# إعداد الصفحة
st.set_page_config(
    page_title="نتيجة تحليل المشاعر",
    page_icon="📊",
    layout="centered"
)

# عرض الشعار
st.image("logo.png", width=120)

# عنوان الصفحة
st.markdown("<h1 style='color:#4CAF50; text-align:center;'>📊 نتيجة تحليل المشاعر</h1>", unsafe_allow_html=True)

# تحميل النموذج مع التخزين المؤقت
@st.cache_resource
def load_model():
    model_name = "aubmindlab/bert-base-arabertv02-twitter"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    return tokenizer, model

tokenizer, model = load_model()

# دالة تنظيف النصوص العربية والتغريدات
def arabic_clean(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" 
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ؤ', 'و', text)
    text = re.sub(r'ئ', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'[^؀-ۿa-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# دالة التصنيف النهائية مع تعزيز الذكاء
def classify_sentiment(text):
    cleaned_text = arabic_clean(text)

    # تعزيز النص لو قصير
    enhanced_text = cleaned_text
    if len(cleaned_text.split()) < 3:
        enhanced_text = f"اشعر أنني {cleaned_text}"

    # تمرير للنموذج
    inputs = tokenizer(enhanced_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1).squeeze()

    # قراءة النسب
    negative_prob = probs[0].item()
    neutral_prob = probs[1].item()
    positive_prob = probs[2].item()

    # كشف الكلمات السلبية أو الإيجابية
    negative_words = ['حزين', 'زعلان', 'تعبان', 'ضايق', 'احباط', 'متعب', 'توتر', 'ارهاق', 'ضغوط', 'تأجيل', 'حزن', 'تأخير']
    positive_words = ['فرح', 'نجاح', 'سعيد', 'الحمد لله', 'فخور', 'متحمس', 'فرحة', 'استمتعت', 'رائع']

    has_negative_word = any(word in cleaned_text for word in negative_words)
    has_positive_word = any(word in cleaned_text for word in positive_words)

    # المنطق النهائي المعدل:
    if has_negative_word:
        return "سلبي 😞"
    elif positive_prob > max(negative_prob, neutral_prob) or has_positive_word:
        return "إيجابي 😊"
    elif negative_prob > max(neutral_prob, positive_prob):
        return "سلبي 😞"
    else:
        return "محايد 😐"


# الواجهة مع المستخدم
if 'text' in st.session_state and st.session_state['text']:
    text = st.session_state['text']

    with st.container():
        st.markdown("<h4 style='text-align: center;'>✅ النص الذي قمت بتحليله:</h4>", unsafe_allow_html=True)
        st.info(text)

        with st.spinner('⏳ جاري تحليل النص...'):
            sentiment = classify_sentiment(text)

        st.markdown("<h4 style='text-align: center;'>🔍 نتيجة التحليل:</h4>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color:#d4edda;padding:20px;border-radius:10px;margin-top:20px;">
                <h2 style='text-align: center; color: #155724;'>{sentiment}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <br><div style="text-align: center;">
            <a href="/app" target="_self">
                <button style='background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;'>⬅️ العودة إلى الصفحة الرئيسية</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.warning("⚠️ لم يتم إدخال نص بعد. الرجاء العودة للصفحة الرئيسية وإدخال نص أو اختيار تغريدة.")
