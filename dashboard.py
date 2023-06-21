import streamlit as st
import pandas as pd
from xgboost import XGBRegressor

from utils import *
from prepocess_api import PreProcessor

st.title("DMLab task: Build a regression model to predict product prices")

features = pd.read_csv("data/basetable.csv").columns


item = {}

for prop in features:
    value = None
    if prop in float_cols:
        if prop == "display_size":
            unit = "inch"
        elif prop == "dim_weight":
            unit = "kg"
        else:
            unit = "cm"
        value = st.number_input(f'Add {prop} (in {unit}):')
    elif prop in int_cols:
        value = st.number_input(f'Add {prop} (number of slots):')
    elif prop in binary_cols:
        has = st.checkbox(f'Add {prop} (has it or not):', 1,0)
        if has:
            value = "Igen"
        else:
            value = "Nem"
    elif prop in label_encoder:
        value = st.selectbox(f'Add {prop}: ', label_encoder[prop])
    
    item[prop] = value
    

product = st.text_input("Product name (or just the company):")
item["product"] = product

price = st.number_input("Add price")
item["price"] = price

st.write("Your product:")
st.write(item)


preprocessor = PreProcessor("")
line = preprocessor.product(item)
print(line)

model = XGBRegressor().load_model("models/xgbr_log.json")
