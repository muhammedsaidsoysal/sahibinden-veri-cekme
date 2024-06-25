from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import requests
import matplotlib.pyplot as plt
import logging

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Görsellerin kaydedileceği klasörü oluştur
os.makedirs("images", exist_ok=True)

driver = webdriver.Firefox()
driver.get("https://google.com")
driver.maximize_window()
time.sleep(4)
input_element = driver.find_element(By.NAME, 'q')  # ID yerine NAME kullanarak daha güvenli bir seçim yaptık
input_element.send_keys("sahibinden.com", Keys.ENTER)
time.sleep(6)
link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a h3'))  # Daha genel bir seçici kullanarak linki buluyoruz
)
link.click()
time.sleep(5)
# Çerez reddetme butonu
try:
    search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-reject-all-handler"))) #çerezleri reddediyoruz
    search.click()
except:
    pass

input_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'searchText'))  # ID kullanarak daha güvenilir bir seçim yaptık
)
input_element.send_keys("elazığ merkez satilik daire", Keys.ENTER)
time.sleep(7)

# 'Arama Kaydet' butonu
arama_kaydet = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]")))
arama_kaydet.click()
mahalleler = []
fiyatlar = []
data_list = []
max_pages = 50  # İstediğiniz sayfa sayısını burada belirleyin
current_page_number = 1

try:
    while current_page_number <= max_pages:
        mahalle_elementleri = driver.find_elements(By.CLASS_NAME, "searchResultsLocationValue")
        for mahalle_element in mahalle_elementleri:
            mahalleler.append(mahalle_element.text)
        fiyat_elementleri = driver.find_elements(By.CLASS_NAME, 'searchResultsPriceValue')
        for fiyat_element in fiyat_elementleri:
            fiyat_text = fiyat_element.text.replace(' TL', '').replace('.', '').strip()
            if fiyat_text.isdigit():
                fiyatlar.append(int(fiyat_text))
        tum_veriler = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsItem"))
        )
        current_url = driver.current_url
        logging.info(f'Sayfa {current_page_number} - URL: {current_url}')
        #with open("link.txt", "a", encoding="utf-8") as file:  # 'w' yerine 'a' kullanarak dosyaya ekleme yapıyoruz
        # for element in tum_veriler:  txt formatında kaydetmek için kullanabiliriz
        #     content_text = element.text
        #     href_elements = element.find_elements(By.TAG_NAME, "a") 
        #     href = href_elements[0].get_attribute("href") if href_elements else "No link available"

        for element in tum_veriler:
            content_text = element.text
            href_elements = element.find_elements(By.TAG_NAME, "a")
            href = href_elements[0].get_attribute("href") if href_elements else "No link available"

            # İlan resmini indir ve kaydet
            image_elements = element.find_elements(By.TAG_NAME, "img")
            if image_elements:
                image_url = image_elements[0].get_attribute("src")
                image_name = os.path.join("images", f"{current_page_number}_{len(data_list)}.jpg")
                with open(image_name, "wb") as img_file:
                    img_file.write(requests.get(image_url).content)

            # Verileri JSON formatında saklamak için dict oluşturuyoruz
            data = {
                "content_text": content_text,
                "href": href,
                "image": image_name if image_elements else "No image available"
            }
            data_list.append(data)

        # Verileri dosyaya JSON formatında kaydediyoruz
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)

        if current_page_number == max_pages:
            logging.info("İstenen sayfa sayısına ulaşıldı.")
            break

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.prevNextBut[title="Sonraki"]'))
        )

        current_page = driver.current_url
        next_button.click()
        time.sleep(10)

        new_page = driver.current_url

        if current_page == new_page:
            logging.info("Son sayfaya ulaşıldı veya döngü algılandı.")
            break

        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))

        # Sayfayı kaydırarak yeni öğelerin yüklenmesini sağlıyoruz
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        current_page_number += 1

except Exception as e:
    logging.error(f"Hata: {e}")

driver.close()

# plt.hist(mahalleler, bins=60, edgecolor='white')
# plt.xlabel('Mahalle')
# plt.ylabel('Mahalle Sayısı')
# plt.title('Elazığ Merkez Mahalle Histogramı')
# plt.savefig('mahalle_histogram.png')
# plt.show()
# Veri görselleştirme: İlan başlıklarının uzunluğunun dağılımı
title_lengths = [len(data["content_text"]) for data in data_list]
plt.hist(title_lengths, bins=20, edgecolor='black')
plt.title('İlan Başlıklarının Uzunluk Dağılımı')
plt.xlabel('Başlık Uzunluğu')
plt.ylabel('Frekans')
plt.savefig('title_lengths_histogram.png')
plt.show()
plt.hist(fiyatlar, bins=30, edgecolor='black')
plt.xlabel('Fiyat (Milyon TL)')
plt.ylabel('İlan Sayısı')
plt.title('Elazığ Merkez Satılık Daire Fiyatları Histogramı')
plt.savefig('fiyat_histogram.png')
plt.show()