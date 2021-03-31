from data_manager_firestore import get_data_pool, json_to_user_preferences, preselect_by_volume #, update_result_with_estimate
from optimizer import weigh_data_to_match_preferences
import json

# TODO: automatize database updates;

# hierüber spricht man mit den Modulen
# managed Firebase requests in der zukunft
def process_request(request):
    request_json = request.get_json()

    country, industry, volumes = get_data_pool()
    data_pool = country.join(industry)

    user_prefenrences = json_to_user_preferences(request_json, data_pool.columns)

    preselection = preselect_by_volume(data_pool, volumes)

    result = weigh_data_to_match_preferences(preselection, user_prefenrences)
    """response = update_result_with_estimate(result)"""
    print(result)
    return json.dumps(result)
