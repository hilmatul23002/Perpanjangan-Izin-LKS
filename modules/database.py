# modules/database.py

import pandas as pd
import os

FILE_DB = "database/surat.xlsx"

def simpan_data(data):
    df_new = pd.DataFrame([data])

    if os.path.exists(FILE_DB):
        df_old = pd.read_excel(FILE_DB)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(FILE_DB, index=False)

def load_data():
    if os.path.exists(FILE_DB):
        return pd.read_excel(FILE_DB)
    return pd.DataFrame()
