# NetSecOps Laboratory

Bu proje, staj kapsamında ağ varlık envanteri, port/risk denetimi ve yapılandırma değişikliği takibini göstermek amacıyla hazırlanmış simüle edilmiş bir laboratuvar uygulamasıdır.

## Kapsam

- Simüle edilmiş IP, MAC ve cihaz envanteri
- Tanımlı kritik portların risk değerlendirmesi
- Zaman damgalı örnek yapılandırma yedekleri
- Cihaz bazlı yedek geçmişi ve SHA-256 bütünlük doğrulaması
- Satır bazlı yapılandırma fark analizi ve kritik değişiklik uyarısı
- JSON tabanlı envanter ve rapor çıktıları
- Yalnızca loopback üzerinde çalışan gerçek TCP Socket laboratuvarı

## Güvenlik sınırı

Uygulama yalnızca `config/simulated_network.json` içindeki örnek laboratuvar verileriyle çalışır. Socket deneyi yalnızca `127.0.0.1` loopback adresinde geçici bir test servisi açar ve kod başka hedefleri reddeder. Gerçek kurum ağına bağlantı, gerçek IP taraması veya gerçek cihazlara SSH erişimi içermez.

## Çalıştırma

Python 3.10 veya daha yeni bir sürüm gereklidir. Harici Python paketi gerekmez.

```powershell
python main.py
```

Menüden sırasıyla varlık keşfi, port/risk denetimi veya config yedekleme ve diff işlemi seçilebilir.

Tüm denetimleri tek komutla çalıştırmak için:

```powershell
python main.py --run all
```

Diğer otomasyon seçenekleri `discovery`, `ports`, `config` ve `local` değerleridir.

## Testler

```powershell
python -m unittest discover -s tests -v
```

## Dosya açıklamaları

- `config/`: Uygulama ayarları ve simüle edilmiş cihaz verileri
- `fixtures/`: Karşılaştırma için kontrollü laboratuvar config örnekleri
- `modules/`: Uygulamanın işlevsel modülleri
- `data/inventory/`: Oluşturulan envanter kayıtları
- `data/backups/`: Örnek yapılandırma yedekleri
- `data/reports/`: Port ve fark analizi raporları
- `logs/`: Boyut kontrollü uygulama günlükleri
- `tests/`: Otomatik birim ve güvenlik sınırı testleri
- `docs/`: Teknik mimari ve test senaryoları

Her `main` dalı güncellemesinde GitHub Actions, otomatik testleri farklı Python sürümlerinde çalıştırır ve tam denetim için smoke test uygular.

## Config değişiklik takip akışı

1. `baseline` ve `changed` laboratuvar config dosyaları cihaz klasörüne zaman damgalı olarak yedeklenir.
2. Her yedeğin dosya adı, boyutu ve SHA-256 özeti ayrı metadata kaydında tutulur.
3. Cihazın son iki yedeği otomatik seçilir ve karşılaştırma öncesinde bütünlükleri doğrulanır.
4. VLAN, ACL ve erişim kuralı değişiklikleri satır bazlı diff raporuna yazılır.
5. Güvenli bir `deny` kuralının kaldırılması veya geniş bir `permit` kuralının eklenmesi kritik alarm üretir.

## Staj raporu için not

Çalışma, kurumsal güvenlik politikalarına uygun biçimde simüle edilmiş laboratuvar verileri üzerinde tasarlanmıştır. Hedef, ağ güvenliği süreçlerinde envanter yönetimi, risk görünürlüğü ve değişiklik takibinin otomasyonla nasıl desteklenebileceğini göstermektir.
