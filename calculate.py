import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

def plot_frames(frame):
    # melt frame for easier auto-coloring using seaborn plots
    frame_melt = frame.melt('timestamp', var_name = 'Website', value_name = 'RTT (ms)')

    # print descriptive statistics regarding ping request data
    frame.drop([0])
    print(frame.describe())

    # present all RTT data points as a scatter plot
    sns.scatterplot(data = frame_melt, x = 'timestamp', y = 'RTT (ms)', hue = 'Website')
    plt.title('Ping Requst RTTs for Various Websites')
    plt.xlabel('Timestamp (D - HH:MM)')
    plt.show()

if __name__ == "__main__":
    dir_setup.dir_setup("output/results")
    directory = os.fsencode('output')
    frame_results = pd.DataFrame(columns = ['timestamp'])

    # iterate through all output ping data files for analysis
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # only examine text files
        if filename.endswith('.txt'):
            # read from the file and extract the website, ping timestamps, loss rate, and RTT stats into a dict per site
            current = read_file(filename)
            # populate timestamp column if empty
            if frame_results.empty:
                frame_results['timestamp'] = current['timestamp']
            frame_results[filename.split('_')[0]] = current['rtt']
    
    # plot results
    plot_frames(frame_results)

    print("\nDone!")