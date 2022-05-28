# FTX_TWAP
A python script to TWAP on your favorite shitcoins


## How to use

### Install requests library (allowing to execute http request to FTX)

Make sure to have python3 installed on your computer.

Using powershell or a linux terminal, go to your working directory (FTX_TWAP) : 

> pip3 install -r requirements.txt

### Modify ftx_twap/twap.py
Modify the code of twap.py with the credentials of your FTX account (API_KEY, API_SECRET, SUBACCOUNT_NAME) and the markets you want to TWAP.

### Create a scheduled task

#### If using windows : 
Follow the following tutorial to schedule a task on executing the script ftx_twap/twap.py (https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/Scheduled_tasks_and_cron_jobs_on_Windows/index.html).

First you create a simple task that start at 0:00, every day. 
The key here is to find the advanced properties.
Double click the task and a property window will show up.
Click the Triggers tab.
Double click the trigger details and the Edit Trigger window will show up.
Under Advanced settings panel, tick Repeat task every 5 minutes, and set Indefinitely if you need.
Finally, click ok.

Your computer will TWAP the markets you mentionned in twap.py every 5 minutes.

#### If using linux  :

Use crontask by executing 'crontab -e' in your terminal
add the following line in the crontab
> */5 * * * * /usr/bin/python3 /[path_to_your_ftx_twap/twap.py_script]

Your computer will TWAP the markets you mentionned in twap.py every 5 minutes.+



If you encounter a problem, DM 0xTechnician on Twitter

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/0xTechnician.svg?style=social&label=Follow%200xTechnician)](https://twitter.com/0xTechnician)

