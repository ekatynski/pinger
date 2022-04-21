# pinger

An attempt to automate a data-collection function for a networking class. The homework assignment wasn't mine, but I like the idea of making a project complete itself.

Before running, be sure to install the necessary dependencies :

```

pip install -r requirements.txt

```

I would recommend doing this in a virtual environment, but I trust your judgement.

To use, run setup.py in python3. You will be prompted for the number of websites and the respective URLs you wish to ping. Please skip the "www." in your URLs but feel free to include any extensions after your TLD. Note: multiple pings to the same site may result in errors, the output files are named using prior to the TLD and this may cause name overwrites.

After this, you will be prompted for the paramaters of the full test you wish to run. Enter the delay between ping exercises and the number of exercises you wish to run.

After running setup.py, you will have a shell script to run ping requests asynchronously and simultaneously to each website in question. You will also have a script to govern the aforementioned ping request script. Their outputs will be inside a folder called 'output', each in their own respective text file. To run, simply type "./manager.sh" and wait for the requests to complete. Execution permission should already be enabled for both files.

After the ping requests complete, calculate.py will plot all of the data in question as well as print descriptive statistics for all of the ping requests to the console.
