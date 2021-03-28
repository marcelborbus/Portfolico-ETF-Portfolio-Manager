from docplex.mp.model import Model
import numpy as np

def result_to_symbols(result, data_pool):
    symbols = data_pool.index.values
    return {symbols[i]: result[i] for i in result}

def as_preference_vector(dataframe):
    vector = dataframe.sort_index(axis=1).to_numpy()
    return vector.reshape(np.size(vector))

def objective_function(weights, input_matrix, target_vector):
    # return the distance sqared between the weighted sum of the vectors and the target vector
    scaled_matrix = input_matrix * weights[:, np.newaxis]
    sum_vector = sum(scaled_matrix)
    difference_vector = sum_vector - target_vector
    return difference_vector.dot(difference_vector) # sqare because sqrt is unnecessary

def weigh_data_to_match_preferences(data_pool, user_preferences, min_weight=.01):
    # input_matrix is a matrix of vectors representing an ETF each, target vector representing user preferences
    # create a MIQP model from input data and weigh ETFs to match user preferences
    # each row of the vectors must represent the same parameter and they have to be in the according range ([0;1] by default)
    input_matrix = data_pool.to_numpy()
    target_vector = as_preference_vector(user_preferences)

    # define model
    model = Model()
    weights = np.array(model.semicontinuous_var_list(len(input_matrix), lb=min_weight, ub=1))
    model.minimize(objective_function(weights, input_matrix, target_vector))
    model.add_constraint(sum(weights) == 1)

    # solve and return results
    result = model.solve()
    return {"result": result_to_symbols(result.as_index_dict(), data_pool), "error": result.get_objective_value()}