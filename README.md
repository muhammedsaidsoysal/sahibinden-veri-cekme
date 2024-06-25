# sahibinden-veri-cekme
Python programlama dili kullanarak, Selenium ve BeautifulSoup kütüphaneleri yardımıyla sahibinden.com web sitesinden belirli ilan verilerini başarıyla topladım. Bu süreçte, çeşitli ilanlardan mahalle, fiyat, fotoğraf, ilan tarihi, oda sayısı ve m² (Brüt) bilgilerini çekmek üzere detaylı bir web scraping (web kazıma) işlemi gerçekleştirdim. Bu işlemleri daha detaylı bir şekilde aşağıda açıklıyorum:

Kullanılan Kütüphaneler ve Araçlar
Selenium:
Selenium, web tarayıcılarını otomatikleştirmek ve kullanıcı etkileşimlerini simüle etmek için kullanılan güçlü bir araçtır. Bu projede, dinamik içerikleri yükleyebilmek ve sayfalar arasında gezinebilmek için Selenium kullanıldı. Selenium ile birlikte kullanılan Chrome WebDriver, sayfaların otomatik olarak açılıp gezilmesini sağladı.

BeautifulSoup:
BeautifulSoup, HTML ve XML dosyalarını ayrıştırmak ve içeriğini çıkarmak için kullanılan bir Python kütüphanesidir. Bu projede, Selenium ile indirilen sayfa kaynaklarının ayrıştırılması ve gerekli bilgilerin çekilmesi için BeautifulSoup kullanıldı.
