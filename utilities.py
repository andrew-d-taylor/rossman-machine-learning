__author__ = 'andrew'

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def createFlatCsv():
    trainDf = pd.read_csv('csv/train.csv')
    storeDf = pd.read_csv('csv/store.csv')
    combined = pd.merge(trainDf, storeDf, on='Store')
    combined['StoreType_a'] = [1 if val == 'a' else 0 for val in combined['StoreType']]
    combined['StoreType_b'] = [1 if val == 'b' else 0 for val in combined['StoreType']]
    combined['StoreType_c'] = [1 if val == 'c' else 0 for val in combined['StoreType']]
    combined['StoreType_d'] = [1 if val == 'd' else 0 for val in combined['StoreType']]
    combined['Assortment'] = [1 if val == 'a' else 0 for val in combined['Assortment']]
    combined.to_csv('csv/combined.csv', sheet_name='train.csv X store.csv')

def plot(estimate, response, responseLabel, predictor, predictorLabel):
    X_prime = np.linspace(predictor.min(), predictor.max(), 100)[:, np.newaxis]
    X_prime = sm.add_constant(X_prime)
    predictions = estimate.predict(X_prime)
    plt.scatter(predictor, response, alpha=0.3)
    plt.xlabel(predictorLabel)
    plt.ylabel(responseLabel)
    plt.plot(X_prime[:, 1], predictions, 'r', alpha=0.9)


createFlatCsv()