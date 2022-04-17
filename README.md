# pinger

An attempt to automate a data-collection function for a networking class.

To use, run setup.py in python3. You will be prompted for the number of websites and the respective URLs you wish to ping. Please skip the "www." in your URLs but feel free to include any extensions after your TLD. Note: multiple pings to the same site may result in errors, the output files are named using prior to the TLD and this may cause name overwrites.

After running setup.py, you will have a shell script to run ping requests asynchronously and simultaneously to each website in question. Their outputs will be inside a folder called 'output', each in their own respective text file. To run, simply type "./pinger" and wait for the requests to complete. Execution permission should already be enabled.
