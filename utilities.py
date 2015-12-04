__author__ = 'andrew'

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
from collections import namedtuple
import math

def create_training_csv():
    trainDf = pd.read_csv('csv/train.csv')
    trainDf = merge_store_data(trainDf, 'csv/store.csv')
    trainDf = trainDf.fillna(0)
    create_training_features(trainDf)
    # trainDf.to_csv('csv/combined.csv', sheet_name='train.csv X store.csv')
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
    add_current_week(df)
    # generate_competition_metrics(df)
    # generate_promo2_metrics(df)
    # generate_customer_metrics(df)
    # generate_sales_metrics(df)

def add_current_week(df):

    def parse_week(date_string):
        return datetime.strptime(date_string, "%Y-%m-%d").isocalendar()[1]

    df['current_week'] = [parse_week(val) for val in df['Date']]

def expand_holiday_features(df):
    df['public_holiday'] = [1 if val == 'a' else 0 for val in df['StateHoliday']]
    df['easter_holiday'] = [1 if val == 'b' else 0 for val in df['StateHoliday']]
    df['christmas_holiday'] = [1 if val == 'c' else 0 for val in df['StateHoliday']]

def drop_closed_stores(df):
    df = df[df.Open != 0]

def generate_competition_metrics(df):

    def get_months(row):

       if row['CompetitionOpenSinceYear'] != 0:
            cur_date = datetime.strptime(row['Date'], "%Y-%m-%d")
            comp_year = int(row['CompetitionOpenSinceYear'])
            comp_month = int(row['CompetitionOpenSinceMonth'])
            comp_date = datetime.strptime(str(comp_year) + "-" + str(comp_month) + "-" + str(1), "%Y-%m-%d")
            val = round(abs((cur_date - comp_date).days) / 30)
            return val
       else:
           return 0

    df['Competition_since_months'] = df.apply(get_months, axis=1)


def generate_promo2_metrics(df):
    return None


def generate_customer_metrics(df):
    generate_avg_customers_by_week_by_store(df)
    generate_avg_customers_by_store_school_holiday(df)


def generate_avg_customers_by_store_school_holiday(df):
    mean_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['avg_customers_by_store_school_holiday'] = 0

    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        store = store[(store['SchoolHoliday'] == 1)]
        mean_dictionary[store_number] = store['Customers'].mean()

    def apply_avg_school_holiday(row):
        store_id = row['Store']
        return mean_dictionary[store_id]

    df['avg_customers_by_store_school_holiday'] = df.apply(apply_avg_school_holiday, axis=1)



def generate_sales_metrics(df):
    pass

def generate_avg_customers_by_week_by_store(df):

    mean_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['avg_customers_by_week'] = 0

    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        for week_number in range(1, 53):
            weeks = store[(store['current_week'] == week_number)]
            mean = weeks['Customers'].mean()
            key = str(store_number) + str(week_number)
            mean_dictionary[key] = mean

    def apply_cust_avg(row):
        store_id = row['Store']
        week = row['current_week']
        keyy = str(store_id) + str(week)
        return mean_dictionary[keyy]

    df['avg_customers_by_week'] = df.apply(apply_cust_avg, axis=1)


df = create_training_csv()
generate_customer_metrics(df)
print(df.describe())