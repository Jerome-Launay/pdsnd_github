# import pandas
import pandas as pd
import numpy as np
import datetime
import time

# This is the list of cities. It can easily be added to in the future.
# If a city is added to it, the cities_path will be created and the city and
# path will be added to the city_dict
cities = ['chicago', 'new york city', 'washington']
cities_path = [element.replace(' ', '_') + '.csv' for element in cities]
city_dict = dict(zip(cities, cities_path))
valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday\
', 'sunday', 'all']

def filter():
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" or None to apply
        no month filter
        (str) day - name of the day of week to filter by, or "all" or None to
        apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # Code block asking thefor the city to be analyzed
    print('\nWhich city do you want to analyze?\nEnter the index (integer) or'\
    'type the name of the city.')
    while True:
        try:
            #print('\nWhich city do you want to analyze?')
            for x in range(len(cities)):
                print('{}. {}'.format(x + 1, cities[x].title()))
            city = input()
            # Allows us to select by index based on the prompt
            if city.isdigit():
                city = cities[int(city) - 1]
                break
            # We can also select the city using some of the well known acronyms
            # for New York City and Washington DC. Not particularly useful
            # though as these are just special cases.
            elif city in ('nyc', 'new york'):
                city = 'new york city'
                break
            elif city in ('dc', 'd.c', 'd.c.'):
                city = 'washington'
                break
            elif city_dict.get(city.lower()) == None:
                print('\nData not available for this city. Please select a'\
                'city with available data from the list below.\nEnter the'\
                'index (integer) or type the name of the city.')
                continue
            else:
                break
        except IndexError:
            print('\nOut of index. Please select a city based on the index\
            below or type the name of the city.')
    # Code block asking for the date filter
    while True:
        try:
            print('\nDo you want to filter by month, day of the week or all?\n'
            'Enter \'month\', \'day\' or \'all\'')
            f = input()
            if f.lower() not in ('month', 'day', 'all'):
                print('Please enter \'month\', \'day\' or \'all\'.')
                continue
            elif f == 'month':
                day = None
                print('\nWhich month - January, February, March, April, May,'\
                'or June?')
                month = input()
                while month.lower() not in valid_months:
                    print('\nNot a valid month. Please enter a valid month.'\
                    'Valid values are:')
                    for m in range(len(valid_months)):
                        print(valid_months[m].title())
                    month = input()
                break
            elif f == 'day':
                month = None
                print ('\nWhich day of the week?')
                day = input()
                while day.lower() not in valid_days:
                    print('Not a valid day of the week. Please, enter a valid'\
                    'day of the week. Valid avalues are:')
                    for d in range(len(valid_days)):
                        print(valid_days[d].title())
                    day = input()
                break
            else:
                month, day = None, None
                break
        # error message for KeyboardInterrupt
        except KeyboardInterrupt:
            print('No input taken.')
    if f == 'day':
        print('\nWe will be analyzing {}, filtered by {} ({}).'
        .format(city.title(), f, day.title()))
    elif f == 'month':
        print('\nWe will be analyzing {}, filtered by {} ({}).'
        .format(city.title(), f, month.title()))
    else:
        print('\nWe will be analyzing {} unfiltered.'.format(city.title()))
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if\
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no\
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no\
        day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(city_dict[city])
    # convert the Start Time column to datetime
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    # extract month and day of week from Start Time to create new columns
    data['month'] = pd.DatetimeIndex(data['Start Time']).month
    data['day_of_week'] = pd.DatetimeIndex(data['Start Time']).dayofweek
    # filter by month if applicable
    if month != 'all' and month != None:
        # use the index of the months list to get the corresponding int
        month = valid_months.index(month) + 1
        # filter by month to create the new dataframe
        data = data[data['month'] == month]
    # filter by day of week if applicable
    if day != 'all' and day != None:
        day = valid_days.index(day)
        # filter by day of week to create the new dataframe
        data = data[data['day_of_week'] == day]
    return data

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('The most popular hour is {}:00.'.format(popular_hour))
    # Will only calculate the popular month if we are NOT filtering by month
    if df.groupby(['month'])['month'].nunique().sum() > 1:
        popular_month = df['month'].value_counts().idxmax()
        print('The most popular month is {}.'.format(valid_months[popular_month]
        .title()))
    # Will only calculate the popular day if we are NOT filtering by day
    if df.groupby(['day_of_week'])['day_of_week'].nunique().sum() > 1:
        popular_day = df['day_of_week'].value_counts().idxmax()
        print('The most popular day is {}.'.format(valid_days[popular_day]
        .title()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    popular_start = df['Start Station'].value_counts().idxmax()
    print('The most popular start station is {}.'.format(popular_start))
    # Will only calculate the popular month if we are NOT filtering by month
    popular_end = df['End Station'].value_counts().idxmax()
    print('The most popular end station is {}.'.format(popular_end))
    # Will only calculate the popular day if we are NOT filtering by day
    df['Trip'] = df['Start Station'] + ' and ' + df['End Station']
    popular_trip = df['Trip'].value_counts().idxmax()
    print('The most popular trip is between {}.'.format(popular_trip))

def trip_duration_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Calculate the avergae trip duration using numpy (faster)
    avg_dur_s = np.fix(np.average(df['Trip Duration']))
    avg_dur = datetime.timedelta(seconds = avg_dur_s)
    sum_dur_s = np.fix(np.sum(df['Trip Duration']))
    sum_dur = datetime.timedelta(seconds = sum_dur_s)
    # Round and remove the decimal
    #print('The average trip time is {} seconds.'.format(int(np.fix(avg_dur))))
    print('The average trip time is {}.'.format(avg_dur))
    print('The sum total of the trips took {}.'. format(sum_dur))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types.to_string(), '\n')
    # Display counts of gender
    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        gender_counts = df.groupby(['Gender'])['Gender'].count()
        print(gender_counts.to_string(), '\n')
        # Display earliest, most recent, and most common year of birth
        min_birth = int(df['Birth Year'].min())
        max_birth = int(df['Birth Year'].max())
        print('The oldest user was born in {}.\nThe youngest user was born in'\
        '{}.'.format(min_birth, max_birth))
    # If gender or birth year not available, print 'no further user data
    # available'
    else:
        print('There is no further user data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = filter()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask if the user wants to display data
        display = input('\nWould you like to display the data? Enter yes or'\
        ' no.\n')
        frames = 0
        # while loop to display 5 more rows every time user selects 'yes'
        while display.lower() == 'yes':
            print(df.iloc[list(range(frames, frames + 5))].to_string())
            frames += 5
            display = input('\nWould you like to display more data? Enter yes'\
            ' or no.\n')

        restart = input('\n\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
