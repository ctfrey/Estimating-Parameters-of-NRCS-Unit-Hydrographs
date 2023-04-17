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


# Import year
num_years = input('How many years would you like to retrieve sites for?: ')
num_years_int = int(num_years)
while num_years_int <= 0 or num_years_int > 25:
    print('Invalid number of years. Please make sure that the number is positive and less than or equal to 25.')
    num_years = input('How many years would you like to retrieve sites for?: ')
    num_years_int = int(years)

# Create state results directories if it does not already exist
if os.path.exists('USGS Search Results/' + state + '/text') == False:
    os.makedirs('USGS Search Results/' + state + '/text')
if os.path.exists('USGS Search Results/' + state + '/sites') == False:
    os.makedirs('USGS Search Results/' + state + '/sites')

# Begin main program section which imports years, creates the URL, downloads text file from the web, and extracts the
# sites from the text file

# Counter for while loop
index = 1

while index <= num_years_int:
    if index == 1:

        # Input first year
        rn = input('Please input the first year you would like to retrieve sites for: ')
        rn_int = int(rn)

        # Ensure that first year is valid
        while rn_int > 2023 or rn_int < 1950:
            print('Year is invalid. Please input four digit year between 1950 and 2023.')
            year = input('Please enter the year for which you would like to retrieve sites: ')
            rn_int = int(rn)

        # Insert required information into the template URL
        url = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=' + state + '&startDT=' + rn + '-01-01&endDT=' \
              + rn + '-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40'
        print('For reference, here is the URL:')
        print(url)

        # Search and download the text file to the "USGS Search Results" folder
        file_name = state + '_' + rn + '.txt'
        urllib.request.urlretrieve(url, file_name)

        # Extract sites from the raw text file
        # Open raw text file as a variable to be modified
        file = open(file_name, 'r')
        Lines = file.readlines()

        # Define the variables that will be updated with each correct line
        goodLines = []
        sites = []

        # Counter for for loop
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

        # Move the text file to the correct location
        shutil.move(file_name, 'USGS Search Results/' + state + '/text/' + file_name)

        # Convert the variable to a dataframe
        sites_df = pd.DataFrame(sites)

        # Use the dataframe to write a text file
        sites_text = state + '_' + rn + '_sites.txt'
        sites_df.to_csv(sites_text, sep='\t', index=False, header=None)

        # Move the sites file to the correct location
        shutil.move(sites_text, 'USGS Search Results/' + state + '/sites/' + sites_text)
        index = index + 1
    else:

        # Input subsequent years
        rn = input('Please input the next year you would like to retrieve sites for: ')
        rn_int = int(rn)

        # Ensure that subsequent years are valid
        while rn_int > 2023 or rn_int < 1950:
            print('Year is invalid. Please input four digit year between 1950 and 2023.')
            year = input('Please enter the year for which you would like to retrieve sites: ')
            rn_int = int(rn)

        # Insert required information into the template URL
        url = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=' + state + '&startDT=' + rn + '-01-01&endDT=' \
              + rn + '-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40'
        print('For reference, here is the URL:')
        print(url)

        # Search and download the text file to the "USGS Search Results" folder
        file_name = state + '_' + rn + '.txt'
        urllib.request.urlretrieve(url, file_name)

        # Extract sites from the raw text file
        # Open raw text file as a variable to be modified
        file = open(file_name, 'r')
        Lines = file.readlines()

        # Define the variables that will be updated with each correct line
        goodLines = []
        sites = []

        # Counter for for loop
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

        # Move the text file to the correct location
        shutil.move(file_name, 'USGS Search Results/' + state + '/text/' + file_name)

        # Convert the variable to a dataframe
        sites_df = pd.DataFrame(sites)

        # Use the dataframe to write a text file
        sites_text = state + '_' + rn + '_sites.txt'
        sites_df.to_csv(sites_text, sep='\t', index=False, header=None)

        # Move the sites file to the correct location
        shutil.move(sites_text, 'USGS Search Results/' + state + '/sites/' + sites_text)
        index = index + 1

print('Site retrieval and storage is complete.')