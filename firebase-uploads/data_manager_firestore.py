import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd


# database access
def get_data_pool():
    if (not firebase_admin._apps):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {'projectId': 'genuine-airfoil-309308'})

    # access db and filter top 100 by volume
    db = firestore.client()
    docs = db.collection(u'ETFS').order_by(u'avgVolume', direction=firestore.Query.DESCENDING).limit(100).stream()

    industry, country = pd.DataFrame(), pd.DataFrame()

    for doc in docs:
        doc_dict = doc.to_dict()
        industry = industry.append(pd.DataFrame(doc_dict['industries'], index=[doc.id]).astype('float32'))
        country = country.append(pd.DataFrame(doc_dict['countries'], index=[doc.id]).astype('float32'))

    return industry, country

def json_to_user_preferences(user_req, data_pool_columns):
    # json to DataFrames
    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])
    user_preferences = user_industry.join(user_country)

    # apply columns of data_pool
    combined_exposures = pd.concat([user_preferences, pd.DataFrame(columns=data_pool_columns)]).fillna(0)
    return combined_exposures.sort_index(axis=1)