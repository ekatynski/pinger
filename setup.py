import os
import shutil
import stat

if __name__ == "__main__":

    # delete all contents of output folder if present
    if os.path.exists("output"):
        shutil.rmtree("output")
        os.makedirs("output")

    # delete the config file if it exists
    try:
        os.remove('pinger.sh')
    except FileNotFoundError:
        pass

    # collect all website names
    websites = []
    ping_count = int(input('Enter the amount of times you wish to ping each website: '))
    site_count = int(input('Enter the number of websites you wish to ping: '))
    print('Enter all website names, including the TLD (i.e. "google.com"): ')
    
    for i in range(site_count):
        websites.append(input('> '))
    
    # write shell file to run all ping requests in parallel
    with open('pinger.sh', 'w') as f:
        for site in websites:
            f.write(f'ping -w{ping_count} {site} >> {site.split(".")[0]+"_ping.txt"} &\n')

    # add execute permission for the new shell file
    st = os.stat('pinger.sh')
    os.chmod('pinger.sh', st.st_mode | stat.S_IEXEC)
