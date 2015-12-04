__author__ = 'andrew'

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def create_training_csv():
    trainDf = pd.read_csv('csv/train.csv')
    trainDf = merge_store_data(trainDf, 'csv/store.csv')
    create_training_features(trainDf)
    trainDf.to_csv('csv/combined.csv', sheet_name='train.csv X store.csv')
    return trainDf

def merge_store_data(df, store_csv_filename):
    storeDf = pd.read_csv(store_csv_filename)
    df = pd.merge(df, storeDf, on='Store')
    return df

def create_training_features(df):
    expand_holiday_features(df)
    drop_closed_stores(df)
    df['StoreType_a'] = [1 if val == 'a' else 0 for val in df['StoreType']]
    df['StoreType_b'] = [1 if val == 'b' else 0 for val in df['StoreType']]
    df['StoreType_c'] = [1 if val == 'c' else 0 for val in df['StoreType']]
    df['StoreType_d'] = [1 if val == 'd' else 0 for val in df['StoreType']]
    df['Assortment'] = [1 if val == 'a' else 0 for val in df['Assortment']]
    generate_competition_metrics(df)
    generate_promo2_metrics(df)
    generate_customer_metrics(df)
    generate_sales_metrics(df)

def expand_holiday_features(df):
    df['public_holiday'] = [1 if val == 'a' else 0 for val in df['StateHoliday']]
    df['easter_holiday'] = [1 if val == 'b' else 0 for val in df['StateHoliday']]
    df['christmas_holiday'] = [1 if val == 'c' else 0 for val in df['StateHoliday']]

def drop_closed_stores(df):
    df = df[df.Open != 0]

def generate_competition_metrics(training_df):
    return None

def generate_promo2_metrics(df):
    return None

def generate_customer_metrics(df):
    return None

def generate_sales_metrics(df):
    pass

create_training_csv()