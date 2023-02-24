import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Hi! Please choose one of the following cities: chicago, washington, new york city\n").lower()
    # In case the user entry isn't a part of the CITY_DATA dict keys, print the line below and ask for another entry
    while city not in CITY_DATA.keys(): 
        city = input("{} is not a valid choice, please choose one of the following 3 cities only: chicago, washington, new york city\n".format(city)).lower()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Please enter any month from january to june, or enter 'all' if you wish to select them all:").lower()
    # check whether the user entry is valid or not
    while True: 
        if month in months:
            break
        else:
            month = input("Invalid input, please enter one of the following options\n[all, january, february, march, april, may, june]\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input("Please enter one of the days of the month, or enter 'all' if you wish to select them all\nOptions: [all, monday, tuesday, wednesday, thursday, friday, saturday, sunday]\n").lower()
    # check whether user entry is valid or not
    while True:
        if day in days:
            break
        else:
            # let the user know their entry is invalid and prompt them to try again
            day = input("Invalid input, please enter one of the following options: [all, monday, tuesday, wednesday, thursday, friday, saturday, sunday]: ").lower()

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
    df = pd.read_csv(CITY_DATA[city]) # load data in csv file into df

    df['Start Time'] = pd.to_datetime(df['Start Time']) # convert 'Start Time' column to datetime format
    df['month'] = df['Start Time'].dt.month # extract the month out of the datetime format and assign it to df['month']
    df['day of week'] = df['Start Time'].dt.day_name() # extract day of week out of 'Start Time' column
    df['Start Hour'] = df['Start Time'].dt.hour # extract the hour out of the 'Start Time' datetime column

    # filter by month, in case user hasn't selected 'all''
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 # convert the month name to number cuz it's written as number in the raw data,, i.e. january => 1
        df = df[df['month'] == month] # assign all filtered values into df

    # filter by day in case user hasn't selected 'all'
    if day != 'all':
        df = df[df['day of week'] == day.title()] # title case the selected day and user it to filter through day of week dataframe, then assign to df

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most common month: {}".format(df['month'].mode()[0])) 

    # display the most common day of week
    print("Most common day of week: {}".format(df['day of week'].mode()[0]))

    # display the most common start hour
    print("Most common start hour: {}".format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('Most common end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'] + " to " + df['End Station']
    print('Most common combination of start to end stations: {}'.format(df['start_to_end'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time: {}'.format(round(df['Trip Duration'].mean()))) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city): # adding city to args since Washington doesn't have a 'Gender' column
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("User types count:\n", user_types)

    # Display counts of gender, as long as city != washington
    if city != 'washington':
        genders_count = df['Gender'].value_counts().to_string()
        print("Genders count:\n", genders_count)
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print('Earliest birth year: ', earliest_birth_year)
        print('Most recent birth year: ',recent_birth_year)
        print('Most common birth year: ', common_birth_year)
    else:
        print("Washington's data does not include gender or birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    # to collect user input as to whether they wish to view 5 rows of raw data or not
    i = 0 # index to iterate through the csv, 5 rows at a time in the while loop below
    user_input = input('Would you like to view 5 rows of raw data? (Y/N): ').lower()

    while user_input not in ['y', 'n', 'yes', 'no']:
        user_input = input('{} is not a valid input, please enter Y or N: '.format(user_input)).lower()

    if user_input in ['n', 'no']:
        print('Have a nice day!')
    else:
        while i+5 < df.shape[0]:
            print(df.iloc[i:i+5]) # print all rows starting from row with index i to row with index i+5
            i += 5
            user_input = input('Would you like to view 5 more rows?(Y/N): ').lower()
            while user_input not in ['yes', 'y', 'no', 'n']:
                user_input = input('Invalid entry, please enter Y or N: ').lower()
            if user_input in ['yes', 'y']:
                continue
            else:
                print('Have a nice day!')
                break
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
