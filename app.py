import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. API ANAHTARINI BURAYA YAPIŞTIR (AQ. ile başlayanı kabul eder)
# ---------------------------------------------------------
API_KEY = "AQ.Ab8RN6LEXd6EJmLUfRn5tYC1HPGADb_rquvkVwW3x02Wbi1bWA"

client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------
# 2. SAYFA VE ARAYÜZ AYARLARI
# ---------------------------------------------------------
st.set_page_config(page_title="Akıllı Ders Asistanı", layout="centered", page_icon="🎓")

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
                Sen üniversite derslerini kusursuz özetleyen zeki bir öğrencisin.
                Sana verilen ses kaydı ve referans slaytı sentezleyerek doğrudan çalışmaya hazır, temiz bir A4 ders notu hazırla.

                KURALLAR:
                1. GEREKSİZLERİ AT: Hocanın laf kalabalığını, esprilerini ve sınıf uyarılarını filtrele.
                2. SLAYT + SES SENTEZİ: Slayttaki iskelet yapıyı hocanın sözlü detaylarıyla birleştir.
                3. SÖZLÜ DETAYLAR: Slaytta olmayan ama hocanın anlattığı noktaları `> 💡 HOCANIN SÖZLÜ EKLEMESİ:` olarak yaz.
                4. SINAV VURGULARI: 'Burası sınavda çıkar', 'önemli' denen yerleri `> ⚠️ SINAV / KRİTİK NOKTA:` olarak belirt.
                5. HİYERARŞİ: Markdown başlıkları (#, ##, ###), maddeler ve karşılaştırmalı tablolar kullan. En sona 3 maddelik '🎯 Hızlı Sınav Tekrarı' ekle.
                """

                contents = []

                # PDF Varsa ekle
                if pdf_file:
                    contents.append(
                        types.Part.from_bytes(
                            data=pdf_file.read(),
                            mime_type="application/pdf",
                        )
                    )

                # Ses dosyasını ekle
                contents.append(
                    types.Part.from_bytes(
                        data=audio_file.read(),
                        mime_type="audio/wav",
                    )
                )

                contents.append("Ders kaydını ve slaytı analiz edip kurallara uygun eksiksiz ders notunu çıkar.")

                # Yeni SDK Çağrısı
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                    ),
                )

                st.success("Ders notu hazırlandı!")
                st.markdown("---")
                st.markdown(response.text)

                # İndirme Butonu
                st.download_button(
                    label="📥 Notu İndir (.md)",
                    data=response.text,
                    file_name="ders_notu.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")
