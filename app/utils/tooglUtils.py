#! /usr/bin/env python
# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests
import config
from base64 import b64encode

# default API user agent value
user_agent = "TogglPy"

# -------------------------------------------------------------
# Methods that modify the headers to control our HTTP requests
# -------------------------------------------------------------


def setAPIKey():
    '''set the API key in the request header'''
    # craft the Authorization
    authHeader = config.TOOGL_API_TOKEN + ":" + "api_token"
    return "Basic " + b64encode(authHeader.encode()).decode('ascii').rstrip()


# template of headers for our request
headers = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "python/urllib",
    'Authorization': setAPIKey()
}
REPORT_DETAILED = "https://api.track.toggl.com/api/v2/details"


def get_detail_report(since, until,):

    data = []
    page = []
    page_num = 1
    while len(page) > 0 or page_num == 1:
        page.clear()
        parameters = {'workspace_id': getWorkspace(
        ), 'since': since, 'until': until, 'user_agent': 'api_test', 'page': page_num}
        endpoint = Endpoints.REPORT_DETAILED + "?" + urlencode(parameters)
        resp = make_request(endpoint)
        if resp is None:
            raise BaseException('empty response received from toogl')

        if 'error' in resp:
            raise BaseException(
                f'{resp["error"]["message"]}. {resp["error"]["tip"]}')

        page = resp['data']
        data.extend(page)
        page_num += 1

    return data


def make_request(endpoint):
    response = requests.get(url=endpoint, headers=headers)
    return response.json()


def getWorkspace():
    resp = make_request(Endpoints.WORKSPACES)
    return resp[0]['id']


class Endpoints():
    WORKSPACES = "https://api.track.toggl.com/api/v9/workspaces"
    CLIENTS = "https://api.track.toggl.com/api/v9/clients"
    PROJECTS = "https://api.track.toggl.com/api/v9/projects"
    TASKS = "https://api.track.toggl.com/api/v9/tasks"
    REPORT_WEEKLY = "https://api.track.toggl.com/api/v2/weekly"
    REPORT_DETAILED = "https://api.track.toggl.com/reports/api/v2/details"
    REPORT_SUMMARY = "https://api.track.toggl.com/api/v2/summary"
    START_TIME = "https://api.track.toggl.com/api/v9/time_entries/start"
    TIME_ENTRIES = "https://api.track.toggl.com/api/v9/time_entries"

    @staticmethod
    def STOP_TIME(pid):
        return "https://api.track.toggl.com/api/v9/time_entries/" + str(pid) + "/stop"
    CURRENT_RUNNING_TIME = "https://api.track.toggl.com/api/v9/time_entries/current"


if __name__ == '__main__':
    get_detail_report('2018-06-18', '2018-07-05')
