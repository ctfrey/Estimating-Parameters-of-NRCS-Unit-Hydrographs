# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, August 2020, in Python 3.7
#
# Script to download and visualize the discharge data from NWIS, USGS
# and separate the flood events with a single peak
#
# Version 1.0        
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Program heavily modified by Calvin Frey during March-April 2023

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import hydrofunctions as hf
from scipy.signal import find_peaks

## function to create a folder to store the results if it does not exist

def ResultsFolder(Folder):
    if os.path.exists(Folder) == False:
        os.makedirs(Folder)

## A function to obtain the peak flow data of a USGS gauge

def GetFlow(site_no,begin_date,end_date,state):
    # download the discharge data (instantaneous values,15-min) from NWIS

    # Raw data stuff
    Folder1 = state + '/' + state + '_' + year + '/Raw_Data/Raw_Data_' + site_no + '/'
    ResultsFolder(Folder1)

    # Flood data stuff
    Folder2 = state + '/' + state + '_' + year + '/Flood_Events/Flood_Events_' + site_no + '/'
    ResultsFolder(Folder2)

    discharge = hf.NWIS(site_no, 'iv', begin_date, end_date)
    #print("meow")
    discharge.get_data()
    #print("success")

    # save the data as TXT and CSV and store them in the "Raw_Data" folder

    raw_data = pd.DataFrame({'discharge_cfs':discharge.df().iloc[:,0],
                          'qualifiers':discharge.df().iloc[:,1]})
    raw_data.to_csv(Folder1 + "Raw_Discharge_" + site_no + ".txt")
    raw_data.to_csv(Folder1 + "Raw_Discharge_" + site_no + ".csv")
    #print('yes!')

    # generate a discharge hydrograph and save as JPEG, and store them in the "Raw_Data" folder

    flow = pd.DataFrame(raw_data['discharge_cfs'])

    flow.plot(figsize=(12,6))
    plt.title("Discharge Hydrograph of "+ site_no)
    plt.legend(["Discharge"], loc='best',edgecolor='k')
    plt.xlabel("Date")
    plt.ylabel("Discharge (cfs)")
    plt.savefig(Folder1 + "Discharge_" + site_no +".jpeg")
    plt.close()

    # find the peak flow and store separately the data of each flood event

    # set minimal prominence as 40 cfs(the difference between peak and its nearest lowest point)

    peaks,_ =find_peaks(flow['discharge_cfs'],prominence=40)

    # separate the flood event(assuming that duration is about 5 days) and save as JPEG and CSV
    # store them in the "Flood_Events" folder

    event_no = 1

    for index in peaks:
    
        if index-200 < 0:
            start = 0
        else:
            start = index-200
        end = index + 200
    
        flood_event=flow[start:end]
    
        flood_event.plot(figsize=(12,6))
        peakvalue = flow[index:index+1]
        plt.scatter(peakvalue.index,peakvalue['discharge_cfs'],color='r')
        plt.title("Flood Event " + str(event_no) +" of "+ site_no)
        plt.legend(["Discharge","Peak Rate"], loc='best',edgecolor='k')
        plt.xlabel("Date")
        plt.ylabel("Discharge (cfs)")
        plt.savefig(Folder2 + "Flood_Event_" + str(event_no) +"_"+ site_no +".jpeg")
        plt.close()

        flood_event.to_csv(Folder2 + "Flood_Event_" + str(event_no) +"_"+ site_no +".csv")
    
        event_no = event_no + 1

## main program

# Import necessary information
# Import state
#state = input("Please enter the two letter state code (XX): ")

# Ensure that state is valid
# List of valid state codes
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# Loop while state input is not valid
valid_input = False
while not valid_input:
    state = input("Please enter the two letter state code (XX): ").upper()
    if state in states:
        valid_input = True
    else:
        print("Invalid state code. Please enter a valid US state postal code (ex. CA).")

# Import year
year = input('Please enter the year for which you would like to retrieve sites: ')

# Ensure that year is valid
year_int = int(year)
while year_int > 2023 or year_int < 1950:
    print('Year is invalid. Please input four digit year between 1950 and 2023.')
    year = input('Please enter the year for which you would like to retrieve sites: ')
    year_int = int(year)

# Convert year into start and end dates
begin_date = year + '-01-01'
end_date = year + '-12-31'

# read all the gauge number from the TXT file
sites_file = 'USGS Search Results/' + state + '/sites/' + state + '_' + year + '_sites.txt'
site_no = np.genfromtxt(sites_file, dtype=str)
#print('The below array displays the sites to be analyzed')
#print(site_no)

# input the intended prominence value
#prom = input("Please input the desired value of peak prominence in cubic feet per second: ")

Results = [None]*len(site_no)
i = 0

for site in site_no:
    try:
        GetFlow(site,begin_date,end_date,state)

    # skip the Nodata error and continue
    except Exception as msg:
        print("* "*20)
        print("Warnings for " + site + ":",msg)
        print("Please try again later!")
        print("* "*20)

        Results[i]=0
        i=i+1

    else:
        no = i + 1
        print("Gauge " + site + " is done! (" + str(no) + '/' + str(len(site_no)) + ')')
        
        Results[i]=1
        i=i+1
        
    continue
'''
for R in Results:
    print(R)
'''    
print("Discharge data processing is done!")
