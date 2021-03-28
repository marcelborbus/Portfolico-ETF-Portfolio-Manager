from data_manager import get_data_pool, json_to_user_preferences, preselect_by_volume, result_to_dict
from optimizer import weigh_data_to_match_preferences
import json

# TODO: split to different files; rename and document code; port to firebase; automatize database updates;

def process_request(request):
    json_req = json.loads(request)
    data_pool = get_data_pool()
    user_prefenrences = json_to_user_preferences(json_req, data_pool) # .get_json()) # for firebase
    preselection = preselect_by_volume(data_pool)

    result = weigh_data_to_match_preferences(preselection, user_prefenrences)
    response = result_to_dict(result)
    return json.dumps(response)