import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle


class XgbtTest:

    def __init__(self):
        self.file1 = "xgb_model.pkl"
        self.df = pd.read_csv('dataset/croppred.csv')
        self.cropsDict = dict()
        self.load_model()

    def get_key(self, val):
        for key, value in self.cropsDict.items():
            if val == value:
                return key

    def load_model(self):
        crops = self.df['Crop'].unique()
        crops = [crop for crop in crops]
        i = 0
        for crop in crops:
            i += 1
            self.cropsDict[crop] = i
        self.df['Crop'] = [self.cropsDict.get(crop) for crop in self.df['Crop']]

    def xgbt_Predict(self, rainfall, temp, ph):
        model = pickle.load(open(self.file1, "rb"))
        print(rainfall, temp, ph)
        Xnew = np.array([[rainfall, temp, ph]]).reshape((1, -1))
        print(Xnew)
        predictions = model.predict(Xnew)
        print(predictions)
        return self.get_key(predictions[0])


if __name__ == "__main__":
    # Values taken from dataset/rainTempPh
    rainfall = 700
    temperature = 35
    ph = 7
    model = XgbtTest()
    crop = model.xgbt_Predict(rainfall, temperature, ph)
    print(f"Best suitable crop is : {crop} ")
