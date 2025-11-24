import pandas as pd
import joblib
import os
from challenge.model import DelayModel

def train_and_save():
    print("Loading data...")
    data = pd.read_csv("data/data.csv")
    
    print("Initializing model...")
    model = DelayModel()
    
    print("Preprocessing...")
    features, target = model.preprocess(data=data, target_column="delay")
    
    print("Fitting...")
    model.fit(features, target)
    
    print("Saving model...")
    joblib.dump(model._model, "challenge/model.joblib")
    print("Model saved to challenge/model.joblib")

if __name__ == "__main__":
    train_and_save()
