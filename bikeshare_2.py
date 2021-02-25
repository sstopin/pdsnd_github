import time
import pandas as pd
import numpy as np
import itertools

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NAMES = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
                'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10,
                'Nov': 11, 'Dec': 12, 'All': 13}
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month_day, month, day = '', '', ''

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please enter the city of interest. (Chicago, New York City, Washington)').lower()
    while city not in CITY_DATA:
        city = input('Invalid City, Please enter the city of interest. (Chicago, New York City, Washington)').lower()


    month_day = input('Would you like to search by month or day?').lower()
    while month_day != 'month' and month_day != 'day':
        month_day = input('Invalid option, would you like to search by month or day?').lower()
    # get user input for month (all, january, february, ... , june)
    if month_day == 'month':
        month = input('Please enter month or All. (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Nov, Dec, All)').title()
        while month not in MONTH_NAMES:
            month = input('Invalid month, Please enter month or All. (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sept, Oct, Nov, Dec, All)').title()
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif month_day == 'day':
        day = input('Please enter day or All. (Mon, Tue, Wed, Thur, Fri, Sat, Sun, All)').title()
        while day not in DAY_NAMES:
            day = input('Invalid day, Please enter day or All. (Mon, Tue, Wed, Thur, Fri, Sat, Sun, All)').title()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA.get(city))
    df_copy = df

#   Load data for selected month, day or all
    df['month'] = pd.to_datetime(df['Start Time'], dayfirst=True).dt.month
    df['weekday'] = pd.to_datetime(df['Start Time'], dayfirst=True).dt.dayofweek
    df['hour'] = pd.to_datetime(df['Start Time'], dayfirst=True).dt.hour
    if month != 'All' and day != 'All':
        if month:
            month_val = MONTH_NAMES.get(month)
            df.drop(df[df['month'] != month_val].index, inplace=True)
        elif day:
            df.drop(df[df['weekday'] != DAY_NAMES.index(day)].index, inplace=True)

    return df, df_copy




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_df = df.groupby('month').count()
    month_df.columns = [c.replace(' ', '_') for c in month_df.columns]
    max_month = month_df['Start_Time'].idxmax()
    max_month_count = month_df.loc[max_month]['Start_Time']

    month_key_list = list(MONTH_NAMES.keys())
    month_val_list = list(MONTH_NAMES.values())
    max_month_name = month_key_list[month_val_list.index(max_month)]

    print('The most active month was {} with {} riders.'.format(max_month_name, max_month_count))


    # display the most common day of week
    day_df = df.groupby('weekday').count()
    day_df.columns = [c.replace(' ', '_') for c in day_df.columns]
    max_day = day_df['Start_Time'].idxmax()
    max_day_count = day_df.loc[max_day]['Start_Time']

    print('The most active day was {} with {} riders.'.format(DAY_NAMES[max_day], max_day_count))


    # display the most common start hour
    hour_df = df.groupby('hour').count()
    hour_df.columns = [c.replace(' ', '_') for c in hour_df.columns]
    max_hour = hour_df['Start_Time'].idxmax()-1
    max_hour_count = hour_df.iloc[hour_df['Start_Time'].idxmax()-1]['Start_Time']

    print('The most common start hour was {} with {} riders.'.format(max_hour, max_hour_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df.columns = [c.replace(' ', '_') for c in df.columns]
    start_station_df = df.groupby('Start_Station').count()
    max_start_station = start_station_df['Start_Time'].idxmax()
    max_start_station_count = start_station_df.loc[max_start_station]['Start_Time']

    print('The most commonly used start station was {} with {} riders.'.format(max_start_station, max_start_station_count))


    # display most commonly used end station
    end_station_df = df.groupby('End_Station').count()
    max_end_station = end_station_df['Start_Time'].idxmax()
    max_end_station_count = end_station_df.loc[max_end_station]['Start_Time']

    print('The most commonly used end station was {} with {} riders.'.format(max_end_station, max_end_station_count))


    # display most frequent combination of start station and end station trip
    combo_station_df = df.groupby(['Start_Station', 'End_Station']).count()
    max_combo_station = combo_station_df['Start_Time'].idxmax()
    max_combo_station_count = combo_station_df.loc[max_combo_station]['Start_Time']

    print('The most commonly used start and end station was {} with {} riders.'.format(max_combo_station, max_combo_station_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # display total travel time
    total_time = df['Trip_Duration'].sum()
    total_hours = total_time // 3600
    rem_time = total_time % 3600
    total_min = rem_time // 60
    total_sec = rem_time % 60

    print('Total Travel Time {} hours, {} minute, {} seconds'.format(total_hours, total_min, total_sec))


    # display mean travel time
    mean_time = int(df["Trip_Duration"].mean().round())
    mean_hours = mean_time // 3600
    mean_rem_time = mean_time % 3600
    mean_min = mean_rem_time // 60
    mean_sec = mean_rem_time % 60

    print('Mean Travel Time {} hours, {} minute, {} seconds'.format(mean_hours, mean_min, mean_sec))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # Display counts of user types
    types_df = df.groupby('User_Type').count()
    print('User type counts: ')
    for type_idx in types_df.index:
        print('        ', type_idx, ':', types_df['Start_Time'][type_idx])


    # Display counts of gender
    if 'Gender' in df:
        gender_df = df.groupby('Gender').count()
        print('\nGender counts: ')
        for gender_idx in gender_df.index:
            print('        ', gender_idx, ':', gender_df['Start_Time'][gender_idx])

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        print('\Oldest year of birth:', int(df['Birth_Year'].min()))
        print('\nMost recent year of birth:', int(df['Birth_Year'].max()))

        birth_df = df.groupby('Birth_Year').count()

        common_birth_year = int(birth_df['Start_Time'].idxmax())
        print('\nMost common year of birth', common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df_copy):
    """ User is able to view raw data 5 items at a time if requested """
    i = 0
    raw = input("Would you like to see individual trip raw data?\n")
    pd.set_option('display.max_columns',200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            for index in range(i, i+5):
                temp_dict = dict(zip(list(df_copy.iloc[[0]]), df_copy.iloc[[index][0]]))
                print(temp_dict, '\n')
            raw = input("Would you like to continuing seeing individual trip raw data?\n")
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df, df_copy = load_data(city, month, day)
        if df.empty:
            print('NO DATA TO DISPLAY!!\n\n')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df_copy)


        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no' or restart.lower() == 'yes':
                break
            else:
                print('Invalid option.\n')

        if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
