import pandas as pd

def result_to_dict(result):
    result.update({"estimate": get_exposures_from_dict(result["result"])})
    return result

def get_exposures_from_dict(dictionary):
    industry = pd.read_csv('industry_exposure.csv', index_col=0).astype('float32') # change for firebase
    country = pd.read_csv('country_exposure.csv', index_col=0).astype('float32')

    etf_list_industry = pd.DataFrame()
    etf_list_country = pd.DataFrame()

    for etf in dictionary:
        etf_list_industry = etf_list_industry.append(pd.DataFrame(industry.loc[etf] * dictionary[etf]).T)
        etf_list_country = etf_list_country.append(pd.DataFrame(country.loc[etf] * dictionary[etf]).T)

    return {"industry": etf_list_industry.sum().to_dict(), "country": etf_list_country.sum().to_dict()}

def get_data_pool():
    industry_exposure = pd.read_csv('industry_exposure.csv', index_col=0).astype('float32') # change for firebase
    country_exposure = pd.read_csv('country_exposure.csv', index_col=0).astype('float32')
    return industry_exposure.join(country_exposure)

def json_to_user_preferences(user_req, data_pool=get_data_pool()):
    base_exposure = data_pool.loc['AAXJ'].to_frame().T.reset_index(drop=True) # change to IE00B3RBWM25

    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])

    user_preferences = user_industry.join(user_country)
    combined_exposures = pd.concat([user_preferences, base_exposure])

    final_exposures = combined_exposures.groupby(combined_exposures.index).first().sort_index(axis=1)
    return final_exposures

def preselect_by_volume(data_pool):
    volumes = pd.read_csv('volumes.csv', index_col=0)
    filtered_symbols = volumes.sort_values('avgVolume', ascending=False)[:100].index.values
    return data_pool.loc[data_pool.index.intersection(filtered_symbols),:]