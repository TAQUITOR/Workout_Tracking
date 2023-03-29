import requests
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]
PASSWORD = os.environ["PASSWORD"]

today = datetime.now()

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}
parameters_exercise_stats = {
    "query": input("Tell me which exercises you did: "),
    "gender": "male",
    "weight_kg": 74.4,
    "height_cm": 170,
    "age": 21
}

request_api_exercise = "https://trackapi.nutritionix.com/v2/natural/exercise"
response_exercise = requests.post(url=request_api_exercise, json=parameters_exercise_stats, headers=header)
response_exercise.raise_for_status()
data = response_exercise.json()

header = {"Authorization": PASSWORD}
json_body = {
    "workout": {
        "date": today.strftime("%d/%m/%Y"),
        "time": today.strftime("%H:%M:%S"),
        "exercise": data["exercises"][0]['user_input'].title(),
        "duration": data["exercises"][0]['duration_min'],
        "calories": round(data["exercises"][0]['nf_calories'])
    }
}
post_new_row = requests.post(url=SHEET_ENDPOINT, json=json_body, headers=header)
post_new_row.raise_for_status()
