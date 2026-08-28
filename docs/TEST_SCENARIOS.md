# Test Senaryoları

## Otomatik testler

| Senaryo | Beklenen sonuç |
|---|---|
| Riskli Telnet portu açık | Port 23 yüksek risk olarak sınıflandırılır |
| İzleme listesi dışındaki port | Rapor sonucuna dahil edilmez |
| `permit ip any any` eklenmesi | Kritik config uyarısı oluşur |
| `deny ip any any` satırının silinmesi | Kritik config uyarısı oluşur |
| Aynı config dosyalarının karşılaştırılması | Değişiklik ve alarm oluşmaz |
| CIDR dışındaki simüle IP | Veri doğrulaması işlemi durdurur |
| Hatalı MAC adresi | Veri doğrulaması işlemi durdurur |
| Birleşik denetim özeti | Cihaz, port, risk ve alarm sayıları doğru hesaplanır |
| Geçici loopback TCP servisi | Açık port olarak algılanır |
| Loopback dışı TCP hedefi | Güvenlik sınırı nedeniyle reddedilir |
| Config yedeği oluşturma | Config ve SHA-256 metadata dosyaları birlikte oluşur |
| Yedek içeriğinin sonradan değiştirilmesi | Bütünlük doğrulaması başarısız olur |
| Güvensiz cihaz klasör adı | Dizin geçişi girişimi reddedilir |
| İkiden az config yedeği | Karşılaştırma açıklayıcı hatayla durur |
| Birden fazla config yedeği | Zaman sırasına göre son iki doğrulanmış yedek seçilir |

Test komutu:

```powershell
python -m unittest discover -s tests -v
```

## Manuel kabul testi

1. `python main.py --run all` komutu çalıştırılır.
2. Konsolda üç cihaz ve altı simüle açık port raporlandığı görülür.
3. İki yüksek riskli port bulgusunun bulunduğu doğrulanır.
4. VLAN 10'dan VLAN 20'ye geçiş diff çıktısında kontrol edilir.
5. Güvenli `deny` kuralının kaldırılması ve geniş `permit` kuralının eklenmesi için iki kritik uyarı doğrulanır.
6. `data/reports` altında JSON ve metin özetlerinin oluştuğu kontrol edilir.
7. `logs/app.log` içinde denetimin başlangıç ve bitiş kayıtları doğrulanır.
8. Loopback Socket laboratuvarında bir açık ve bir kapalı port görüldüğü doğrulanır.
9. Config işlemi çıktısında önceki/güncel yedek adları ile başarılı bütünlük kontrolü görülür.
10. Yedeklerin yanında oluşan metadata kayıtlarında SHA-256 değerleri kontrol edilir.
