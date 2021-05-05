import requests
from cachetools import TTLCache, cached

from server import config


@cached(TTLCache(maxsize=10, ttl=900))
def state_options():
    response = requests.get(
        "https://cdn-api.co-vin.in/api/v2/admin/location/states",
        headers={"User-Agent": config.USER_AGENT},
    ).json()
    options = [
        {
            "text": {"type": "plain_text", "text": state["state_name"]},
            "value": str(state["state_id"]),
        }
        for state in response.get("states")
    ]

    return options


@cached(TTLCache(maxsize=20, ttl=900))
def district_options(state_id):
    response = requests.get(
        f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}",
        headers={"User-Agent": config.USER_AGENT},
    ).json()
    options = [
        {
            "text": {"type": "plain_text", "text": district["district_name"]},
            "value": str(district["district_id"]),
        }
        for district in response.get("districts")
    ]

    return options
