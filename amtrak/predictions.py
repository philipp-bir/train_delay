import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import xgboost as xgb
import math
import pickle

class ColumnTransform:
    
    def __init__(self,train_data=None,ignore=[],label=None,na_cutoff=1,is_category=[],
                 fill_zero_na_pre=[],fill_zero_na_post=[],to_predict_data=None):
        self.cat_columns=[]
        self.num_columns=[]
        self.categories={}
        self.ignore=ignore
        self.label=label
        self.is_category=is_category
        self.na_cutoff=na_cutoff #ratio of how many rows at most can be NA for the column to be considered
        
        self.to_predict_data=to_predict_data
        self.fill_zero_na_pre=fill_zero_na_pre
        self.fill_zero_na_post=fill_zero_na_post
        
        self.normalize_data={}
        if train_data is not None:
            self.decide_cols_(train_data)
        
    def to_dict(self):
        return {
            "cat_columns":self.cat_columns,
            "num_columns": self.num_columns,
            "categories": self.categories,
            "label": self.label,
            "normalize_data": self.normalize_data,
            "fill_zero_na_pre": self.fill_zero_na_pre,
            }
            
    def from_dict(self,d):
        self.cat_columns = d["cat_columns"]
        self.num_columns = d["num_columns"]
        self.categories = d["categories"]
        self.label = d["label"]
        self.normalize_data = d["normalize_data"]
        self.fill_zero_na_pre = d["fill_zero_na_pre"]
            
            

    def is_good_category_(self,train_data,col):
        if self.to_predict_data is None:
            return True
        to_predict_cats=set(self.to_predict_data[col].unique())
        untrainable=to_predict_cats-set(train_data[col].unique())
        if len(untrainable)>0:
            print(f"{col} - {untrainable}")
            return False

        val_counts=data[col].value_counts(dropna=False).to_dict()
        print(val_counts)
        for c in val_counts.keys():
            if val_counts[c]<10:
                if c in to_predict_cats:
                    return False
                else:
                    print(f"Don't need to drop {d}")
        return True
        
    def decide_cols_(self,train_data):
        for c in train_data.columns:
            if c in self.ignore or c==self.label:
                continue
            na_count=sum(train_data[c].isna())
            if na_count/len(train_data)<self.na_cutoff:
                dtype=str(train_data[c].dtype)
                if "object" in dtype or "category" in dtype or c in self.is_category:
                    if self.is_good_category_(train_data,c):
                        self.cat_columns+=[c]
                        #self.train_data[c]=self.train_data[c].fillna(self.na_category)
                    else:
                        print(f"Dropping {c}")
                elif "float" in dtype:
                    self.num_columns+=[c]
                elif "int" in dtype:
                    if len(set(train_data[c]))<10 and self.is_good_category_(train_data,c):
                        self.cat_columns+=[c]
                        #self.train_data[c]=self.train_data[c].fillna(-999912312)
                    else:
                        self.num_columns+=[c]
                else:
                    #unknown dtype
                    self.cat_columns+=[c]
        
        for c in self.num_columns:
            self.normalize_data[c]=(train_data[c].mean(),train_data[c].std())
        
        for c in self.cat_columns:
            self.categories[c]=sorted(train_data.loc[:, c].value_counts(dropna=True).index)
            
                        
    def transform(self,data):
        categorical_data=pd.DataFrame(index=data.index)
        for c in self.cat_columns:
            categorical_data[c] = pd.Categorical(data.loc[:,c],categories = self.categories[c])
        
        one_hot_encoded = pd.get_dummies(categorical_data)
        
        df=data[self.num_columns].join(one_hot_encoded)

        if self.label in data.columns:
            df=df.join(data[self.label])
        df[self.fill_zero_na_pre]=df[self.fill_zero_na_pre].fillna(0)
        for c in self.num_columns:
            mean,std=self.normalize_data[c]
            df[c]=(df[c]-mean)/std

        df=df.fillna(0)
        return df
        
        
class Predictor:
    
    def __init__(self,ct_file_name,bst_file_name):
        with open(bst_file_name,"rb") as bst_file:
            self.bst=pickle.load(bst_file)
        with open(ct_file_name,"rb") as ct_file:
            ct_dict=pickle.load(ct_file)
            self.ct=ColumnTransform()
            self.ct.from_dict(ct_dict)
        
    
    def predict(self,entry):
        val=pd.DataFrame.from_dict(entry)
        val_tf=self.ct.transform(val)
        #_=val_tf.pop("delay")
        xgb_val=xgb.DMatrix(val_tf)

        return self.bst.predict(xgb_val)
    
    
