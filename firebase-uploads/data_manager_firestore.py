import pandas as pd

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# database access
def get_data_pool():
    if (not firebase_admin._apps):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': 'genuine-airfoil-309308',
        })

    db = firestore.client()
    users_ref = db.collection(u'ETFS')
    docs = users_ref.stream()

    industry, country, volume = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for doc in docs:
        doc_dict = doc.to_dict()
        industry = industry.append(pd.DataFrame(doc_dict['industries'], index=[doc.id]).astype('float32'))
        country = country.append(pd.DataFrame(doc_dict['countries'], index=[doc.id]).astype('float32'))
        volume = volume.append(pd.DataFrame([doc_dict['avgVolume']], index=[doc.id], columns=['avgVolume']).astype('float32'))

    return industry, country, volume

def json_to_user_preferences(user_req, data_pool_columns):
    # json to DataFrames
    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])
    user_preferences = user_industry.join(user_country)

    # apply columns of data_pool
    combined_exposures = pd.concat([user_preferences, pd.DataFrame(columns=data_pool_columns)]).fillna(0)
    return combined_exposures.sort_index(axis=1)

# return top 100 ETFs by avgVolume
def preselect_by_volume(data_pool, volumes):
    filtered_symbols = volumes.sort_values('avgVolume', ascending=False)[:100].index.values # 100 for performance
    return data_pool.loc[data_pool.index.intersection(filtered_symbols),:]