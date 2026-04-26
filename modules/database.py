# modules/database.py

import pandas as pd
import os

FILE_DB = r"E:\A KULIAH\SEMESTER 5 6\MAGANG\dashboardLKSA\generatesurat\database\surat.xlsx"

def simpan_data(data):
    if os.path.exists(FILE_DB):
        df = pd.read_excel(FILE_DB)
    else:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(FILE_DB, index=False)

def load_data():
    if os.path.exists(FILE_DB):
        return pd.read_excel(FILE_DB)
    return pd.DataFrame()