#
# Program by Calvin Frey, March-April 2023
#
# This program is designed to automate the URL generation and site collection on USGS' website
#
# When generating URLs using the website, for the purposes of this project, instantaneous data, stream watersheds,
# and a maximum of 40 square miles are constant.
#
# https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=ia&startDT=2001-01-01&endDT=2001-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40
#
# Version 1.3, years are also constant as 2000-2020.

# Import necessary modules
import urllib.request
import os
import shutil
import pandas as pd

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
print('Sites will be retrieved from 2000 through 2020.')

# Print template URL
url = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=' + 'STATE' + '&startDT=' + '20XX' + '-01-01&endDT=' \
     + '20XX' + '-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40'
print('For reference, here is the URL:')
print(url)

# Define a function to delete empty state folders
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


# Create state results directories if it does not already exist
if os.path.exists('USGS Search Results/' + state + '/text') == False:
    os.makedirs('USGS Search Results/' + state + '/text')
if os.path.exists('USGS Search Results/' + state + '/sites') == False:
    os.makedirs('USGS Search Results/' + state + '/sites')

# Begin main program section which imports years, creates the URL, downloads text file from the web, and extracts the
# sites from the text file

# Counter for while loop
index = 1

for year in years:

    # Insert desired values into the URL
    url = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=' + state + '&startDT=' + year + '-01-01&endDT=' \
          + year + '-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40'

    # Search and download the text file to the "USGS Search Results" folder
    file_name = state + '_' + year + '.txt'
    urllib.request.urlretrieve(url, file_name)

    # Extract sites from the raw text file
    # Open raw text file as a variable to be modified
    file = open(file_name, 'r')
    Lines = file.readlines()

    # Define the variables that will be updated with each correct line
    goodLines = []
    sites = []

    counter = 0

    # Remove file information and headers
    for line in Lines:
        if line[0] != '#':
            counter = counter + 1
            if counter > 2:
                goodLines.append(line)

    # Add the sites to the site variable
    for item in goodLines:
        sites.append(item[5:item.index('\t', 8)])

    # Close the text file variable
    file = 0

    # Read the text file, skip 62 rows, use column 2
    # sites_only = pd.read_csv(file_name, sep=r'\t{1,}', usecols=[2], skiprows=62, engine='python')
    # sites_only = pandas.read_csv(file_name, sep='\t', delimiter="", header=None)
    # print(sites_only)

    # Move the text file to the correct location
    shutil.move(file_name, 'USGS Search Results/' + state + '/text/' + file_name)

    # Convert the variable to a dataframe
    sites_df = pd.DataFrame(sites)

    # Use the dataframe to write a text file
    sites_text = state + '_' + year + '_sites.txt'
    sites_df.to_csv(sites_text, sep='\t', index=False, header=None)

    # Move the sites file to the correct location
    shutil.move(sites_text, 'USGS Search Results/' + state + '/sites/' + sites_text)

print('Site retrieval and storage is complete.')