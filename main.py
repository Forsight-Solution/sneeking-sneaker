#%%
import pandas as pd
import dotenv
import requests
from fastapi import FastAPI
import os
import json

dotenv.load_dotenv()

def apify_call(payload):
    scaper_url = f"https://api.apify.com/v2/actor-tasks/observant_ginkgo~api/run-sync-get-dataset-items?token={os.getenv( 'APIFY-TOKEN')}"

    headers = {
        'Content-Type': 'application/json',
    }

    result = requests.get(scaper_url, headers=headers, data=payload)

    data = result.json()
    print(data)

    df = pd.DataFrame.from_dict(data)

    df.sort_values(by=['likesCount'], inplace=True, ascending=False)

    final_data = []
    for index, row in df.iterrows():
        final_data.append({"displayUrl":row['displayUrl'], "likesCount":row['likesCount']})


    return final_data

app = FastAPI()

@app.post("/")
async def root(payload: dict):
    return {apify_call(json.dumps(payload))}
