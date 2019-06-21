from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from utility import write_row, clean_str, ufcstats_output


output_file = "output/utcstats.csv"
base_url = "http://ufcstats.com/statistics/events/upcoming"
verify = True
csv_headers = ['Event', 'Event Date', 'Event Location', 'Weight Class', 'Name', 'Height', 'Weight', 'Reach', 'STANCE',
               'DOB', 'SLpM', 'Str. Acc.', 'SApM', 'Str. Def.', 'TD Avg', 'TD Acc', 'TD Def', 'Sub. Avg.', 'Win s', 'Los s']
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}
write_row(ufcstats_output, csv_headers, 'w')


def run():
    r = requests.get(base_url, headers=headers, verify=verify)
    soup = BeautifulSoup(r.text, "html5lib")
    event_links = [(i['href'],  clean_str(i.text)) for i in soup.select(".b-statistics__table-content a[href]")]
    event_dates = [clean_str(i.text) for i in soup.select(".b-statistics__date")]
    event_locations = [clean_str(i.text) for i in soup.select(".b-statistics__table-col_style_big-top-padding")]

    for index, value in enumerate(event_links):
        event_title = value[1]
        event_date = event_dates[index]
        event_location = event_locations[index]

        r = requests.get(urljoin(base_url, value[0]), headers=headers, verify=verify)
        soup = BeautifulSoup(r.text, "html5lib")

        tr_tags = soup.select('tbody.b-fight-details__table-body tr')
        fighter_links = []
        for tr in tr_tags:
            links = [a['href'] for a in tr.select("td:nth-child(2) a[href]")]
            weight_class = clean_str(tr.select_one("td:nth-child(7)").text)
            fighter_links.extend([(link, weight_class) for link in links])

        for fighter_link, weight_class in fighter_links:
            print(urljoin(base_url, fighter_link))
            r = requests.get(urljoin(base_url, fighter_link), headers=headers, verify=verify)
            soup = BeautifulSoup(r.text, 'html5lib')
            name = clean_str(soup.select_one('.b-content__title-highlight').text)
            height = clean_str(soup.select_one('i:contains("Height:")').next_sibling)
            weight = clean_str(soup.select_one('i:contains("Weight:")').next_sibling)
            reach = clean_str(soup.select_one('i:contains("Reach:")').next_sibling)
            stance = clean_str(soup.select_one('i:contains("STANCE:")').next_sibling)
            dob = clean_str(soup.select_one('i:contains("DOB:")').next_sibling)
            slpm = clean_str(soup.select_one('i:contains("SLpM:")').next_sibling)
            str_acc = clean_str(soup.select_one('i:contains("Str. Acc.:")').next_sibling)
            sapm = clean_str(soup.select_one('i:contains("SApM:")').next_sibling)
            str_def = clean_str(soup.select_one('i:contains("Str. Def:")').next_sibling)
            td_avg = clean_str(soup.select_one('i:contains("TD Avg.:")').next_sibling)
            td_acc = clean_str(soup.select_one('i:contains("TD Acc.:")').next_sibling)
            td_def = clean_str(soup.select_one('i:contains("TD Def.:")').next_sibling)
            sub_avg = clean_str(soup.select_one('i:contains("Sub. Avg.:")').next_sibling)

            record = clean_str(soup.select_one('.b-content__title-record').text).split(':')[-1].strip()
            win_s = record.split("-")[0]
            los_s = record.split("-")[1]

            row = [event_title, event_date, event_location, weight_class, name, height, weight, reach, stance, dob,
                   slpm, str_acc, sapm, str_def, td_avg, td_acc, td_def, sub_avg, win_s, los_s]

            write_row(ufcstats_output, row, 'a')
            print(row)

        print("\n")


if __name__ == "__main__":
    run()
