# Geliştirme Aşamaları

## Tamamlanan aşamalar

### 1. Aşama - Proje iskeleti ve simüle envanter

- Modüler Python klasör yapısı
- Simüle IP, MAC ve cihaz envanteri
- JSON tabanlı çıktı yapısı
- Git deposu ve temel dokümantasyon

### 2. Aşama - Port ve risk denetimi

- Kritik port risk sınıflandırması
- Yalnızca loopback üzerinde gerçek TCP Socket laboratuvarı
- CIDR ve veri şeması doğrulaması
- Birleşik raporlama, loglama ve otomatik test altyapısı

### 3. Aşama - Config yedekleme ve değişiklik takibi

- Cihaz bazlı zaman damgalı config arşivi
- Her yedek için SHA-256 bütünlük metadata kaydı
- Son iki doğrulanmış yedeğin otomatik seçimi
- VLAN ve ACL değişikliklerinin satır bazlı karşılaştırılması
- Kritik kural ekleme/silme uyarıları

## Sonraki aşama

### 4. Aşama - Entegrasyon ve bildirim geliştirmeleri

- Tam denetim akışı ve CLI menüsü modülleri birleştirir.
- Webhook bildirimi varsayılan kapalı ve ortam değişkeni tabanlıdır.
- HTTPS veya loopback HTTP hedef kontrolü uygulanır.
- Bildirim sonucu JSON/metin raporlarına eklenir.

Bu aşama tamamlandı. Sonraki çalışma, nihai dokümantasyon ve sunum çıktılarıdır.
