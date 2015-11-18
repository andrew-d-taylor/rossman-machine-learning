__author__ = 'andrew'

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def createFlatCsv():
    trainDf = pd.read_csv('train.csv')
    storeDf = pd.read_csv('store.csv')
    combined = pd.merge(trainDf, storeDf, on='Store')
    combined.to_csv('combined.csv', sheet_name='train.csv X store.csv')


def plot(estimate, response, responseLabel, predictor, predictorLabel):
    X_prime = np.linspace(predictor.min(), predictor.max(), 100)[:, np.newaxis]
    X_prime = sm.add_constant(X_prime)
    predictions = estimate.predict(X_prime)
    plt.scatter(predictor, response, alpha=0.3)
    plt.xlabel(predictorLabel)
    plt.ylabel(responseLabel)
    plt.plot(X_prime[:, 1], predictions, 'r', alpha=0.9)

