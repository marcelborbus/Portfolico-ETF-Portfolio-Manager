import pandas as pd

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

# database access
def get_data_pool():
    industry_exposure = pd.read_csv('industry_exposure.csv', index_col=0).astype('float32') # change for firebase
    country_exposure = pd.read_csv('country_exposure.csv', index_col=0).astype('float32')
    return industry_exposure.join(country_exposure)

def json_to_user_preferences(user_req, data_pool_columns=get_data_pool().columns):
    # json to DataFrames
    user_industry = pd.DataFrame(user_req['industries'], index=[0])
    user_country = pd.DataFrame(user_req['countries'], index=[0])
    user_preferences = user_industry.join(user_country)

    # apply columns of data_pool
    combined_exposures = pd.concat([user_preferences, pd.DataFrame(columns=data_pool_columns)]).fillna(0)
    return combined_exposures.sort_index(axis=1)

# return top 100 ETFs by avgVolume
def preselect_by_volume(data_pool):
    volumes = pd.read_csv('volumes.csv', index_col=0)
    filtered_symbols = volumes.sort_values('avgVolume', ascending=False)[:100].index.values # 100 for performance
    return data_pool.loc[data_pool.index.intersection(filtered_symbols),:]