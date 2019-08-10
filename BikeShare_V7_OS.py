#!/usr/bin/env python
# coding: utf-8

# In[11]:


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hey there! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city =input('Would you like to see data for Chicago, Washington or New York City? ').lower()
        if city not in cities:
            print('It seems you typed a wrong city name, please try again!')
        else:
            break






    # get user input for month (all, january, february, ... , june)
    while True:

        input_time = input('Would you like to filter the data by month, day or not at all? Type "none" for no time filter.\n ')
        if input_time == 'month':
            while True:
                month = input('Which month? January, February, March, May or June? Please Type out the full month name.\n ').lower()
                if month in months:
                    month = month.lower()
                    day = 'all'
                    break
                else:
                    print('Please write the full month name, try again!')
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
        if input_time == 'day':
            while True:
                try:
                    day = int(input('Which day? Please type your respond as an integer (e.g., 1=Sunday) \n')) - 1
                    day = days[day]
                    month = 'all'
                    break

                except:
                    print('Wrong input, it should be an integer between 1 and 7, please try again!')
            break

        if input_time == 'none':
            day = 'all'
            month = 'all'
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['end hour'] = df['End Time'].dt.hour
    df['total time'] = df['End Time'].dt.minute - df['Start Time'].dt.minute
    df['route'] = df['Start Station']+" - " + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = (months.index(month))+1

        # filter by month to create the new dataframe
        df = df[df['month']==month]
        print('Getting data for the month:', months[month-1].title())

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
        print('Getting data for the day: ',day)
    #print(city, month, day)
    #print(df.head())

    if day == 'all' and month == 'all':
        print('Getting data for all months and days!')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].mode()[0]
    print('Most popular month: {}'.format(months[common_month-1]).title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most popular day: {}'.format(common_day))

    # display the most common start hour

    common_hour = df['hour'].mode()[0]
    print('Most popular hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().rename_axis('unique_station').reset_index(name='counts')['unique_station'][0]
    count_common_start_station = df['Start Station'].value_counts()[0]
    print('Most popular start station: {} Count: {}'.format(common_start_station, count_common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().rename_axis('unique_station').reset_index(name='counts')['unique_station'][0]
    count_common_end_station = df['End Station'].value_counts()[0]
    print('Most popular end station: {} Count: {}'.format(common_end_station, count_common_end_station))

    # display most frequent combination of start station and end station trip
    popular_route = df['route'].value_counts().rename_axis('unique_station').reset_index(name='counts')['unique_station'][0]
    count_route = df['route'].value_counts()[0]
    print('Most popular route:{} count: {}'.format(popular_route, count_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['total time'].sum()
    count_travel_time = df['total time'].count()
    print('Total travel time in hours: {} Count: {}'.format(total_travel_time / 60, count_travel_time))


    # display mean travel time
    mean_travel_time = total_travel_time / count_travel_time
    print('Mean travel time in minutes : ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()
    print('User types: \n', users)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('Genders: \n', genders)

    # Display earliest, most recent, and most common year of birth
    if 'BIrth Year' in df:

        earliest_year_of_birth = df['Birth Year'].min()
        print('Earliest year of birth: ', earliest_year_of_birth)

        most_recent_year_of_birth = df['Birth Year'].max()
        print('Most recent year of birth: ', most_recent_year_of_birth)

        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth: ', most_common_year_of_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    while True:

        display_data_input = input('Would you like to see some raw data? Enter yes or no.\n').lower()
        if display_data_input == 'yes':
            start_row = 0
            end_row= 5
            print('Displaying raw data..', df.iloc[start_row:end_row, 1:9])

            while True:
                next_5_raws = input('Would you like to see the next 5 rows of the raw data? Enter yes or no.\n').lower()
                if next_5_raws == 'yes':
                    start_row += 5
                    end_row += 5
                    print('Displaying raw data..', df.iloc[start_row :end_row, 1:9])

                else:
                    break
            break
        else:
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
