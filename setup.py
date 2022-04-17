import os
import json

if __name__ == "__main__":

    # delete the config file if it exists
    try:
        os.remove("config.json")
    except FileNotFoundError:
        pass

    # collect all website names
    websites = []
    ping_count = int(input("Enter the amount of times you wish to ping each website: "))
    site_count = int(input("Enter the number of websites you wish to ping: "))
    print("Enter all website names, after 'www.' and before the TLD (i.e. www.google.com -> google): ")
    
    for i in range(site_count):
        websites.append(input("> "))

    # format JSON output data in a dictionary
    json_data = {"pingCount":ping_count, "siteCount":site_count, "websites":websites}
    
    # plant dictionary into config file
    with open('config.json', 'w') as fp:
        json.dump(json_data, fp)
