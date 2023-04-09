# Final Project
# Building Blocks

# Documentation: https://projects.propublica.org/api-docs/campaign-finance/
# or https://propublica.github.io/campaign-finance-api-docs/#candidates

import urllib.parse
import urllib.request
import urllib.error
import json

base_url = 'https://api.propublica.org/campaign-finance/{version}/{cycle}/{command}.json'
# Current Version: v1
version = 'v1'
API_KEY = {"X-API-Key": 'UEgkIJTEpk3difdnRL8TiB0g3Cz3FiqkGN9WCkZq'}


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def error_codes(code):
    codes = {
        400: 'Bad Request – Your request is improperly configured',
        401: 'Unauthorized – Your API key is wrong or missing',
        403: 'Forbidden – Your request is not allowed',
        404: 'Not Found – Your request worked, but did not find a response',
        405: 'Method Not Allowed – You tried to access a response with an invalid method',
        406: 'Not Acceptable – You requested a format that isn’t json or xml',
        429: 'Too Many Requests – You’ve made too many requests.',
        500: 'Internal Server Error – We had a problem with our server. Try again later, and let us know what you requested at apihelp@propublica.org.',
        502: 'Bad Gateway',
        503: 'Service Unavailable – We’re temporarily offline for maintenance or because of another issue. Please try again later.'
    }
    return (codes[code])


def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as error:
        print("The server couldn't fulfill the request.")
        print("Error code: ", error.code, ':', error_codes(error.code))
    except urllib.error.URLError as error:
        print("We failed to reach a server")
        print("Reason: ", error.reason)
    return None


##############################################
#### All API Request Functions Below Here ####
##############################################

# Function Format Template
# Name of function should match name in API documentation or very similar
# Define parameters for data to be sent in 'command'

# def get_candidates_from_state(state='WA', cycle='2022'):
#     # Define a command to be added to the url
#     command = "races/" + state
#     # url format below should not change between functions
#     url = base_url.format(version=version, cycle=cycle, command=command)
#     request = urllib.request.Request(url=url, headers=API_KEY)
#     # request.add_header("X-API-Key", KEY())
#     candiates_from_state = safe_get(request)
#     teststr = candiates_from_state.read().decode('utf-8')
#     if candiates_from_state is not None:
#         return json.load(teststr)

# print(pretty(get_candidates_from_state()))

###############################################
#### All Data Sorting Functions Below Here ####
###############################################


def create_dict_of_candidates(json_file):
    # Save candidates to a dictionary of individual candidates
    list_of_candidates = {}
    for candidate in json_file['results']:
        candidate_id = candidate['candidate']['id']
        list_of_candidates[candidate_id] = candidate['candidate']
    return (list_of_candidates)

# print(create_dict_of_candidates())


def get_candidates_from_state(state='WA', cycle='2022'):
    # Define a command to be added to the url
    command = "races/" + state
    # url format below should not change between functions
    url = base_url.format(version=version, cycle=cycle, command=command)
    request = urllib.request.Request(url=url, headers=API_KEY)
    candidates_from_state = safe_get(request)
    # print(candidates_from_state)
    # print(type(candidates_from_state))
    teststr = candidates_from_state.read().decode('utf-8')
    # print(pretty((teststr)))
    if candidates_from_state is not None and teststr is not None:
        # print(json.loads(teststr))
        return json.loads(teststr)
    else:
        return json.load('No candidates found')


# print(pretty(get_candidates_from_state(cycle=2018)))


def get_specific_candidate(id, cycle='2022'):
    # Define a command to be added to the url
    command = "candidates/" + id
    # file_type = 'json'
    # url format below should not change between functions
    url = base_url.format(version=version, cycle=cycle,
                          command=command)
    request = urllib.request.Request(url=url, headers=API_KEY)
    candidate = safe_get(request)
    # print(candidate)
    teststr = candidate.read().decode('utf-8')
    # print(teststr)
    if candidate is not None and teststr is not None:
        # print(json.loads(teststr))
        return json.loads(teststr)
    else:
        return json.load('No candidate found')


# get_specific_candidate('S0WA00258', cycle='2012')


stored_candidates = {}


def create_graph_data(state='WA', cycle='2022'):
    state_senator_data = {}
    # Bring the data in from API
    state_candidate_data = get_candidates_from_state(state=state, cycle=cycle)
    # Create a variable, 'highest_cost_campaign', to help remove candidates that are
    # below a set percentage of the highest 'campaign_cost'
    highest_cost_campaign = 0
    exclusion_percentage = 0.05
    for candidate in state_candidate_data['results']:
        candidate_id = candidate['candidate']['id']
        stored_candidates[candidate_id] = get_specific_candidate(
            candidate_id, cycle=cycle)
        if stored_candidates[candidate_id]['results'][0]['total_disbursements'] > highest_cost_campaign:
            highest_cost_campaign = stored_candidates[candidate_id]['results'][0]['total_disbursements']
        # print(pretty(stored_candidates))
    # Assign variables for the data desired in output
    for candidate in stored_candidates:
        candidate_id = candidate
        # This is throwing out any candidates not running for the senate.
        if candidate_id[0] == 'S':
            candidate_data = stored_candidates[candidate]
            # print(pretty(candidate_data))
            # Throwing out candidates that didn't spend anything or withdrew before the reporting cycle
            if candidate_data['results'][0]['total_disbursements'] != 0.0 and candidate_data['results'][0]['total_disbursements'] > highest_cost_campaign*exclusion_percentage:
                # Handling the error of 'null' names in display_name
                # Set to prefer 'display_name'
                if not candidate_data['results'][0]['display_name']:
                    candidate_name = candidate_data['results'][0]['name']
                else:
                    candidate_name = candidate_data['results'][0]['display_name']

                # Creating list for each candidate's data
                total_campaign_cost = candidate_data['results'][0]['total_disbursements']
                # state_senator_data[candidate_name] = {
                #     'fec_id': candidate_id,
                #     'campaign_cost': total_campaign_cost,
                #     'party': candidate_data['results'][0]['party'],
                #     'social': {
                #         'facebook': candidate_data['results'][0]['facebook_url'],
                #         'twitter_handle': candidate_data['results'][0]['twitter_user'],
                #         'campaign_website': candidate_data['results'][0]['url'],
                #     }
                # }

                state_senator_data[candidate_id] = [
                    cycle, candidate_name, candidate_data['results'][0]['party'], total_campaign_cost]

                # party = candidate_data['results'][0]['party']
                # new_candidate_list = [candidate_name, party, total_campaign_cost]

                # state_senator_data[cycle] = [
                #     [candidate_name, party, total_campaign_cost]
                # ]
                # ## Max # of candidates = 2
                # if len(state_senator_data) == 2:
                #     if state_senator_data[cycle][0][total_campaign_cost] <
    return (state_senator_data)


print((create_graph_data(cycle='2022')))
# print((create_graph_data(cycle='2020')))
# print((create_graph_data(cycle='2018')))
# print((create_graph_data(cycle='2016')))
# print((create_graph_data(cycle='2014')))

# def test(lst):
#     result = {}
#     for year in lst:
#         result[year] = create_graph_data(cycle=year)
#     return result