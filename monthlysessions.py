"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import secrets
import traceback
import datetime
import csv
import os

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = "client_secrets.json"

VIEW_ID = secrets.viewid


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
                    'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                }]
        }
    ).execute()


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.
    Args:
        response: An Analytics Reporting API V4 response.
    """
    monthlysessions = open("//CHFS/Shared Documents/OpenData/datasets/staging/monthlysessions.csv", "a")
    writer = csv.writer(monthlysessions)

    if os.stat("//CHFS/Shared Documents/OpenData/datasets/staging/monthlysessions.csv").st_size == 0:
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
    log_file = open("monthlysessionserror.txt", "a")
    try:
        analytics = initialize_analyticsreporting()
        response = get_report(analytics)
        print_response(response)
    except RuntimeError:
        log_file.write("There was an error running the program.")
        log_file.write(traceback.format_exc() + "\n")


if __name__ == '__main__':
    main()
