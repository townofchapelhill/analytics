"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import secrets
import traceback
import datetime
import csv
import os

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = "toch_secrets.json"

VIEW_ID = secrets.toch_viewid


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.
    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
    """Queries the Analytics Reporting API V4.
    Args:
        analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
        The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '1daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}]
                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.
    Args:
        response: An Analytics Reporting API V4 response.
    """
    dailysessions = open("//CHFS/Shared Documents/OpenData/datasets/staging/dailytownsessions.csv", "a")
    writer = csv.writer(dailysessions)

    if os.stat("//CHFS/Shared Documents/OpenData/datasets/staging/dailytownsessions.csv").st_size == 0:
        writer.writerow(['sessions', 'session count', 'date'])

    for report in response.get('reports', []):
        metric_headers = report.get('columnHeader', {}).get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            date_range_values = row.get('metrics', [])

            for i, values in enumerate(date_range_values):
                for metric_header, value in zip(metric_headers, values.get('values')):
                    writer.writerow(['sessions', value, str(datetime.datetime.now())])


def main():
    log_file = open("dailytownsessionserror.txt", "a")
    try:
        analytics = initialize_analyticsreporting()
        response = get_report(analytics)
        print_response(response)
    except RuntimeError:
        log_file.write("There was an error running the program.")
        log_file.write(traceback.format_exc() + "\n")


if __name__ == '__main__':
    main()
    
    
    # Create file to log exception handling
log_file = open("dailytownsessionserror.txt", "a")

# Import modules/libraries
try: 
    from apiclient.discovery import build
    from oauth2client.service_account import ServiceAccountCredentials
    import secrets
    import traceback
    import datetime
    import csv
    import os
except:
    print("Could not import all libraries.")
    log_file.write("Library Import Failed")
    log_file.write(traceback.format_exc())

# Authentication 
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = "client_secrets.json"
VIEW_ID = secrets.toch_viewid

# Initialize with credentials   
# Initializes an Analytics Reporting API V4 service object. Returns: An authorized Analytics Reporting API V4 service object.
def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

# Get the metrics for the date range
def get_report(analytics):
    #Queries the Analytics Reporting API V4.Args: analytics: An authorized Analytics Reporting API V4 service object. Returns: The Analytics Reporting API V4 response.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '1daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'},{'expression': 'ga:users'},{'expression': 'ga:avgSessionDuration'},{'expression': 'ga:percentNewSessions'}]
                }]
        }
    ).execute()

# Write the response    
# Parses and prints the Analytics Reporting API V4 response. Args: response: An Analytics Reporting API V4 response.
def print_response(response):
    
    # Create CSV to store data
    dailytownsessions = open("//CHFS/Shared Documents/OpenData/datasets/staging/dailytownsessions", "a")

    # Iterate through response data to write headers and data    
    for report in response.get('reports', []):
        metric_headers = report.get('columnHeader', {}).get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            date_range_values = row.get('metrics', [])
            for i, values in enumerate(date_range_values):
                # Write headers to csv
                for header in metric_headers:
                    # Write headers only if file is empty
                    if os.stat("//CHFS/Shared Documents/OpenData/datasets/staging/dailytownsessions").st_size == 0:
                        dailytownsessions.write(header['name'] + ", ")
                # Add date and enter if file is empty -- set here to avoid messing up headers in loop
                if os.stat("//CHFS/Shared Documents/OpenData/datasets/staging/dailytownsessions").st_size == 0:
                    dailytownsessions.write("Date, \n")
                # Write values under headers
                for metricvalue in values['values']:
                    dailytownsessions.write(metricvalue + ", ")
                # End row by writing the date and a new line
                dailytownsessions.write(str(datetime.datetime.now()) + ", \n")

# Call functions
def main():
    print("Retreiving Google Analytics data...")
    try:
        analytics = initialize_analyticsreporting()
        response = get_report(analytics)
        print_response(response)
    except RuntimeError:
        log_file.write("There was an error running the program.")
        log_file.write(traceback.format_exc() + "\n")
    print("Analytics data collected and written to CSV.")

# Call main
if __name__ == '__main__':
    main()
