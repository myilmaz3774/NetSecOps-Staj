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

Test komutu:

```powershell
python -m unittest discover -s tests -v
```

## Manuel kabul testi

1. `python main.py --run all` komutu çalıştırılır.
2. Konsolda üç cihaz ve altı açık port raporlandığı görülür.
3. İki yüksek riskli port bulgusunun bulunduğu doğrulanır.
4. VLAN 10'dan VLAN 20'ye geçiş diff çıktısında kontrol edilir.
5. Güvenli `deny` kuralının kaldırılması ve geniş `permit` kuralının eklenmesi için iki kritik uyarı doğrulanır.
6. `data/reports` altında JSON ve metin özetlerinin oluştuğu kontrol edilir.
7. `logs/app.log` içinde denetimin başlangıç ve bitiş kayıtları doğrulanır.
