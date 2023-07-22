# WebScrapingMongoDB
Proje Detayı: 

Projeye başlamadan önce gerekli kurulumları yaptım. Python pymongo, requests, bs4 install ettikten sonra daha önce selenıumu kullanarak bir proje yaptığım için web scraping mantığını araştırdıktan sonra requests kütüphanesini kullanarak belirttiğiniz urlleri liste halinde düzenledim ve get isteği ile web sayfasının içeriğini çektim Headers değişkeni ile HTTP başlıklarını(user-Agent bilgisi) gönderdim. BeatifulSoup kütüphanesini kullanarak web sayfa içeriğini html belgesine çevirme işlemini yaptırdım. Artık ilgili linklerden istediğim bilgilerimi çekebilmem için ortamım hazırdı. 

 Gerekli url bilgilerini liste olarak ekedim. Daha sonra bilgileri çekmek için kitapyurdu urli için kişisel gelişim kategorisini kitapsepeti urli içinde çizgi roman kategorisine ait link adreslerini url listeme string olarak ekledim. Daha sonra sayfa kaynaklarını inceleyerek hangi div veya hangi span... vb. Attributes (class, id, href... vb.) içinde ise  price title writers and publisher bilgilerinin yer aldığını inceleyerek find_all fonksiyonu ile bilgilerimi çektikten sonra bir döngü ile her kitap için bir  json formatı ile sizin de belirtmiş olduğunuz collection db ve alan isimleriyle uyumlu olacak şekilde veritabanıma kaydettim. Collection isimlerini kitapyurdu ve kitapsepeti şeklinde güncelleyerek fonksiyonlarımı hazırladım.  

Proje olası bir durumda verileri çekmeden kapatıldığında verileri kaybetmemek için bir dosya oluşturdum. 

 Ben bu dosyayı şu adımlarla oluşturdum: 

 

import tempfile 

# Geçici dosya için uygun dizini alın 

directory = tempfile.mkdtemp()  

# Daha sonra dosya yolunu belirleyebilirsiniz 

TEMP_DATA_FILE = directory + "/temp_data.pkl" 

Daha sonra bu dosya dizinini projemde verdim ve bir fonksiyon içinde veritabanına verileri kaydettikçe bu datayı dosyama yazan bir fonksiyon ekledim. 

Projede datetime ve time kütüphanelerini kullanarak zaman kontrolü yapan ve her gün 12 de çalışacak şekilde geliştirdim.  
