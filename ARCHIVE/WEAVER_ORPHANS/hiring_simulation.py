#!/usr/bin/env python3
# hiring_simulation.py
# Simulates a hiring decision pipeline with and without Kalaxi governance
# Uses UCI Adult dataset as proxy for hiring data

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import sys
sys.path.append('.')
from WEAVER.dignity_check import dignity_gate  # we'll create a simple stub if not present

# Simple dignity stub for simulation
def simple_dignity(individual, prediction):
    """Check for proxy discrimination (race, sex)"""
    # In real system, would call full dignity_gate
    race_cols = [c for c in individual.index if 'race' in c]
    sex_cols = [c for c in individual.index if 'sex' in c]
    # If prediction is 0 (reject) and individual belongs to protected group, flag
    if prediction == 0 and any(individual[race_cols] > 0 if race_cols else False):
        return False
    if prediction == 0 and any(individual[sex_cols] > 0 if sex_cols else False):
        return False
    return True

def main():
    # Load dataset
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    columns = ['age','workclass','fnlwgt','education','education-num','marital-status',
               'occupation','relationship','race','sex','capital-gain','capital-loss',
               'hours-per-week','native-country','income']
    data = pd.read_csv(url, header=None, names=columns, na_values=' ?')
    data = data.dropna()

    # Prepare features and labels
    X = pd.get_dummies(data.drop('income', axis=1))
    y = (data['income'] == '>50K').astype(int)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train baseline model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict probabilities
    y_pred_prob = model.predict_proba(X_test)[:,1]
    threshold = 0.5
    y_pred = (y_pred_prob >= threshold).astype(int)

    # Apply dignity audit
    dignity_results = []
    for i in range(len(X_test)):
        ind = X_test.iloc[i]
        pred = y_pred[i]
        ok = simple_dignity(ind, pred)
        dignity_results.append(ok)

    # Cohort analysis by race (simplified)
    race_cols = [c for c in X_test.columns if 'race' in c]
    if race_cols:
        groups = X_test[race_cols].idxmax(axis=1)  # get race group
        cohort_means = groups.groupby(groups).apply(lambda g: np.mean([dignity_results[j] for j in g.index]))
        print("Cohort dignity means by race:")
        print(cohort_means)
        print("Variance:", np.var(cohort_means))
    else:
        print("No race columns found – dataset may be anonymized.")

    # Governance simulation: reject predictions that fail dignity
    y_pred_governed = []
    for i in range(len(X_test)):
        if not dignity_results[i]:
            y_pred_governed.append(0)  # reject (could also defer)
        else:
            y_pred_governed.append(y_pred[i])

    acc_baseline = accuracy_score(y_test, y_pred)
    acc_governed = accuracy_score(y_test, y_pred_governed)
    print(f"Baseline accuracy: {acc_baseline:.3f}")
    print(f"Governed accuracy: {acc_governed:.3f}")
    print(f"Accuracy loss: {acc_baseline - acc_governed:.3f}")

if __name__ == "__main__":
    main()
