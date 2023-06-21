import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

from utils import *
from preprocess import PreProcessor

st.title("DMLab task: Build a regression model to predict product prices")

features = pd.read_csv("data/basetable.csv").columns

st.header("Specify product")


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
        value = st.number_input(f'Add {prop} (in {unit}):', value=0.0)
        if value == 0.0:
            value = None
    elif prop in int_cols:
        value = st.number_input(f'Add {prop} (number of slots):', value=-1)
        if value < 0:
            value = None
    elif prop in binary_cols:
        has = st.checkbox(f'Has {prop} or not (check box if yes):', value=0)
        if has:
            value = "Igen"
        else:
            value = "Nem"
    elif prop in label_encoder:
        value = st.selectbox(f'Add {prop}: ', ["Don't know"] + label_encoder[prop], index=0)
        if value == "Don't know":
            value = None
    
    if value: # not None
        item[prop] = value
            
    

product = st.text_input("Product name (or just the company):")
item["product"] = product

price = st.number_input("Add price")
item["price"] = price


####################
st.subheader("Your product:")
st.write(item)

        
def product(item):
    global COLUMNS
    preprocessor = PreProcessor()
    # get columns
    # get my features
    feature = item.copy()
    preprocessor.label_encode(item,feature)
    preprocessor.binary_encode(item,feature)
    preprocessor.onehot_encode(item,feature)
    preprocessor.derive(feature)
    feature["price"] = float(item["price"])
    for key in COLUMNS:
        if key not in feature:
            feature[key] = np.nan    
    drop = []
    for key in feature:
        if key not in COLUMNS:
            drop.append(key)
    for key in drop:
        feature.pop(key)
    return feature

COLUMNS = pd.read_csv("data/basetable.csv").columns

values = product(item)

######################
st.subheader("Features:")

values.pop("serial_id")
values.pop("price")
line = pd.DataFrame(values, index=[0], columns=COLUMNS, dtype=float)
st.write(line)


###################
st.header("Prediction")

model = XGBRegressor()
model.load_model("models/xgbr_log_cutoff.json")

pred = model.predict(line.drop(columns=["price","serial_id"]))
pred_price = np.exp(pred[0])

st.write(f"Predicted price: {pred_price} Ft")
if price > 0.0:
    st.write(f"Actual price is {price} Ft, difference is ~{abs(pred_price - price):.0f} Ft.")
else: 
    st.write(f"Actual price is not set")