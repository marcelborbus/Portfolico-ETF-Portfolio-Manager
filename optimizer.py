from docplex.mp.model import Model
import numpy as np

# konvertiert Indizes zu Ticker
def indices_to_tickers(result, data_pool):
    symbols = data_pool.index.values
    return {symbols[i]: result[i] for i in result}

# DataFrame zu Vektor mit der Richtigen größe
def to_numpy(dataframe, is_matrix=False):
    vector = dataframe.sort_index(axis=1).to_numpy()

    if (not is_matrix):
        vector = vector.reshape(np.size(vector))

    return vector

# Zielfunktion
def objective_function(weights, input_matrix, target_vector):
    # return the distance sqared between the weighted sum of the vectors and the target vector
    scaled_matrix = input_matrix * weights[:, np.newaxis]
    sum_vector = sum(scaled_matrix)
    difference_vector = sum_vector - target_vector
    return difference_vector.dot(difference_vector) # sqare because sqrt is slow and unnecessary

# definiert das MIQP anhand aller ETFs und den Präferenzen jeweils als DataFrame und löst dieses
# data_pool und user_preferences müssen die selben Spalten besitzen
# DataFrame Layout: Ticker (egal bei user_preferences), Parameter1, ..., ParameterN
def weigh_data_to_match_preferences(data_pool, user_preferences, min_weight=.01):
    # DataFrames zu Vektoren
    input_matrix = to_numpy(data_pool, is_matrix=True)
    target_vector = to_numpy(user_preferences)

    # definiere das Model:
    # finde eine Gewichtung, sodass der Abstand der gewichteten ETFs zu den Präferenzen minimal ist
    # unter der Bedingung, dass die Gewichte null oder zwischen min_weight und eins liegen und zusammen eins ergeben
    model = Model()
    weights = np.array(model.semicontinuous_var_list(len(input_matrix), lb=min_weight, ub=1))
    model.minimize(objective_function(weights, input_matrix, target_vector))
    model.add_constraint(sum(weights) == 1)

    # löse das Modell
    result = model.solve()
    return {"result": indices_to_tickers(result.as_index_dict(), data_pool), "deviance": result.get_objective_value(), "status_code": model.solve_details.status_code}