import pandas as pd
from sqlalchemy import create_engine
import time

# 1. Bağlantı (Lokalden Docker'daki Postgres'e bağlanıyoruz)
DB_URL = "postgresql://postgres:123456@localhost:5432/arabam_db"
engine = create_engine(DB_URL)

print("Veri okunuyor...")
start_time = time.time()

# 2. Temiz veriyi oku (CSV veya Parquet)
#df = pd.read_parquet("arabam_temiz_veri.parquet")
df = pd.read_csv("scripts/arabam_temiz_veri.csv")

print(f"Toplam {len(df)} satır veritabanına aktarılıyor...")

# 3. Toplu yükleme (10.000'er satırlık chunk'lar halinde)
df.to_sql(
    name="car_listings",
    con=engine,
    if_exists="replace",  # Varsa tabloyu baştan yaratır
    index=False,
    chunksize=10000,
    method="multi"
)

print(f"Tamamlandı! Geçen süre: {round(time.time() - start_time, 2)} saniye.")