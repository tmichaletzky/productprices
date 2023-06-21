import json
import warnings
import pandas as pd

from collections import Counter
from utils import *

class PreProcessor():
    def __init__(self):
        pass
        
    def read(self):
        parsed_keys = Counter()
        for item in self.stream:
            parsed_keys.update(item.keys())
        return parsed_keys
    
    def parse(self,fdata):
        global translate_dict
        stream = json.load(open(fdata))
        records = []
        for item in stream:
            record = {}
            for key in item:
                if key.strip() in translate_dict:
                    new_key = translate_dict[key.strip()]
                    record[new_key] = item[key]
                else: # self-defined variables: product,serialnumber,price
                    record[key] = item[key]
            records.append(record)
        return records
    
    def float_encode(self,record,values):
        global float_cols
        for prop in float_cols:
            if prop not in record:
                continue
            value, unit = record[prop].split(" ") # 3,14 format float
            value = float( ".".join(value.split(",")) ) # right float format
            if unit == "cm":
                value *=  0.3937008
            values[prop] = value
    
    def int_encode(self,record,values):
        global int_cols
        for prop in int_cols:
            if prop not in record:
                continue
            value, unit = record[prop].split(" ") # 3,14 format float
            value = int( value )
            if unit != "db":
                warnings.warn(f"Unit does not equal to 'db' in {prop} feature in record {record}, do not propagate to features.")
            else:
                values[prop] = value
                
    def label_encode(self,record,values):
        global label_encoder
        for prop in label_encoder:
            if prop not in record:
                continue
            raw = record[prop]
            if "Ultra HD" in raw:
                raw += " 4K"
            for idx,spec in enumerate(label_encoder[prop]):
                if spec in raw:
                    values[prop] = idx # the smaller the better
                    break
    
    def binary_encode(self,record,values):
        global binary_cols
        for prop in binary_cols:
            if prop not in record:
                continue
            if "Igen" in record[prop]:
                values[prop] = 1
            else: 
                values[prop] = 0
    
    def onehot_encode(self,record,values):
        global companies
        onehot_dict = {
            f"is_company_{company}": 0 for company in companies
        }
        if "product" in record:
            company = record["product"].split(" ")[0].lower()
            if company in companies:
                onehot_dict[f"is_company_{company}"] = 1
        values.update(onehot_dict)
    
    def encode(self,record):
        feature = {}
        self.float_encode(record,feature)
        self.int_encode(record,feature)
        self.label_encode(record,feature)
        self.binary_encode(record,feature)
        self.onehot_encode(record,feature)
        return feature
    
    def derive(self,feature):
        if density_ready(feature):
            feature["dim_density"] = feature["dim_weight"]
            feature["dim_density"] /= ( feature["dim_height"] * feature["dim_width"] * feature["dim_depth"] )
        if pixel_ready(feature):
            feature["display_pixeldensity"] = resolution2pixel(feature["display_resolution"]) / 1000
            feature["display_pixeldensity"] /= ( feature["dim_height"] * feature["dim_width"] ) # the smaller the denser
        if energy_ready(feature):
            feature["display_relativeenergy"] = resolution2pixel(feature["display_resolution"]) / 1000
            feature["display_relativeenergy"] /= feature["energyclass"] + 1 # the bigger the less power consumption
            
    def preprocess(self,fdata):
        records = self.parse(fdata)
        features = []
        for record in records:
            feature = self.encode(record)
            self.derive(feature)
            feature["price"] = float(record["price"])
            feature["serial_id"] = int(record["serialnumber"])
            features.append(feature)
        return features
    
if __name__ == "__main__":
    preprocessor = PreProcessor()
    records = preprocessor.preprocess("crawler/products.json")
    table = pd.DataFrame.from_records(records)
    print(table.columns)
    print(table.head())
    table.to_csv("data/basetable.csv", index=False)