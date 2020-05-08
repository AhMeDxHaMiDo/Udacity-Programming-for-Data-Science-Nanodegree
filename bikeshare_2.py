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
    city = input("Which city would you like to filter by? \n'Chicago', 'New York City', 'Washington'\n").strip().lower()
    while True:
        if city in CITY_DATA.keys():
            break
        else:
            print("Invalid Input, Please Try Again With The Correct City!")
            city = input("City Name: ").strip().lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to filter by? \n'All', 'January', 'February', ... , 'June'\n").strip().lower()
    while True:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

        if month in months:
            break
        else:
            print("Invalid Input, Please Try Again With The Correct Month!")
            month = input("Month Name or All: ").strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to filter by? \n'All', 'Saturday', 'Sunday', ... , 'Friday'\n").strip().lower()
    while True:
        weekdays = ['all', 'sunday', 'monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday']

        if day in weekdays:
            break
        else:
            print("Invalid Input, Please Try Again With The Correct Day!")
            day = input("Day Name: ").strip().lower()


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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The Most Frequent Month: ', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The Most Frequent Day of Week: ', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The Most Frequent Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The Most Popular Start Station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The Most Popular End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df_start_end_combination = df.copy()
    df_start_end_combination['Start and End Stations'] = df['Start Station'] + ', ' + df['End Station']
    popular_start_end_station = df_start_end_combination['Start and End Stations'].mode()[0]
    print('The Most Popular Start and End stations: ', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    max_time = df['Trip Duration'].max()
    print('Total Travel Time: {:.2f} Min, and {:.2f} Sec'.format(max_time//60, max_time%60))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean Travel Time: {:.2f} Min, and {:.2f} Sec'.format(mean_time//60, mean_time%60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of User Types")
    for type, count in user_types.items():
        print("\t", type, ": ", count)

    # Display counts of gender
    genders = df['Gender'].value_counts()
    print("Counts of Gender")
    for gender, count in genders.items():
        print("\t", gender, ": ", count)

    # Display earliest, most recent, and most common year of birth
    earliest_birth_year = int(df['Birth Year'].min())
    recent_birth_year = int(df['Birth Year'].max())
    common_birth_year = int(df['Birth Year'].mode()[0])

    print("Earliest Year of Birth: ", earliest_birth_year)
    print("Recent Year of Birth: ", recent_birth_year)
    print("Common Year of Birth: ", common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays multiples of 5 raw data."""
    display_raw_input = input("\nWould you like to see 5 lines of raw data? Enter 'Yes' or 'No'\n").strip().lower()
    num_rows = 5
    while True:
        if display_raw_input == 'no':
            break
        elif display_raw_input == 'yes':
            print(df.iloc[num_rows - 5 : num_rows, :])
            print('-'*40)

            num_rows += 5
            display_raw_input = input("Would you like to see the next 5 lines of raw data? Enter 'Yes' or 'No'\n").strip().lower()
        else:
            print("Invalid Input, Please Enter 'Yes' or 'No'!")
            display_raw_input = input("Would you like to see 5 lines of raw data?\n").strip().lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input("\nWould you like to restart? Enter 'Yes' or 'No'.\n").strip().lower()

        if restart not in ('yes', 'no'):
            while True:
                print("Invalid Input, Please Enter 'Yes' or 'No'!")
                restart = input("\nWould you like to restart? Enter 'Yes' or 'No'.\n").strip().lower()
                if restart in ('yes', 'no'):
                    break

        if restart == 'no':
            break


if __name__ == "__main__":
	main()
