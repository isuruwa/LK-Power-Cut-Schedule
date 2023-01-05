#Developed By MR.X
#github.com/isuruwa

import PySimpleGUI as sg
import requests
requests.packages.urllib3.disable_warnings()
import json, datetime
from bs4 import BeautifulSoup

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

# Create the GUI layout
layout = [
    [sg.Text("Start Date (YYYY-MM-DD):") , sg.Input(pad=(75, 0))],
    [sg.Text("Account Number:"), sg.Input(pad=(133, 0))],
    [sg.Button("Submit"), sg.Button("Cancel")],
    [sg.Multiline(size=(40, 10), key="output")]
]

# Create the window
sg.theme('LightBlue4')
window = sg.Window("LK Power Cut Schedule  - Developed By Mr.X", layout)

# Event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    elif event == "Submit":
        start_date = values[0]
        start_date_parsed = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = (start_date_parsed + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        acct_no = values[1]
        interruptions = get_interruption_times(start_date, end_date, acct_no)
        window["output"].update(interruptions)
