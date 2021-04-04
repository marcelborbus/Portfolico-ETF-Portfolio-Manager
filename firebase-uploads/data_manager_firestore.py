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
    db = firestore.client().collection(u'ETFS').order_by(u'avgVolume', direction=firestore.Query.DESCENDING).limit(100).stream()
    
    industry, country = [], []

    # performance killer
    for doc in db:
        doc_dict = doc.to_dict()
        doc_dict['industries'].update({'ticker': doc.id})
        industry.append(doc_dict['industries'])
        doc_dict['countries'].update({'ticker': doc.id})
        country.append(doc_dict['countries'])

    industry_df = pd.DataFrame.from_dict(industry, dtype='float32').set_index('ticker')
    country_df = pd.DataFrame.from_dict(country, dtype='float32').set_index('ticker')

    return industry_df, country_df

def json_to_user_preferences(user_req, data_pool_columns):
    # json to DataFrames
    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])
    user_preferences = user_industry.join(user_country)

    # apply columns of data_pool
    combined_exposures = pd.concat([user_preferences, pd.DataFrame(columns=data_pool_columns)]).fillna(0)
    return combined_exposures.sort_index(axis=1)


# Fügt die Anteile der Schätzung dem Ergebnis hinzu, um dem Nutzer die Abweichung zu veranschaulichen
def add_guessed_exp(result, countries, industries):
    guess = result["result"]

    etf_list_industry = pd.DataFrame()
    etf_list_country = pd.DataFrame()

    for etf in guess:
        etf_list_industry = etf_list_industry.append(pd.DataFrame(industries.loc[etf] * guess[etf]).T)
        etf_list_country = etf_list_country.append(pd.DataFrame(countries.loc[etf] * guess[etf]).T)

    guesses_exp = {"industry": etf_list_industry.sum().to_dict(), "country": etf_list_country.sum().to_dict()}
    result.update({"estimate": guesses_exp})
