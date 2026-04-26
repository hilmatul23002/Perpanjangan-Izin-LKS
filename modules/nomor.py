import pandas as pd
import os
from datetime import datetime

FILE_DB = "database/surat.xlsx"

def generate_nomor():
    os.makedirs("database", exist_ok=True)

    now = datetime.now()
    bulan = now.strftime("%m")
    tahun = now.strftime("%Y")

    if not os.path.exists(FILE_DB):
        return f"001/LKS/427.42/{bulan}/{tahun}"

    df = pd.read_excel(FILE_DB)

    if df.empty or "nomor" not in df.columns:
        return f"001/LKS/427.42/{bulan}/{tahun}"

    try:
        # Ambil hanya nomor dengan tahun sekarang
        df["tahun"] = df["nomor"].str.split("/").str[-1]

        df_tahun_ini = df[df["tahun"] == tahun]

        if df_tahun_ini.empty:
            nomor_baru = 1
        else:
            last_nomor = df_tahun_ini.iloc[-1]["nomor"]
            last_urut = int(last_nomor.split("/")[0])
            nomor_baru = last_urut + 1

        return f"{nomor_baru:03d}/LKS/427.42/{bulan}/{tahun}"

    except:
        return f"001/LKS/427.42/{bulan}/{tahun}"