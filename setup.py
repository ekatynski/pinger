import os
import stat

import dir_setup


# set up output directory and remove any prior scripts
def setup():
    # delete all contents of output folder if present
    dir_setup.dir_setup('output')

    # delete the pinger script if it exists
    try:
        os.remove('pinger.sh')
    except FileNotFoundError:
        pass

    # delete the manager script if it exists
    try:
        os.remove('manager.sh')
    except FileNotFoundError:
        pass


# set up script to run ping requests against all websites
def ping_script_setup():
    # collect all website names and ping request parameters
    websites = []
    ping_count = int(input('Enter the amount of times you wish to ping each website: '))
    site_count = int(input('Enter the number of websites you wish to ping: '))
    parallel_count = int(input('Enter the number of requests to run in parallel at one time: '))
    print('Enter all website names, including the TLD (i.e. "google.com"): ')

    for i in range(site_count):
        websites.append(input('> '))

    # write shell file to run all ping requests in parallel
    with open('pinger.sh', 'w') as f:
        i = 1
        f.write('#!/bin/bash\n')
        for site in websites:
            # author the ping requests
            f.write(f'ping -w{ping_count} {site} >> output/{site.split(".")[0] + "_ping.txt"}')
            # limit the number of scripts run in parallel
            if i % parallel_count != 0:
                f.write(' &')
            f.write('\n')
            i += 1

    # add execute permission for the new shell file
    st = os.stat('pinger.sh')
    os.chmod('pinger.sh', st.st_mode | stat.S_IEXEC)


# set up script to manage runs of ping request script
def manager_script_setup():
    # collect ping request timing details:
    operation_delay = int(input('Enter the delay (in minutes) between ping operations (max 1440): ')) % 1441
    operation_count = int(input('Enter the number of times you wish to run ping operations: '))

    # write shell file to run all ping requests in parallel
    with open('manager.sh', 'w') as f:
        f.write('count=1')  # create a loop to run the pinger script and then delay for a predetermined number of hours
        f.write(f'\nwhile [ $count -le {operation_count} ]')  # set loop for the number of requested executions
        f.write('\ndo')
        f.write('\n\techo "RUN: $count"')
        f.write('\n\tbash pinger.sh')  # execute ping requests
        f.write('\n\tsleep 2s')  # delay to ensure datestamp is placed after ping statistics
        f.write('\n\tfor file in output/*.txt; do')  # datestamp and newline at the end of each statistic file
        f.write('\n\t\techo "DATE: " `date` >> $file')
        f.write('\n\t\techo "" >> "$file"')
        f.write('\n\tdone')
        f.write(f'\n\tif [ $count -ne {operation_count} ]')
        f.write('\n\tthen')
        f.write('\n\t\techo "WAITING"')
        f.write(f'\n\t\tsleep {operation_delay}m')  # if not the last round of ping requests, wait the specified time
        f.write('\n\telse')
        f.write('\n\t\techo "DONE"')
        f.write('\n\tfi')
        f.write('\ncount=$((count+1))')
        f.write('\ndone')
        f.write('\npython3 calculate.py')  # call calculation script to tabulate results

    # add execute permission for the new shell file
    st = os.stat('manager.sh')
    os.chmod('manager.sh', st.st_mode | stat.S_IEXEC)


if __name__ == "__main__":
    setup()
    ping_script_setup()
    manager_script_setup()
