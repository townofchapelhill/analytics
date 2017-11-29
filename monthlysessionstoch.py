"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import secrets
import traceback

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = "toch_secrets.json"

VIEW_ID = secrets.toch_viewid

def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.
  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

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
          'metrics': [{'expression': 'ga:sessions'}]
        }]
        
      }
  ).execute()


def print_response(response):
  
  # Change to correct path
  monthlysessions = open("//CHFS/Shared Documents/OpenData/datasets/staging/monthlytownsessions.csv", "w")
  """Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        monthly = (str(header.encode("utf-8")) + ': ' + str(dimension.encode("utf-8"))).replace("ga:sessions: ", "sessions, ")
        monthlystripped = monthly.replace('"',"")
        monthlysessions.write(monthlystripped + ", ")
        # print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          monthlyviews = (metricHeader.get('name') + ': ' + value).replace("ga:sessions: ", "sessions, ")
          viewsstripped = monthlyviews.replace('"', "")
          monthlysessions.write(viewsstripped + ", \n")
          # print metricHeader.get('name') + ': ' + value.encode("utf-8")
      
def main():
  log_file = open("analyticserror.txt", "a")
  try:
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    print_response(response)
  except Exception as exc:
        log_file.write("There was an error running the program.")
        log_file.write(traceback.format_exc() + "\n")
  

if __name__ == '__main__':
  main()
