import pandas as pd
from datetime import datetime


def create_training_csv():
    df = pd.read_csv('csv/train.csv')
    df = merge_store_data(df, 'csv/store.csv')
    df = df.fillna(0)
    df = df[(df['Store'] < 50)]
    create_training_features(df)
    # trainDf.to_csv('csv/combined.csv', sheet_name='train.csv X store.csv')
    return df

def merge_store_data(df, store_csv_filename):
    storeDf = pd.read_csv(store_csv_filename)
    df = pd.merge(df, storeDf, on='Store')
    return df

def create_training_features(df):
    expand_holiday_features(df)
    drop_closed_stores(df)
    generate_store_types(df)
    add_current_week(df)
    generate_customer_metrics(df)
    generate_competition_metrics(df)
    generate_sales_metrics(df)
    # generate_promo2_metrics(df)


def generate_store_types(df) :
    df['StoreType_a'] = [1 if val == 'a' else 0 for val in df['StoreType']]
    df['StoreType_b'] = [1 if val == 'b' else 0 for val in df['StoreType']]
    df['StoreType_c'] = [1 if val == 'c' else 0 for val in df['StoreType']]
    df['StoreType_d'] = [1 if val == 'd' else 0 for val in df['StoreType']]
    df['Assortment'] = [1 if val == 'a' else 0 for val in df['Assortment']]


def add_current_week(df):
    def parse_week(date_string):
        return datetime.strptime(date_string, "%Y-%m-%d").isocalendar()[1]

    df['current_week'] = [parse_week(val) for val in df['Date']]

def expand_holiday_features(df):
    df['public_holiday'] = [1 if val == 'a' else 0 for val in df['StateHoliday']]
    df['easter_holiday'] = [1 if val == 'b' else 0 for val in df['StateHoliday']]
    df['christmas_holiday'] = [1 if val == 'c' else 0 for val in df['StateHoliday']]


def drop_closed_stores(df):
    df = df[(df['Open'] != 0)]
    df = df.reset_index(drop=True)
    def print_closed(x):
        if x == 0:
            print('CLOSED')
    df['Open'].apply(print_closed)

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
    generate_avg_customers_by_week_and_day_by_store(df)
    generate_avg_customers_by_store_school_holiday(df)
    generate_avg_customers_by_store_state_holiday(df)
    generate_customer_statistics_by_store(df)


def generate_customer_statistics_by_store(df):
    max_dictionary = {}
    mean_dictionary = {}
    std_dev_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['max_customers_by_store'] = 0
    df['mean_customers_by_store'] = 0
    df['std_dev_customers_by_store'] = 0


    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        customers = store['Customers']
        max_dictionary[store_number] = customers.max()
        mean_dictionary[store_number] = customers.mean()
        std_dev_dictionary[store_number] = customers.std()

    def apply_max(row):
        store_id = row['Store']
        return max_dictionary[store_id]

    def apply_mean(row):
        store_id = row['Store']
        return mean_dictionary[store_id]

    def apply_std_dev(row):
        store_id = row['Store']
        return std_dev_dictionary[store_id]


    df['mean_customers_by_store'] = df.apply(apply_mean, axis=1)
    df['std_dev_customers_by_store'] = df.apply(apply_std_dev, axis=1)
    df['max_customers_by_store'] = df.apply(apply_max, axis=1)


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


def generate_avg_customers_by_store_state_holiday(df):
    mean_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['avg_customers_by_store_state_holiday'] = 0

    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        store = store[(store['StateHoliday'] != 0)]
        mean_dictionary[store_number] = store['Customers'].mean()

    def apply_avg_state_holiday(row):
        store_id = row['Store']
        return mean_dictionary[store_id]

    df['avg_customers_by_store_state_holiday'] = df.apply(apply_avg_state_holiday, axis=1)



def generate_sales_metrics(df):
    generate_sales_statistics(df)
    generate_sales_school_state_holiday(df)


def generate_sales_school_state_holiday(df):
    school_mean_dictionary = {}
    state_mean_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['avg_sales_by_store_school_holiday'] = 0
    df['avg_sales_by_store_state_holiday'] = 0

    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        school = store[(store['SchoolHoliday'] == 1)]
        state = store[(store['StateHoliday'] != 0)]
        school_mean_dictionary[store_number] = school['Sales'].mean()
        state_mean_dictionary[store_number] = state['Sales'].mean()


    def apply_avg_school_holiday(row):
        store_id = row['Store']
        return school_mean_dictionary[store_id]

    def apply_avg_state_holiday(row):
        store_id = row['Store']
        return state_mean_dictionary[store_id]

    df['avg_sales_by_store_school_holiday'] = df.apply(apply_avg_school_holiday, axis=1)
    df['avg_sales_by_store_state_holiday'] = df.apply(apply_avg_state_holiday, axis=1)



def generate_sales_statistics(df):
    max_dictionary = {}
    mean_dictionary = {}
    std_dev_dictionary = {}
    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['max_sales_by_store'] = 0
    df['mean_sales_by_store'] = 0
    df['std_dev_sales_by_store'] = 0


    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        sales = store['Sales']
        max_dictionary[store_number] = sales.max()
        mean_dictionary[store_number] = sales.mean()
        std_dev_dictionary[store_number] = sales.std()

    def apply_max(row):
        store_id = row['Store']
        return max_dictionary[store_id]

    def apply_mean(row):
        store_id = row['Store']
        return mean_dictionary[store_id]

    def apply_std_dev(row):
        store_id = row['Store']
        return std_dev_dictionary[store_id]


    df['mean_sales_by_store'] = df.apply(apply_mean, axis=1)
    df['std_dev_sales_by_store'] = df.apply(apply_std_dev, axis=1)
    df['max_sales_by_store'] = df.apply(apply_max, axis=1)



def generate_avg_customers_by_week_and_day_by_store(df):

    week_dictionary = {}
    day_dictionary = {}

    min_id = df['Store'].min()
    max_id = df['Store'].max() + 1
    df['avg_customers_by_week'] = 0
    df['avg_customers_by_day'] = 0

    for store_number in range(min_id, max_id):
        store = df[(df['Store'] == store_number)]
        for week_number in range(1, 53):
            weeks = store[(store['current_week'] == week_number)]
            mean = weeks['Customers'].mean()
            key = str(store_number) + str(week_number)
            week_dictionary[key] = mean

        for i in range(1,8):
           days = store[(store['DayOfWeek'] == i)]
           mean = days['Customers'].mean()
           key = str(store_number) + str(i)
           day_dictionary[key] = mean


    def apply_week_avg(row):
        store_id = row['Store']
        week = row['current_week']
        key = str(store_id) + str(week)
        return week_dictionary[key]

    def apply_day_avg(row):
        store_id = row['Store']
        day = row['DayOfWeek']
        key = str(store_id) + str(day)
        return day_dictionary[key]

    df['avg_customers_by_week'] = df.apply(apply_week_avg, axis=1)
    df['avg_customers_by_day'] = df.apply(apply_day_avg, axis=1)



blah = create_training_csv()
print(blah.describe())