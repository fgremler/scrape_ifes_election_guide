import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data_with_headers = []

# ids do not necessarily go continously (s. here: view-source:https://www.electionguide.org/countries/)
# but up to 266 - one could scrape all the /countries/id links on the site
# to ensure that this script runs on future iterations of the site
# here I just manually check whether it's a country site and then scrape it
# at the end we should have 240 country profiles

for country_id in range(2,267):

    url = f"https://www.electionguide.org/countries/id/{country_id}"

    result = requests.get(url)

    soup = BeautifulSoup(result.content, "html.parser")

    if soup("title")[0].text != "IFES Election Guide | Country Profiles":
        country = soup.find("div", {"class": "path col-md-12"})
        country = country.find_all("li")[2].text.strip()

        print(f"Scraping {country}.")

        all_tabs = soup.find_all("table")

        all_trs = all_tabs[2].find_all("tr")


        table_data = [[cell.text for cell in row("td")] for row in all_trs]

        for row in table_data:
            if len(row) > 0:
                row_dict = dict()
                row_dict["election_for"] = row[0]
                row_dict["date"] = row[1].strip()
                row_dict["votes"] = row[2]
                row_dict["registered_voters"] = row[3]
                row_dict["turn_out"] = row[4]
                row_dict["country"] = country
                data_with_headers.append(row_dict)

        time.sleep(1)

pd.DataFrame(data_with_headers).to_csv("ifes_data.csv", index=False)
