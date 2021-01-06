import os
import sys

sys.path.append("../..")

import numpy as np
import pandas as pd

from mikasa.common import timer
from mikasa.io import load_pickle


def submission(models, data):
    def lgbm_predict(models, data):
        preds = [m.predict(data) for m in models]
        return np.mean(preds, axis=0)

    pred = lgbm_predict(models, data)
    pred = (pred > 0.5).astype(np.int8)
    return pred


def create_features(data):
    # === extract_raw_feature ===
    # Fill null values.
    data["Embarked"].fillna("missing", inplace=True)

    # Label encoding.
    data["Sex"] = data["Sex"].map({"female": 0, "male": 1})
    data["Embarked"] = data["Embarked"].map({"C": 0, "Q": 1, "S": 2, "missing": 3})
    ticket_uniques = load_pickle("../data/preprocess/ticket_uniques.pkl", verbose=False)
    data["Ticket"] = data["Ticket"].map({u: i for i, u in enumerate(ticket_uniques)})
    cabin_uniques = load_pickle("../data/preprocess/cabin_uniques.pkl", verbose=False)
    data["Cabin"] = data["Cabin"].map({u: i for i, u in enumerate(cabin_uniques)})

    # Drop columns
    data.drop(["Survived", "PassengerId", "Name"], axis=1, inplace=True)
    return data


def main():
    test = pd.read_csv("../data/raw/test.csv")
    test["Survived"] = 0
    X_test = create_features(test)

    lgbm_models = load_pickle("../data/working/lgbm_models.pkl")

    print(test.head())

    with timer("Submission"):
        pred = submission(lgbm_models, X_test)

        submit = pd.read_csv("../data/raw/gender_submission.csv")
        submit["Survived"] = pred
        submit.to_csv("../data/submit/submission.csv", index=False)

        print(submit.head())
        print(submit["Survived"].value_counts().sort_index())


if __name__ == "__main__":
    main()