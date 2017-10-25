# Import required libraries 
import requests
import json
import datetime
import time
import os
import traceback
# Import API secrets file
import secrets 

# Create a file to log program progress as it runs
log_file = open("//CHFS/Shared Documents/OpenData/datasets/staging/library/flurry/flurrylog.txt", "a")
# Write date at beginning of log file
now = str(datetime.date.today())
log_file.write(now +"\n")

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    
    # Find date and create vars to hold the span of one day 
    # Write in format sierra understands
    now = str(datetime.date.today())
    one_day_ago = str(datetime.date.today() - datetime.timedelta(days=1))
    date_string = one_day_ago + "/" + now
    
    # Flurry API call, date string is updated to cover daily stats
    url = "https://api-metrics.flurry.com/public/v1/data/appUsage/day/company/app/language?metrics=sessions,activeDevices,newDevices,timeSpent,averageTimePerDevice,averageTimePerSession&dateTime=" + date_string
    # Take API token from secrets file
    headers = {"Authorization":"Bearer " + str(secrets.flurry_api_token)}
    # Access json data
    data = requests.get(url,headers=headers).json()
    data_list = data["rows"]
    
    # Write success to log file 
    log_file.write("Flurry data successfully accessed." + "\n")
    
    # Open the file to write/append to 
    # Stored in flurry folder with open data directory
    flurrycsv = open('//CHFS/Shared Documents/OpenData/datasets/staging/library/flurry/flurry.csv', "a")

    # Write CSV headings if the file is empty
    if os.stat("//CHFS/Shared Documents/OpenData/datasets/staging/library/flurry/flurry.csv").st_size == 0:
        flurrycsv.write("Company Name, Average Time Per Session, Active Devices, Language, Time Spent, Sessions, Date and Time, Average Time Per Device, App Name, New Devices"+"\n")

    # Set counter
    i = 0

    # Write/append the data to the file once the headings have been added
    # Write data in CSV format
    while i < len(data_list):
        flurrycsv.write(data_list[i]['company|name'] + ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerSession'])+ ", ")
        flurrycsv.write(str(data_list[i]['activeDevices'])+ ", ")
        flurrycsv.write(data_list[i]['language|name']+ ", ")
        flurrycsv.write(str(data_list[i]['timeSpent'])+ ", ")
        flurrycsv.write(str(data_list[i]['sessions'])+ ", ")
        flurrycsv.write(data_list[i]['dateTime']+ ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerDevice'])+ ", ")
        flurrycsv.write(data_list[i]['app|name']+ ", ")
        flurrycsv.write(str(data_list[i]['newDevices']))
        flurrycsv.write("\n")
        i += 1 
    flurrycsv.close()
    
    # Write success to log file 
    log_file.write("Flurry data successfully written to flurrydata directory. \n")
    
    # Copy flurry file to unpub direct
    f = open('//CHFS/Shared Documents/OpenData/datasets/staging/library/flurry/flurry.csv')
    f1 = open("//CHFS/Shared Documents/OpenData/datasets/staging/library/flurry/updatedflurry.csv", "w")
    for line in f:
        f1.write(line)
    log_file.write("Flurry data successfully copied into unpublished directory." + "\n")
   
# Main function
def main():
    
    # Handle exceptions, print errors to log file
    try:
        get_flurry()
    except Exception as exc:
        log_file.write("There was an error running the program.")
        log_file.write(traceback.format_exc() + "\n")

# Call main
main()
