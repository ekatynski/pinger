from ast import Interactive
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import interactive
from dateutil import parser
import dir_setup

def read_file(filename):
    filename = 'output/' + filename
    rtt_times = []
    rtt_stamps = []
    rtt_count = 0

    with open(filename, 'r') as f:
            line = f.readline()
            # before the file ends
            while line:
                if 'time=' in line:
                    # extract RTT time from line
                    rtt_count += 1
                    rtt_times.append(float((line.split('=')[3])[:4])) 
                    line = f.readline()

                elif 'DATE:' in line:
                    # extract the timestamp
                    date = parser.parse(line[11:len(line) - 5])
                    rtt_stamps = rtt_stamps + ([date] * rtt_count)

                    # advance to the next line
                    rtt_count = 0
                    line = f.readline()

                else:
                    # skip the line
                    line = f.readline()

    # produce dataframe to return
    data = {'rtt': rtt_times, 'timestamp': rtt_stamps}
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    dir_setup.dir_setup("output/results")
    directory = os.fsencode('output')
    
    frame_results = {}
    website_names = []

    # iterate through all output ping data files for analysis
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.txt'):
            website_names.append(filename.split('_')[0])

            # read from the file and extract the website, ping timestamps, loss rate, and RTT stats into a dict per site
            frame_results[filename.split('.')[0]] = read_file(filename)
        
            # insert website data into dataframe
    
    print(frame_results)
    print("\nDone!")