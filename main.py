#Developed By MR.X
#github.com/isuruwa

import requests
requests.packages.urllib3.disable_warnings()
from os import system, name
import json, datetime
from bs4 import BeautifulSoup

#colors
class colors:
    whit = '\033[37m'
    end = '\033[0m' # end
    red = '\033[31m' # red
    green = '\033[1;32m' # green
    orange = '\033[33m' # orange
    blue = '\033[34m' # blue
    purple = '\033[35m' # purple
    white = "\x1b[97m" #end white
    redf = '\033[41m'#redf
    yellow = '\033[93m' #yellow

#clear Screen
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def get_interruption_times(start_date, end_date, acct_no):
    # Send an HTTP request to the website and retrieve the HTML content
    url = "https://cebcare.ceb.lk"
    response = requests.get(url, verify=False)
    html_content = response.text

    # search for the RequestVerificationToken
    soup = BeautifulSoup(html_content, 'html.parser')
    request_verification_token = soup.find(name='input', attrs={'name': '__RequestVerificationToken'})['value']

    # Retrieve the value of the .AspNetCore.Antiforgery.ThOcTlhnrMo cookie
    antiforgery_cookie = response.cookies['.AspNetCore.Antiforgery.ThOcTlhnrMo']

    # Create a session
    s = requests.session()
    s.verify = False

    # Make the GET request with Values
    r = s.get("https://cebcare.ceb.lk/Incognito/GetCalendarData",
              params={"from": start_date, "to": end_date, "acctNo": acct_no},
              headers={"RequestVerificationToken": request_verification_token},
              cookies={".AspNetCore.Antiforgery.ThOcTlhnrMo": antiforgery_cookie})

    # Parse the response as JSON
    data = r.json()

    # Extract the startTime and endTime values from the response
    interruptions = []
    for interruption in data['interruptions']:
        start_time = interruption['startTime']
        end_time = interruption['endTime']
        interruptions.append(f"startTime: {start_time}, endTime: {end_time}")

    return "\n".join(interruptions)



clear()
print(colors.red + r"""
   _     _  __      ____        ____        ____
  / \   / |/ /     /  __\      /   _\      / ___\
  | |   |   /_____ |  \/|_____ |  /  _____ |    \
  | |_/\|   \\____\|  __/\____\|  \__\____\\___ |
  \____/\_|\_\     \_/         \____/      \____/

   [+] Developed By MR.X - github.com/isuruwa [+]
""")
start_date = input("\n\033[37m [\033[35m+\033[37m]  Enter start date (YYYY-MM-DD): ")
start_date_parsed = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date = (start_date_parsed + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
acct_no = input("\n\033[37m [\033[35m+\033[37m] Enter account number: ")
interruptions = get_interruption_times(start_date, end_date, acct_no)
print("\n" + interruptions)


