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
state = input("Please enter the two letter state code (XX): ")

# Ensure that state is valid
while len(state) > 2:
    print('State is invalid. Please input two letter state code (ex. CA)')
    state = input('Please enter the two letter state code (XX): ')
state = str.upper(state)

# Import year
year = input('Please enter the year for which you would like to retrieve sites: ')

# Ensure that year is valid
year_int = int(year)
while year_int > 2023 or year_int < 1950:
    print('Year is invalid. Please input four digit year between 1950 and 2023.')
    year = input('Please enter the year for which you would like to retrieve sites: ')
    year_int = int(year)

# Insert desired values into the URL
url = 'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd=' + state + '&startDT=' + year + '-01-01&endDT=' \
    + year + '-12-31&siteOutput=expanded&siteType=ST&siteStatus=all&hasDataTypeCd=iv&drainAreaMax=40'
print('For reference, here is the URL:')
print(url)

# Create state results directories if it does not already exist
if os.path.exists('USGS Search Results/' + state + '/text') == False:
    os.makedirs('USGS Search Results/' + state + '/text')
if os.path.exists('USGS Search Results/' + state + '/sites') == False:
    os.makedirs('USGS Search Results/' + state + '/sites')

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

