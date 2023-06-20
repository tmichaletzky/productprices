import streamlit as st

st.title("DMLab task: Build a regression model to predict product prices")

label_encoder = { 
    "display_type": ["TN", "LCD", "LED", "OLED", "QLED", "NANOCELL", "QNED"][::-1], # best to worst
    "energyclass": ["A","B","C","D","E","F","G"], # best to worst
    "display_resolution": ["HD", "Full HD", "4K", "8K"][::-1], # best to worst [720,1080,2160,4320]
    "dim_color": ["Fehér","Ezüst","Szürke","Bézs","Korall","Kék","Fekete"], # brightest to darkest
}

item = {}
for prop in label_encoder:
    choice = st.radio(f"Pick {prop}:", label_encoder[prop])
    item[prop] = choice
    
st.write(item)