import os
import pickle
import random

import numpy as np
import pandas as pd


class ModelWrapper:
    def __init__(self) -> None:
        # load model
        model_path = "models/best_model.pickle"
        self.model = pickle.load(open(model_path, "rb"))

        # load scaler
        scaler_path = "models/used_scaler.pickle"
        self.scaler = pickle.load(open(scaler_path, "rb"))

    def preprocess_result(self, result: dict):
        """
        result = {
                "age": age,
                "sex": sex,
                "chest pain type": cp,
                "resting bp s": trestbps,
                "cholesterol": chol,
                "fasting blood sugar": fbs,
                "resting ecg": restecg,
                "max heart rate": thalach,
                "exercise angina": exang,
                "oldpeak": oldpeak,
                "ST slope": slope,
            }
        """
        result["age"] = int(result["age"])

        result["sex"] = 1 if result["sex"] == "Male" else 0

        result["chest pain type"] = [
            "Typical Angina",
            "Atypical Angina",
            "Non-Anginal Pain",
            "Asymptomatic",
        ].index(result["chest pain type"]) + 1

        result["resting bp s"] = int(result["resting bp s"])

        result["cholesterol"] = int(result["cholesterol"])

        result["fasting blood sugar"] = (
            1 if result["fasting blood sugar"] == "True" else 0
        )

        result["resting ecg"] = [
            "normal",
            "having ST-T wave abnormality",
            "showing probable or definite left ventricular hypertrophy by Estes' criteria",
        ].index(result["resting ecg"])

        result["max heart rate"] = int(result["max heart rate"])

        result["exercise angina"] = 1 if result["exercise angina"] == "Yes" else 0

        result["oldpeak"] = float(result["oldpeak"])

        result["ST slope"] = ["upsloping", "flat", "downsloping"].index(
            result["ST slope"]
        ) + 1

        # convert to dataframe
        X = pd.DataFrame(result, index=[0])

        os.write(1, f"Preprocessed data:\n".encode())
        for col in X.columns:
            # write values
            os.write(1, f"{col}: {X[col].values[0]}\n".encode())
        os.write(1, f"\n".encode())
        return X

    def scale_data(self, X: pd.DataFrame) -> np.array:
        X_scaled = self.scaler.transform(X)
        # show scaled data
        os.write(1, f"Scaled data:\n".encode())
        for col in X.columns:
            # write values
            os.write(1, f"{col}: {X_scaled[0][X.columns.get_loc(col)]}\n".encode())
        os.write(1, f"\n".encode())
        return X_scaled

    def run_model(self, X: np.array) -> float:
        prediction = self.model.predict_proba(X)
        max_index = np.argmax(prediction)
        confidence = prediction[0][max_index]
        return confidence, max_index

    def predict(self, result: dict):
        # preprocess the result
        X = self.preprocess_result(result)

        # scale data
        X_scaled = self.scale_data(X)

        # get prediction from model
        confidence, max_index = self.run_model(X_scaled)

        # return result
        return confidence, max_index
