import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""
# Fügt die Anteile der Schätzung dem Ergebnis hinzu, um dem Nutzer die Abweichung zu veranschaulichen
def update_result_with_estimate(result):
    result.update({"estimate": estimate_to_exposures(result["result"])})
    return result


def estimate_to_exposures(dictionary):
    industry = pd.read_csv('industry_exposure.csv', index_col=0).astype('float32') # change for firebase
    country = pd.read_csv('country_exposure.csv', index_col=0).astype('float32')

    etf_list_industry = pd.DataFrame()
    etf_list_country = pd.DataFrame()

    for etf in dictionary:
        etf_list_industry = etf_list_industry.append(pd.DataFrame(industry.loc[etf] * dictionary[etf]).T)
        etf_list_country = etf_list_country.append(pd.DataFrame(country.loc[etf] * dictionary[etf]).T)

    return {"industry": etf_list_industry.sum().to_dict(), "country": etf_list_country.sum().to_dict()}
"""

# database access
def get_data_pool():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'genuine-airfoil-309308',
    })

    db = firestore.client()

    users_ref = db.collection(u'ETFS')
    docs = users_ref.stream()

    data_pool = pd.DataFrame()
    for doc in docs:
        doc_dict = doc.to_dict()
        cty = pd.DataFrame(doc_dict['countries'], index=[doc.id]).astype('float32')
        idy = pd.DataFrame(doc_dict['industries'], index=[doc.id]).astype('float32')
        data_pool = data_pool.append(cty.join(idy))

    return data_pool

def json_to_user_preferences(user_req, data_pool_columns=get_data_pool().columns):
    # json to DataFrames
    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])
    user_preferences = user_industry.join(user_country)

    # apply columns of data_pool
    combined_exposures = pd.concat([user_preferences, pd.DataFrame(columns=data_pool_columns)]).fillna(0)
    return combined_exposures.sort_index(axis=1)

def get_volumes():
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'genuine-airfoil-309308',
    })

    db = firestore.client()

    users_ref = db.collection(u'ETFS')
    docs = users_ref.stream()

    data_pool = pd.DataFrame()
    for doc in docs:
        doc_dict = doc.to_dict()
        vol = pd.DataFrame(doc_dict['avgVolume'], index=[doc.id]).astype('float32')
        data_pool = data_pool.append(vol)

    return data_pool


# return top 100 ETFs by avgVolume
def preselect_by_volume(data_pool):
    volumes = get_volumes()
    filtered_symbols = volumes.sort_values('avgVolume', ascending=False)[:100].index.values # 100 for performance
    return data_pool.loc[data_pool.index.intersection(filtered_symbols),:]