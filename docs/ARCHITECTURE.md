# Teknik Mimari

## Genel yaklaşım

Uygulama, gerçek kurum ağına erişmeden NetSecOps süreçlerini gösterebilmek için simülasyon modunda tasarlanmıştır. Girdi verileri JSON dosyalarından alınır; bütün çıktılar proje içindeki `data` klasöründe saklanır.

```text
Kullanıcı / CLI
      |
      v
   main.py
      |
      +--> Varlık keşfi ------> Envanter JSON
      +--> Port denetimi -----> Risk raporu JSON
      +--> Loopback TCP lab --> Gerçek Socket bağlantı testi
      +--> Config yedekleme --> Zaman damgalı yedekler
      +--> Diff analizi ------> Değişiklik raporu
      |
      v
Tam denetim iş akışı --> JSON + metin özeti + uygulama günlüğü
```

## Güvenlik kontrolleri

- Çalışma modu yalnızca simüle edilmiş cihaz kayıtlarını kullanır.
- Gerçek Socket bağlantı testi yalnızca `127.0.0.1` loopback adresini kabul eder.
- Her IP adresi `allowed_network` CIDR sınırı içinde doğrulanır.
- IP, MAC, hostname ve port alanları çalıştırma öncesinde kontrol edilir.
- Gerçek cihaz bilgileri için ayrılan `config/devices.json` Git tarafından dışlanır.
- Parola, ortam değişkeni, PEM ve özel anahtar dosyaları Git dışında tutulur.
- Bildirimler ağ üzerinden gönderilmez; yerel rapor ve log olarak üretilir.

## Modüller

- `discovery.py`: Örnek cihazları doğrular ve envanter kaydı üretir.
- `port_scan.py`: İzlenen portları risk seviyelerine ayırır.
- `local_socket_lab.py`: Geçici loopback servisiyle gerçek TCP bağlantı testini gösterir.
- `config_backup.py`: Config sürümlerini cihaz bazlı arşivler, SHA-256 metadata üretir ve son iki doğrulanmış yedeği seçer.
- `config_tracking.py`: Yedekleme, bütünlük kontrolü ve diff analizini tek akışta birleştirir.
- `diff_check.py`: Eklenen ve silinen satırları karşılaştırır; kritik değişiklikleri belirler.
- `workflow.py`: Bütün modülleri tek bir denetim akışında birleştirir.
- `validation.py`: Girdi şeması ve izinli ağ sınırı kontrollerini uygular.
- `app_logging.py`: Uygulama günlüklerini boyut kontrollü şekilde saklar.

Örnek switch yapılandırmaları `fixtures/configs` altında kaynak veri olarak tutulur. Üretilen zaman damgalı kopyalar Git'e eklenmeyen `data/backups/<device_name>` klasörüne yazılır. Her `.txt` yedeğinin yanında dosya boyutu, oluşturulma zamanı ve SHA-256 özetini taşıyan `.metadata.json` kaydı bulunur. Diff işlemi yalnızca son iki yedek metadata ile eşleşirse çalışır.
