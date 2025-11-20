import requests
import pandas as pd


def fetch_trials(page_size=1000, page_token=None):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "pageSize": page_size,
        # Can specify other parameters for query
    }

    if page_token:
        params["pageToken"] = page_token

    resp = requests.get(base_url, params=params)
    resp.raise_for_status()
    data = resp.json()

    return data


def get_all_interventional():
    print("Retrieving interventional trial data")
    all_records = []
    page_token = None
    count = 0

    for i in range(10):
        data = fetch_trials(page_size=1000, page_token=page_token)
        studies = data.get("studies", [])

        for s in studies:
            try:
                stype = s["protocolSection"]["designModule"]["studyType"]
            except KeyError:
                stype = None
            if stype == "INTERVENTIONAL":
                all_records.append(s)

        count += len(studies)
        print(
            f"Fetched {count} records in total, kept {len(all_records)} interventional studies..."
        )

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    df = pd.json_normalize(all_records)
    df.to_csv('output.csv')
    return df


get_all_interventional()
