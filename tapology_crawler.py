from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utility import write_row, tapology_output


output_file = "output/Tapology.csv"

verify = True
csv_headers = ['Event', 'Name', 'Age', 'Weight Class', 'Last Weight-In', 'Height', 'Reach', 'Born',
               'Current Streak', 'UFC Competition', 'First Fight', 'Last Fight', 'Fight out of', 'Wins', 'Loss', 'Draws', 'No Contest']
write_row(tapology_output, csv_headers, 'w')


def data_from_api(fighter_id):
    api_url = "https://api.tapology.com/v1/internal_fighters/%s" % fighter_id
    print(api_url)

    api_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'content-type': 'application/vnd.api+json',
        # 'Referer': 'https://www.tapology.com/fightcenter/fighters/16950-renato-carneiro-moicano',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiaW50ZXJuYWxfYXBpIiwiZXhwIjoyNTM3NjU0NDAwfQ.C1E9hhkQOH7XrfZ5c7aTYS4CKN3ACkJ1nvgvx2v10YY'
    }

    r = requests.get(api_url, headers=api_headers, verify=verify)
    json_data = r.json()

    wins = json_data.get("data", {}).get("attributes", {}).get('pro_wins', 0) + json_data.get("data", {}).get(
        "attributes", {}).get('amateur_wins', 0)
    loss = json_data.get("data", {}).get("attributes", {}).get('pro_losses', 0) + json_data.get("data", {}).get(
        "attributes", {}).get('amateur_losses', 0)
    draws = json_data.get("data", {}).get("attributes", {}).get('pro_draws', 0) + json_data.get("data", {}).get(
        "attributes", {}).get('amateur_draws', 0)
    no_contests = json_data.get("data", {}).get("attributes", {}).get('pro_no_contests', 0) + json_data.get("data", {}).get(
        "attributes", {}).get('amateur_no_contests', 0)
    first_fight = json_data.get("included", [''])[-1].get('attributes', {}).get("event_date")

    ufc_competition = len([i.get('attributes', {}).get('promotion_acronym') for i in json_data.get("included", []) if
                       i.get('attributes', {}).get('status') != "cancelled" and i.get('attributes', {}).get(
                           'promotion_acronym') == "UFC"])

    return first_fight, ufc_competition, wins, loss, draws, no_contests


def run():
    base_url = "https://www.tapology.com/fightcenter?utf8=%E2%9C%93&group=ufc&schedule=upcoming&region=&commit=Submit"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    r = requests.get(base_url, headers=headers, verify=verify)
    soup = BeautifulSoup(r.text, "html5lib")
    event_links = [i['href'] for i in soup.select(".fcListing .left .name a[href]")]

    for event_link in event_links:
        r = requests.get(urljoin(base_url, event_link), headers=headers, verify=verify)
        soup = BeautifulSoup(r.text, "html5lib")

        event_title = soup.select_one('.eventPageHeaderTitles h1').text.strip()
        fighter_links = [i['href'] for i in soup.select(".fightCardFighterBout .fightCardFighterName a[href]")]

        print(event_title)
        for fighter_link in fighter_links:
            print(urljoin(base_url, fighter_link))

            r = requests.get(urljoin(base_url, fighter_link), headers=headers, verify=verify)
            soup = BeautifulSoup(r.text, 'html5lib')
            try:
                name = soup.select_one('strong:contains("Given Name") + span').text.strip()
            except AttributeError:
                name = soup.select_one('strong:contains("Name") + span').text.strip()

            age = soup.select_one('strong:contains("Age") + span').text.strip()
            weight_class = soup.select_one('strong:contains("Weight Class") + span').text.strip()
            last_weightIn = soup.select_one('strong:contains("Last Weigh-In:") + span').text.strip()
            height = soup.select_one('strong:contains("Height:") + span').text.strip()
            reach = soup.select_one('strong:contains("Reach:") + span').text.strip()
            born = soup.select_one('strong:contains("Born") + span').text.strip()
            current_streak = soup.select_one('strong:contains("Current Streak") + span').text.strip()
            last_fight = soup.select_one('strong:contains("Last Fight") + span').text.strip()
            fighting_out_of = soup.select_one('strong:contains("Fighting out of") + span').text.strip()

            fighter_id = soup.select_one('[name="fid"]').get('content')
            first_fight, ufc_competition, wins, loss, draws, no_contests = data_from_api(fighter_id)

            row = [event_title, name, age, weight_class, last_weightIn, height, reach, born, current_streak,
                   ufc_competition, first_fight, last_fight, fighting_out_of, wins, loss, draws, no_contests]

            write_row(tapology_output, row, 'a')
            print(row)

        print("\n")


if __name__ == "__main__":
    run()
    # data_from_api('12538')