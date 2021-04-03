from data_manager_firestore import get_data_pool, json_to_user_preferences
from optimizer import weigh_data_to_match_preferences
import json

# TODO: automatize database updates; return guessed exposures

def process_request(request):
    country, industry = get_data_pool()
    data_pool = country.join(industry)
    user_prefenrences = json_to_user_preferences(request.get_json(), data_pool.columns)
    result = weigh_data_to_match_preferences(data_pool, user_prefenrences)
    return json.dumps(result)