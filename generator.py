import pandas as pd
import numpy as np
import random

def generate_column_data(col_def, n_rows):
    """
    Generate numpy array berdasarkan definisi kolom
    """
    col_type = col_def.get("type", "string")
    
    # 1. Tipe INTEGER
    if col_type == "integer":
        min_val = col_def.get("min", 0)
        max_val = col_def.get("max", 100)
        
        # Menggunakan distribusi uniform jika tidak ada spec distribusi
        # (Bisa dikembangkan ke normal distribution nanti)
        data = np.random.randint(min_val, max_val + 1, size=n_rows)
        return data

    # 2. Tipe FLOAT
    elif col_type == "float":
        min_val = col_def.get("min", 0.0)
        max_val = col_def.get("max", 100.0)
        
        # Gunakan distribusi normal agar data terlihat "organik" (seperti nilai, suhu, dll)
        # Asumsi mean ada di tengah, std dev 1/6 dari range (supaya 99% data masuk range)
        mean_val = col_def.get("mean", (min_val + max_val) / 2)
        std_dev = (max_val - min_val) / 6 if max_val != min_val else 1
        
        data = np.random.normal(loc=mean_val, scale=std_dev, size=n_rows)
        
        # Clip agar tidak keluar batas dan bulatkan 2 desimal
        return np.clip(data, min_val, max_val).round(2)

    # 3. Tipe CATEGORICAL
    elif col_type == "categorical":
        options = col_def.get("values", ["Yes", "No"])
        # Menggunakan np.random.choice lebih cepat untuk data besar dibanding random.choices
        return np.random.choice(options, size=n_rows)

    # Fallback jika tipe tidak dikenali
    return np.array(["unknown"] * n_rows)


def generate_dataframe(schema):
    """
    Fungsi utama untuk membuat DataFrame dari Schema JSON
    """
    rows = schema.get("rows", 10)
    columns_schema = schema.get("columns", [])
    
    data_dict = {}
    
    for col in columns_schema:
        col_name = col["name"]
        data_dict[col_name] = generate_column_data(col, rows)
        
    return pd.DataFrame(data_dict)