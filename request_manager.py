from data_manager import get_data_pool, json_to_user_preferences, preselect_by_volume, update_result_with_estimate
from optimizer import weigh_data_to_match_preferences
import json

# TODO: integrate Database; port to firebase; automatize database updates;

# hierüber spricht man mit den Modulen
# managed Firebase requests in der zukunft
def process_request(request):
    json_req = json.loads(request)
    data_pool = get_data_pool()

    user_prefenrences = json_to_user_preferences(json_req, data_pool.columns) # .get_json()) # for firebase
    preselection = preselect_by_volume(data_pool)

    result = weigh_data_to_match_preferences(preselection, user_prefenrences)
    """response = update_result_with_estimate(result)"""
    return json.dumps(result)