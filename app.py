import streamlit as st
import pandas as pd

# Sayfa tasarımı ve başlıklar
st.set_page_config(page_title="Adaptive Career AI", layout="centered")

st.title("Sana Uygun Kariyer Yolunu Yapay Zeka ile Bul 🚀")
st.write("Becerilerini seç, yapay zeka sana en uygun meslekleri, uygunluk skorunu ve eksiklerini söylesin.")

# Veriyi okuma
df = pd.read_csv("meslek_verileri.csv")

# Tablodaki tüm becerileri ayıklayıp çoklu seçim listesi oluşturma
tum_beceriler = set()
for beceriler in df['Gereken Beceriler']:
    for b in beceriler.split(','):
        tum_beceriler.add(b.strip())
tum_beceriler = sorted(list(tum_beceriler))

st.subheader("1. Kendini Tanıt")
secilen_beceriler = st.multiselect("Hangi becerilere sahipsin? (Listeden seçebilirsin)", tum_beceriler)

# Butona basıldığında çalışacak yapay zeka eşleştirme mantığı
if st.button("Kariyer Önerilerimi Getir"):
    if len(secilen_beceriler) > 0:
        st.subheader("Senin İçin En Uygun Kariyerler")
        
        sonuclar = []
        for index, row in df.iterrows():
            meslek_becerileri = [b.strip() for b in row['Gereken Beceriler'].split(',')]
            ortak = set(secilen_beceriler).intersection(meslek_becerileri)
            eksik = set(meslek_becerileri).difference(secilen_beceriler)
            
            # Uygunluk yüzdesi hesaplama
            skor = (len(ortak) / len(meslek_becerileri)) * 100
            
            sonuclar.append({
                "Meslek": row['Meslek'],
                "Skor": skor,
                "Eksik": ", ".join(eksik) if eksik else "Eksiğin yok, harikasın!"
            })
        
        # En yüksek puan alan 3 mesleği sıralama
        sonuc_df = pd.DataFrame(sonuclar).sort_values(by="Skor", ascending=False).head(3)
        
        # Sonuçları ekrana renkli kutularla yazdırma
        for index, row in sonuc_df.iterrows():
            st.success(f"🎯 **{row['Meslek']}** - Uygunluk: %{round(row['Skor'])}")
            st.warning(f"📚 **Öğrenmen Gerekenler (Eksik Beceriler):** {row['Eksik']}")
            st.write("---")
    else:
        st.error("Lütfen devam etmek için en az bir beceri seç.")