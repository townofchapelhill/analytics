"""Hello Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import secrets
import datetime
import filename_secrets

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = "client_secrets.json"

VIEW_ID = secrets.viewid

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
          'dateRanges': [{'startDate': '1daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:searchResultViews'}],
          'dimensions': [{'name': 'ga:searchKeyword'}],
        }]
        
      }
  ).execute()


"""
  Parses and prints the Analytics Reporting API V4 response.
  Args:
    response: An Analytics Reporting API V4 response.
"""
def print_response(response):
  
  # Open CSV to store data
  fullfilename = os.path.join(filename_secrets.productionStaging, "dailysearch.csv")
  dailysearch = open(fullfilename, "w", encoding='utf-8')

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    
    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for header, dimension in zip(dimensionHeaders, dimensions):
        daily = (header.encode("utf-8") + ': ' + dimension.encode("utf-8")).replace("ga:searchKeyword: ", "")
        dailystripped = daily.replace('"',"")
        dailystripped = dailystripped.replace(",","")
        dailysearch.write(dailystripped + ", ")
        print header + ': ' + dimension

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          monthlyviews = (metricHeader.get('name') + ': ' + value).replace("ga:searchResultViews: ", "")
          viewsstripped = monthlyviews.replace('"', "")
          viewsstripped = viewsstripped.replace(",","")
          dailysearch.write(viewsstripped + ", " + str(datetime.datetime.now()) + "\n")
          print metricHeader.get('name') + ': ' + value.encode("utf-8")

  dailysearch.close()

def main():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  print_response(response)

if __name__ == '__main__':
  main()
