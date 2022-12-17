import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():
    """
    This function asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #To get user input for city (chicago, new york city, washington).
    input_city=input("Which of the following cities would you like to see data for: chicago, new york, or washington? ")
    input_city=input_city.lower()
    
    #>>input validation<<
    while(input_city not in CITY_DATA.keys()):
        input_city=input('invalid input, re-enter the name of the city (chicago, new york, or washington): ')
        input_city=input_city.lower()
      
    # Assign 'city' variable to the appropriate file (for that city).
    if input_city == 'chicago' or input_city.lower() == 'new york' or input_city.lower() == 'washington':
        city= CITY_DATA[input_city]
    
    '''- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
             
    #To get user input for month (january, february, ... , june)
    try:
         input_month=int(input('\nWhich month would you like to see data for? \n0- All \n1- Jan. \n2- Feb. \n3- Mar.'+
               '\n4- Apr. \n5- May \n6- June \nEnter the number you choose: '))   
  
    except Exception as e:
        print("**Exception occurred: {}".format(e))
        input_month=int(input('invalid input, re-enter thenumber of the month would you like to see data for? '
                               +'(1, 2, 3, 4, 5, 6) : '))
    #>>input validation<<
    while(input_month not in [1, 2, 3, 4, 5, 6]):
               input_month=int(input('invalid input, re-enter thenumber of the month would you like to see data for? '
                               +'(1, 2, 3, 4, 5, 6) : ')) 
            
    if input_month==0:
        month='all'
    else:
        #Assign 'month' variable to the name of the month entered
        month=months[input_month-1]
    
    
    '''- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    
    #To get user input for day of week (all, monday, tuesday, ... sunday)
    try:
        input_day=int(input('\nWhich day would you like to see data for? \n1- Monday\n2- Tuesday\n3- Wednesday\n4- Thursday'
                            +'\n5- Frida\n6- Saturday\n7- Sunday\nEnter the number you choose: '))   
     
    except Exception as e:
        print("**Exception occurred: {}".format(e))
        input_day=int(input('invalid input, re-enter the number of the day would you like to see data for? '
                               +'(1, 2, 3, 4, 5, 6, 7) : ')) 
    
    #>>input validation<<
    while(input_day not in [1, 2, 3, 4, 5, 6, 7]):
            input_day=int(input('invalid input, re-enter the number of the day would you like to see data for? '
                               +'(1, 2, 3, 4, 5, 6, 7) : '))  
      
    #Assign 'day' variable to the name of the day
    day = days[input_day-1]

    #To enhance output format 
    print('-'*40)
    
    return city, month, day


def load_data(city, month, day):
    """
    This function used to load the data for the specified city and filters by month and day.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
        
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #load the data file into a dataframe  
    df = pd.read_csv(city)

    #convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['month'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    
    #To filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week
    df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """
    This function displays statistics on the most frequent times of travel.
    
    Args:
        (Dataframe) df - Pandas DataFrame containing city data filtered by month and day
        
    No returns (just printing)
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #To display the most common month   
    index_of_month = int(df['Start Time'].dt.month.mode())
    most_common_month = months[index_of_month - 1]
    print('The most common month is {}.'.format(most_common_month))
    
    #To display the most common day of week
    index_of_day = int(df['Start Time'].dt.dayofweek.mode())
    most_common_day = days[index_of_day]
    print('The most common day of week for start time is {}.'.format(most_common_day))

    #To display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour is {}:00'.format(common_hour))

    #prints time taken to throughout this process
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    #To enhance output format
    print('-'*40)


    
def station_stats(df):
    """
    This function Displays statistics on the most popular stations and trip.
    
    Args:
        (Dataframe) df - Pandas DataFrame containing city data filtered by month and day
        
    No returns (just printing)
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #To display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    common_start_uses_count = df[df['Start Station'] == common_start].count()[0]
    print("Most common start station {} was used {} times".format(common_start, common_start_uses_count))

    #To display most commonly used end station
    common_end = df['End Station'].mode()[0]
    common_end_uses_count = df[df['End Station'] == common_end].count()[0]
    print("Most common end station {} was used {} times".format(common_end, common_end_uses_count))

    #To display most frequent combination of start station and end station trip
    df['Trip'] = 'FROM ' + df['Start Station'] + ' TO '+ df['End Station']
    most_frequent_trip = df['Trip'].mode()[0]
    most_frequent_trip_count = df[df['Trip'] == most_frequent_trip].count()[0]
    print("Most frequent trip chosen by {} users is {}".format(most_frequent_trip_count, most_frequent_trip))
    
    #prints time taken to throughout this process
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    #To enhance output format
    print('-'*40)
    
def time_conversion(sec):
    """
    This function converts seconds to a human readable string representing duration.
    
    Args:
        (number) sec - number of seconds
        
    Returns:
        (str) time - how long number of seconds is in day:hour:minute:seconds format
    """

    sec = int(sec)
    str = ""

    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minute = sec // 60
    sec %= 60
    second = sec
    
    if day > 0: str += " {} day(s)".format(day)
    if hour > 0: str += " {} hour(s)".format(hour)
    if minute > 0: str += " {} minute(s)".format(minute)
    if second > 0: str += " {} second(s)".format(second)

    return str


def trip_duration_stats(df):
    """
    This function displays statistics on the total and average trip duration.
    
    Args:
        (Dataframe) df - Pandas DataFrame containing city data filtered by month and day
        
    No returns (just printing)
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #To display total travel time
    total_travel_time=df['Trip Duration'].sum() 
    print("Total travel time for all trips is {}".format(time_conversion(total_travel_time)))

    #To display mean travel time 
    mean_travel_time=df['Trip Duration'].mean()
    print("Mean travel time for all trips is {}".format(time_conversion(mean_travel_time)))

    #prints time taken to throughout this process
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    #To enhance output format
    print('-'*40)


def user_stats(df):
    """
    This function displays statistics on bikeshare users.
    
    Args:
        (Dataframe) df - Pandas DataFrame containing city data filtered by month and day
        
    No returns (just printing)
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #To display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    for ut in user_types: #ut -> user type
        print('There is/are {} occurence/s of {} user type'.format(user_types[ut], ut))
 
    #To enhance output format
    print('\n')
    
    #To display counts of gender 
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts().to_dict()
        for gt in gender_types: #gt -> gender type
            print('There is/are {} {} user/s'.format(gender_types[gt], gt))

    #To enhance output format
    print('\n')
    
    #To display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("The oldest user was born in {}".format(earliest))
        print("The youngest user was born in {}".format(most_recent))
        print("The most common birth year of a user is {}".format(most_common))
        
    #prints time taken to throughout this process
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    #To enhance output format
    print('-'*40)
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        count = 0
        while (input("Press enter to see row data (Enter 'no' to skip): ")!= 'no'):
            count = count+5
            print(df.head(count))
            
        
        restart = input('\nWould you like to restart? (Enter yes or no)\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()