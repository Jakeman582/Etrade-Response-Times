"""This Python script provides examples on using the E*TRADE API endpoints"""
from __future__ import print_function
import webbrowser
import json
import configparser
import sys
import requests
from rauth import OAuth1Service
from datetime import datetime
import time
import signal
import csv

# loading configuration file
config = configparser.ConfigParser()
config.read('config.ini')

def oauth():
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
        name="etrade",
        consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

    base_url = config["DEFAULT"]["PROD_BASE_URL"]

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a text code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter text code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})

    collect_data(session, base_url)


def collect_data(session, base_url):

    def catch_sig_int(signum, frame):
        print("Ending data collection...\n")
        data_file.close()
        exception_file.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, catch_sig_int)

    url = base_url + "/v1/market/quote/GOOG.json"

    data_file = open("observations.txt", "w");
    exception_file = open("exceptions.txt", "w")

    data_writer = csv.writer(data_file, delimiter=",")
    exception_writer = csv.writer(exception_file, delimiter=",")

    print("Collecting data...")

    while True:

        current_time = datetime.now()

        try:
            response = session.get(url)
            data_writer.writerow([str(current_time), str(response.elapsed)])
            data_file.flush()
        except Exception as e:
            exception_writer.writerow([str(current_time), str(e)])
            exception_file.flush()

        time.sleep(1)

if __name__ == "__main__":
    oauth()
