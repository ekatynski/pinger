from audioop import avg
from logging.handlers import DatagramHandler
import os
import pandas as pd
# import matplotlib
from dateutil import parser


import dir_setup

def read_file(filename):
    filename = 'output/' + filename
    result = {'requests': 0, 'min': float('inf'), 'max': 0, 'avg': 0, 'data': []}

    with open(filename, 'r') as f:
            line = f.readline()
            # before the file ends
            while line:
                # if you reach the ping statistics header
                if 'statistics' in line:
                    result['requests'] += 1

                    # extract packet loss percentage
                    line = f.readline()
                    pl_percent = float(line.split(',')[2].split('%')[0])

                    # extract rtt statistics
                    line = f.readline()
                    rtt_vals = line.split('=')[1].split('/')[0:3]
                    rtt_stats = {'min':float(rtt_vals[0]), 'avg':float(rtt_vals[1]), 'max':float(rtt_vals[2])}

                    # extract the timestamp
                    line = f.readline()
                    date = parser.parse(line[11:len(line) - 5])

                    # process data for return
                    result['data'].append({'packet_loss': pl_percent, 'stats': rtt_stats, 'date': date})
                    result['avg'] += rtt_stats['avg']
                    if rtt_stats['min'] < result['min']: result['min'] = rtt_stats['min']
                    if rtt_stats['max'] > result['max']: result['max'] = rtt_stats['max']

                    # advance to the next line
                    line = f.readline()

                else:
                    # skip the line
                    line = f.readline()

    # calculate average rtt
    result['avg'] = round(result['avg'] / result['requests'], 3)
    return result

if __name__ == "__main__":
    dir_setup.dir_setup("output/results")
    directory = os.fsencode('output')
    
    ping_results = {}
    frame_results = pd.DataFrame(columns=['name', 'min', 'max', 'avg', 'timestamp'])

    # iterate through all output ping data files for analysis
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.txt'):
            website_name = filename.split('.')[0]

            # read from the file and extract the website, ping timestamps, loss rate, and RTT stats into a dict per site
            ping_results[website_name] = read_file(filename)
        
            # insert website data into dataframe
            for item in ping_results[website_name]['data']:
                for request in item['stats']:
                    new_row = {'name': website_name.split('_')[0], 'min': item['stats']['min'], 'max': item['stats']['max'], 'avg': item['stats']['avg'], 'timestamp': item['date']}
                    frame_results = frame_results.append(new_row, ignore_index=True)
        
    print(frame_results)
    
