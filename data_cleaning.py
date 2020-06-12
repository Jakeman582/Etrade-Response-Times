"""
Name:
    data_cleaning.py
Author:
    Jacob Hiance (Jakeman582)
Purpose:
    Clean data generated by the measure_response_times.py script in order to
    ensure the data collected can be used for further analysis. Also, we may
    need to add additional columns so as to more easily describe and analyze
    collected data
"""

import pandas   # pandas.DataFrame, pandas.DataFrame.read_csv()
import math     # math.ceil()

def clean_data():

    # The data files are observations.txt and exceptions.txt
    observations_file = "observations.txt"
    exceptions_file = "exceptions.txt"
    clean_observations_file = "cleaned_observations.txt"
    clean_exceptions_file = "cleaned_exceptions.txt"

    observation_frame = pandas.read_csv(observations_file, usecols = [0, 1],
        names = ['date_time', 'response_time'], parse_dates = [0, 1],
        infer_datetime_format = True)
    exception_frame = pandas.read_csv(exceptions_file, usecols = [0, 1],
        names = ['date_time', 'exception'])

    # The second column of data are timedelta objects, which we can turn into
    # milliseconds by dividing the number of microseconds by 1000
    observation_frame['response_time'] = observation_frame['response_time'].apply(lambda x: x.microsecond / 1000)
    observation_frame['response_time_bucket'] = observation_frame['response_time'].apply(lambda x: math.ceil(x))

    # We may want to break down response times by hour of day
    observation_frame['date_time_hour_bucket'] = observation_frame['date_time'].apply(lambda x: x.hour)

    # write out the cleaned data files
    observation_frame.to_csv(clean_observations_file, index = False)
    exception_frame.to_csv(clean_exceptions_file, index = False)

if __name__ == "__main__":
    clean_data()