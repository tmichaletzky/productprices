import streamlit as st
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

st.title("Task: Build a regression model to predict product prices")


###############
st.header("Specify product")

features = pd.read_csv("data/basetable.csv").columns

# from Preprocessing.ipynb
float_cols = ["display_size",  "dim_height","dim_width","dim_depth","dim_weight"]
int_cols = ["num_usb","num_hdmi"]
binary_cols = ["smart","usb","wifi"]
label_encoder = { 
    "display_type": ["TN", "LCD", "LED", "OLED", "QLED", "NANOCELL", "QNED"][::-1], # best to worst
    "energyclass": ["A","B","C","D","E","F","G"], # best to worst
    "display_resolution": ["HD", "Full HD", "4K", "8K"][::-1], # best to worst [720,1080,2160,4320]
    "dim_color": ["Fehér","Ezüst","Szürke","Bézs","Korall","Kék","Fekete"], # brightest to darkest
}


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
            value = 1
        else:
            value = 0
    elif prop in label_encoder:
        value = st.selectbox(f'Add {prop}: ', ["Don't know"] + label_encoder[prop], index=0)
        if value == "Don't know":
            value = None
        else:
            value = label_encoder[prop].index(value)
    
    if value: # not None
        item[prop] = value
            
    
product = st.text_input("Product name (or just the company):")
item["product"] = product

price = st.number_input("Add price")
item["price"] = price


####################
st.subheader("Your product:")
st.write(item)

######################
st.subheader("Features:")

for feat in features:
    if feat not in item:
        item[feat] = np.nan

item.pop("serial_id")
item.pop("price")

line = pd.DataFrame(item, index=[0], columns=features, dtype=float)
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