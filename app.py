import os
import streamlit as st
import google.generativeai as genai

# ---------------------------------------------------------
# 1. API ANAHTARINI BURAYA YAPIŞTIR
# ---------------------------------------------------------
API_KEY = AQ.Ab8RN6KjQBEyVzmmmmlplXvTGm278613m-XwVR6WORHQP-8fjw
genai.configure(api_key=API_KEY)

# ---------------------------------------------------------
# 2. SAYFA VE ARAYÜZ AYARLARI
# ---------------------------------------------------------
st.set_page_config(page_title="Akıllı Ders Asistanı", layout="centered", page_icon="🎓")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 Akıllı Ders Notu Asistanı")
st.caption("Ders slaytını yükle, sesi kaydet; A4 formatında temiz ders notunu anında al.")

# ---------------------------------------------------------
# 3. DOSYA YÜKLEME VE SES KAYDI
# ---------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    pdf_file = st.file_uploader("1. Slayt / PDF Yükle", type=["pdf"])

with col2:
    audio_file = st.audio_input("2. Dersi Kaydet (Mikrofon)")

# ---------------------------------------------------------
# 4. İŞLEME VE DERS NOTU MOTORU
# ---------------------------------------------------------
if st.button("🚀 Dersi Analiz Et ve A4 Notu Çıkar", type="primary"):
    if not audio_file:
        st.error("Lütfen ders ses kaydını tamamla.")
    else:
        with st.spinner("Ses ve kaynak taranıyor, A4 ders notu hazırlanıyor..."):
            try:
                system_instruction = """
                Sen dünyanın en başarılı, düzenli üniversite öğrencisisin. 
                Sana verilen ses kaydı ve referans slaytı/PDF'i harmanlayarak doğrudan çalışmaya hazır, temiz bir A4 ders notu hazırla.

                KURALLAR:
                1. GEREKSİZLERİ AT: Hocanın laf kalabalığını, esprilerini, sınıf uyarılarını ve dolgu kelimelerini filtrele.
                2. SLAYT + SES SENTEZİ: Slayttaki iskelet yapıyı hocanın sözlü detaylarıyla birleştir.
                3. SÖZLÜ DETAYLAR: Slaytta olmayan ama hocanın sözlü aktardığı kritik noktaları `> 💡 HOCANIN SÖZLÜ EKLEMESİ:` olarak yaz.
                4. SINAV VURGULARI: 'Burası sınavda çıkar', 'önemli' denen yerleri `> ⚠️ SINAV / KRİTİK NOKTA:` olarak belirt.
                5. HİYERARŞİ: Markdown başlıkları (#, ##, ###), maddeler ve karşılaştırmalı tablolar kullan. En sona 3 maddelik '🎯 Hızlı Sınav Tekrarı' ekle.
                """

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_instruction
                )

                contents = []

                # PDF Varsa ekle
                if pdf_file:
                    pdf_bytes = pdf_file.read()
                    contents.append({
                        "mime_type": "application/pdf",
                        "data": pdf_bytes
                    })

                # Ses dosyasını ekle
                audio_bytes = audio_file.read()
                contents.append({
                    "mime_type": "audio/wav",
                    "data": audio_bytes
                })

                contents.append("Ders kaydını ve slaytı analiz edip kurallara uygun eksiksiz ders notunu çıkar.")

                # Üretim
                response = model.generate_content(contents)

                st.success("Ders notu hazırlandı!")
                st.markdown("---")
                st.markdown(response.text)

                # Notu İndirme Butonu
                st.download_button(
                    label="📥 Notu İndir (.md / Yazı)",
                    data=response.text,
                    file_name="ders_notu.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
