# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# Created by Tao Huang, August 2020, in Python 3.7
#
# Script to download and visualize the discharge data from NWIS, USGS
# and separate the flood events with a single peak
#
# Version 2.0
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Program heavily modified by Calvin Frey during March-April 2023
# It is now able to retrieve data for all years between 2000 and 2020 for a given state at once

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import hydrofunctions as hf
from scipy.signal import find_peaks
import time

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

# Define a function to delete empty flood event folders
def delete_empty(path):
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if os.path.isdir(folder_path):
            try:
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")
            except OSError:
                # The folder is not empty or there is no permission to delete it
                pass

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

# Define years
years = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
         '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
         '2018', '2019', '2020']

for year in years:
    # Stop program if data already exists for this state and year to save time
    if os.path.exists(state + '/' + state + '_' + year) == True:
        print('* ' * 20)
        print("You already have data for these sites (" + state + '_' + year + ')')
        print('* ' * 20)

        # Convert year into start and end dates
        begin_date = year + '-01-01'
        end_date = year + '-12-31'

        # read all the gauge number from the TXT file
        sites_file = 'USGS Search Results/' + state + '/sites/' + state + '_' + year + '_sites.txt'
        site_no = np.genfromtxt(sites_file, dtype=str)

        Results = [None] * len(site_no)
        i = 0

        for site in site_no:
            try:
                GetFlow(site, begin_date, end_date, state)
                delete_empty(state + '/' + state + '_' + year + '/Flood_Events')
                delete_empty(state + '/' + state + '_' + year + '/Raw_Data')

            # skip the Nodata error and continue
            except Exception as msg:
                print("* " * 20)
                print("Warnings for " + site + ":", msg)
                print("Please try again later!")
                print("* " * 20)

                Results[i] = 0
                i = i + 1

            else:
                no = i + 1
                print(state + '_' + year + ": Gauge " + site + " is done! (" + str(no) + '/' + str(
                    len(site_no)) + ')')

                Results[i] = 1
                i = i + 1

            continue
        '''
        for R in Results:
            print(R)
        '''



print("Discharge data processing is done!")
