# NetSecOps - Nihai Proje Raporu

## 1. Proje özeti

NetSecOps, ağ varlıklarının görünürlüğünü, kritik port risklerini ve ağ cihazı yapılandırma değişikliklerini tek bir Python komut satırı uygulamasında göstermeyi amaçlayan modüler bir laboratuvar prototipidir.

Proje gerçek kurum ağına bağlanmaz. Varlık ve port verileri kontrollü JSON dosyalarından, yapılandırma sürümleri ise `fixtures/configs` altındaki örneklerden alınır. TCP bağlantı testi yalnızca geçici `127.0.0.1` loopback servisi üzerinde yapılır.

## 2. Amaç ve kapsam

- IP, MAC ve hostname bilgileriyle simüle cihaz envanteri oluşturmak
- İzlenen portları risk seviyelerine göre sınıflandırmak
- Yetkisiz erişim senaryolarını config diff ile görünür kılmak
- Zaman damgalı config yedekleri ve SHA-256 bütünlük metadata üretmek
- Son iki doğrulanmış yedeği karşılaştırmak
- JSON, metin raporu ve uygulama günlüğü üretmek
- Varsayılan kapalı, güvenlik kontrollü webhook bildirim altyapısı sağlamak

## 3. Teknik mimari

`main.py` CLI menüsünü ve otomasyon seçeneklerini yönetir. `workflow.py` tüm denetimleri birleştirir. `discovery.py`, `port_scan.py`, `local_socket_lab.py`, `config_backup.py`, `config_tracking.py` ve `diff_check.py` işlevsel modüllerdir. `validation.py` CIDR, IP, MAC, port ve config ayarlarını çalıştırma öncesinde doğrular. Ayrıntılı mimari için [ARCHITECTURE.md](ARCHITECTURE.md) dosyasına bakılabilir.

## 4. Uygulama akışı

1. `config/settings.json` ve `config/simulated_network.json` okunur.
2. Cihaz kayıtları izinli `192.168.56.0/24` CIDR ağı içinde doğrulanır.
3. Simüle envanter ve port-risk raporları oluşturulur.
4. Loopback üzerinde geçici TCP servisi açılır; açık ve kapalı port durumu gerçek `socket` bağlantısıyla doğrulanır.
5. `baseline` ve `changed` config örnekleri cihaz bazlı yedek klasörüne yazılır.
6. Her yedek için SHA-256, boyut, sürüm ve zaman bilgisi metadata dosyasına yazılır.
7. Son iki doğrulanmış yedek karşılaştırılır; VLAN ve ACL değişiklikleri raporlanır.
8. Kritik değişiklikler yerel rapora yazılır. Webhook yalnızca açıkça etkinleştirilir ve URL ortam değişkeninden alınır.

## 5. Örnek test çıktısı

`python main.py --run all` çalıştırıldığında simülasyon için beklenen temel özet:

| Ölçüm | Sonuç |
|---|---:|
| Simüle cihaz | 3 |
| Simüle açık port | 6 |
| Yüksek riskli port bulgusu | 2 |
| Kritik config değişikliği | 2 |
| Loopback açık TCP portu | 1 |
| Varsayılan webhook durumu | disabled |

Kritik config örneği, `deny ip any any log` satırının silinmesi ve geniş `permit ip any any` kuralının eklenmesidir.

## 6. Test ve kalite kanıtı

- Yerel otomatik test sayısı: 22
- Test komutu: `python -m unittest discover -s tests -v`
- CI matrisi: Python 3.10, 3.12 ve 3.13
- Smoke test: `python main.py --run all`
- GitHub Actions sonucu: başarılı
- Windows UTF-8 konsol davranışı ayrıca test edilmiştir.

## 7. Güvenlik sınırları ve sınırlılıklar

Bu prototip gerçek ARP taraması, gerçek kurumsal IP taraması veya Netmiko ile gerçek cihaza SSH bağlantısı yapmaz. Bu sınır, yetkisiz erişimi önlemek ve staj ortamında güvenli tekrar üretilebilirlik sağlamak için bilinçli olarak seçilmiştir. Yetkili bir GNS3, Cisco Packet Tracer veya host-only sanal ağ hazırlandığında ARP ve Netmiko adaptörleri ayrı bir genişletme aşaması olarak eklenebilir.

Webhook gönderimi varsayılan olarak kapalıdır. Aktifleştirme, yalnızca yetkili test ortamında `notifications.enabled=true` ve `NETSECOPS_WEBHOOK_URL` ortam değişkeniyle yapılmalıdır.

## 8. Çalıştırma

```powershell
cd C:\Projects\NetSecOps-Staj
python main.py
python main.py --run all
python -m unittest discover -s tests -v
```

Teknik sunum: [NetSecOps_Teknik_Sunum.pptx](NetSecOps_Teknik_Sunum.pptx)

## 9. Sonuç

Proje; envanter, port/risk değerlendirmesi, yapılandırma yedekleme, bütünlük kontrolü, diff analizi, raporlama, loglama ve güvenli bildirim tasarımını çalışan bir simülasyon akışında birleştirmiştir. Bu yapı, staj sunumunda hem Python otomasyonunu hem de güvenlik operasyonu düşüncesini gösterecek bir temel sağlar.
