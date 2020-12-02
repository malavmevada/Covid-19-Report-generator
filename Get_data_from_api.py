import pandas as pd
import requests
import csv
import json

URL = 'https://api.covid19india.org/states_daily.json'

def get_covid_data():
    c_data = requests.get(URL)
    c_data = c_data.json()
    data = c_data['states_daily']
    data_file = open('./data/main_covid.csv', 'w')
    csv_w = csv.writer(data_file)
    count = 0

    for i in data:
        if count == 0:
            header = i.keys()
            csv_w.writerow(header)
            count += 1
        csv_w.writerow(i.values())
    data_file.close()

    abbriviations = {
        "AN": "Andaman & Nicobar Island",
        "AP": "Andhra Pradesh",
        "AR": "Arunanchal Pradesh",
        "AS": "Assam",
        "BR": "Bihar",
        "CH": "Chandigarh",
        "CT": "Chhattisgarh",
        "DN": "Dadara & Nagar Havelli",
        "DD": "Daman & Diu",
        "DL": "NCT of Delhi",
        "GA": "Goa",
        "GJ": "Gujarat",
        "HR": "Haryana",
        "HP": "Himachal Pradesh",
        "JK": "Jammu & Kashmir",
        "JH": "Jharkhand",
        "KA": "Karnataka",
        "KL": "Kerala",
        "LD": "Lakshadweep",
        "MP": "Madhya Pradesh",
        "MH": "Maharashtra",
        "MN": "Manipur",
        "ML": "Meghalaya",
        "MZ": "Mizoram",
        "NL": "Nagaland",
        "OR": "Odisha",
        "PY": "Puducherry",
        "PB": "Punjab",
        "RJ": "Rajasthan",
        "SK": "Sikkim",
        "TN": "Tamil Nadu",
        "TG": "Telangana",
        "TR": "Tripura",
        "UP": "Uttar Pradesh",
        "UT": "Uttarakhand",
        "WB": "West Bengal",
        "TT": "Total",

    }

    abbriviations = {k.lower(): v for k, v in abbriviations.items()}

    covid_df = pd.read_csv('./data/main_covid.csv')
    colums_name = ['date', 'dateymd', 'status', 'tt', 'an', 'ap', 'ar', 'as', 'br', 'ch', 'ct', 'dd', 'dl', 'dn', 'ga', 'gj', 'hp', 'hr', 'jh',
                'jk', 'ka', 'kl', 'ld', 'mh', 'ml', 'mn', 'mp', 'mz', 'nl', 'or', 'pb', 'py', 'rj', 'sk', 'tg', 'tn', 'tr', 'up', 'ut', 'wb']
    covid_df = covid_df[colums_name]
    covid_df = covid_df.rename(columns=abbriviations)

    confirmed = covid_df[(covid_df['status'] == 'Confirmed')
                        ].reset_index(drop=True)
    recovered = covid_df[(covid_df['status'] == 'Recovered')
                        ].reset_index(drop=True)
    deceased = covid_df[(covid_df['status'] == 'Deceased')].reset_index(drop=True)

    confirmed.to_csv('./data/confirmed.csv', index=False)
    recovered.to_csv('./data/recovered.csv', index=False)
    deceased.to_csv('./data/deceased.csv', index=False)


    india_states = json.load(open("./data/states_india.geojson"))
    india_states['features'][0].keys()
    state_id_map = {}
    for feature in india_states['features']:
        feature['id'] = feature['properties']['state_code']
        state_id_map[feature['properties']['st_nm']] = feature['id']

    df = confirmed.copy()
    confirmed = confirmed.T
    confirmed = confirmed.rename(columns=df["dateymd"])
    confirmed = confirmed.drop(["date", "dateymd", "status", "Total"], axis=0)
    confirmed = confirmed.reset_index()
    confirmed = confirmed.rename(columns={"index": "states"})
    confirmed['id'] = confirmed["states"].apply(lambda x: state_id_map[x])

    confirmed.to_csv('./data/confirmed_t.csv', index=False)

    df = deceased.copy()
    deceased = deceased.T
    deceased = deceased.rename(columns=df["dateymd"])
    deceased = deceased.drop(["date", "dateymd", "status", "Total"], axis=0)
    deceased = deceased.reset_index()
    deceased = deceased.rename(columns={"index": "states"})
    deceased['id'] = deceased["states"].apply(lambda x: state_id_map[x])

    deceased.to_csv('./data/deceased_t.csv', index=False)

    df = recovered.copy()
    recovered = recovered.T
    recovered = recovered.rename(columns=df["dateymd"])
    recovered = recovered.drop(["date", "dateymd", "status", "Total"], axis=0)
    recovered = recovered.reset_index()
    recovered = recovered.rename(columns={"index": "states"})

    recovered['id'] = recovered["states"].apply(lambda x: state_id_map[x])
    recovered.to_csv('./data/recovered_t.csv', index=False)
