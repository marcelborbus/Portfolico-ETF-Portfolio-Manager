from docplex.mp.model import Model
import numpy as np

def objective_function(weights, input_matrix, target_vector):
    # return the distance sqared between the weighted sum of the vectors and the target vector
    scaled_matrix = input_matrix * weights[:, np.newaxis]
    sum_vector = sum(scaled_matrix)
    difference_vector = sum_vector - target_vector
    return difference_vector.dot(difference_vector) # sqare because sqrt is unnecessary

def solve_model_from_data(input_matrix, target_vector, min_weight=.01):
    # input_matrix is a matrix of vectors representing an ETF each, target vector representing user preferences
    # create a MIQP model from input data and weigh ETFs to match user preferences
    # each row of the vectors must represent the same parameter and they have to be in the according range ([0;1] by default)
    model = Model(name='etf_portfolio_convergence')
    weights = np.array(model.semicontinuous_var_list(len(input_matrix), lb=min_weight, ub=1))
    model.minimize(objective_function(weights, input_matrix, target_vector))
    model.add_constraint(sum(weights) == 1)
    return model.solve().as_index_dict(), np.sqrt(model.objective_value)   

input_matrix = np.array([
    [
        .3206, 0, 0, 0, 0, .1029, # countries
        .2349, 0, 0, .2219, 0 # sectors
    ], [
        0, 0, 0, 0, 1, 0, # countries
        .1723, .2704, .1042, .0323, .0234 # sectors
    ], [
        0, .1396, .1702, 0, 0, 0, # countries
        .0795, .1537, .1248, .1506, .0386 # sectors
    ], [
        0, 0, 0, 0, .0922, .3411, # countries
        .1974, .2123, .4077, .0359, .1124 # sectors
    ], [
        .5696, .0348, .0161, .22, 0, .0362, # countries
        .6884, 0, 0, .2136, .035 # sectors
    ], [
        0, 0, 0, 0, 0, .9967, # countries
        .1354, .2054, .1888, .1334, .0196 # sectors
    ], [
        .5767, .0199, .0121, .1095, 0, 0, # countries
        .1383, .1267, .0433, .1818, 0 # sectors
    ]
])

target_vector = np.array([
    .2, .05, .03, .06, .15, .2, # countries
    .3, .1, .15, .1, .15 # sectors
])

print(solve_model_from_data(input_matrix, target_vector))

# scale the rest parameters according to MSCI ALL WORLD 
# preprocessing: default target vector is MSCI ALL WORLD and scale up values if user wants to
# preselect a list of etfs
# data collection