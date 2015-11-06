__author__ = 'andrew'

import numpy as np
import pandas as pd

def createFlatCsv():
    trainDf = pd.read_csv('train.csv')
    storeDf = pd.read_csv('store.csv')
    combined = pd.merge(trainDf, storeDf, on='Store')
    combined.to_csv('combined.csv', sheet_name='train.csv X store.csv')