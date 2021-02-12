import numpy as np
from scipy.optimize import minimize

def get_magnitude(vector):
    return np.sqrt(vector.dot(vector))

def get_distance(vector1, vector2, scale_vector):
    diff = vector1 - vector2
    scaled_diff = scale_vector * diff
    return get_magnitude(vector1 - vector2)

def sum_vectors(vectors):
    return sum(vectors)

def scale_vectors(scalars, vectors): 
    return [s * v for s, v in zip(scalars, vectors)]

def objective_function(scalars, input_vectors, target_vector, scale_vector):
    scaled_vectors = scale_vectors(scalars, input_vectors)
    summed_vector = sum_vectors(scaled_vectors)
    return get_distance(summed_vector, target_vector, scale_vector)

def constraint(scalars):
    return sum(scalars) - 1

def main():
    scalar_bounds = (0, 1)
    bounds_list = tuple([scalar_bounds for i in input_vectors])

    initial_guess = [0 for i in input_vectors]
    initial_guess[1] = 1 # TODO: better initial guess, maybe by similarity

    constraint_obj = {'type': 'eq', 'fun': constraint}

    result = minimize(objective_function, x0=initial_guess, args=(input_vectors, target_vector, scale_vector), bounds=bounds_list, constraints=[constraint_obj])
    print('\nabweichung:', result.fun, '\ngewischtung:', result.x, '\n')
    
input_vectors = [
    np.array([
        .3206, 0, 0, 0, 0, .1029, # countries
        .2349, 0, 0, .2219, 0 # sectors
    ], dtype='float32'), 
    np.array([
        0, 0, 0, 0, 1, 0, # countries
        .1723, .2704, .1042, .0323, .0234 # sectors
    ], dtype='float32'), 
    np.array([
        0, .1396, .1702, 0, 0, 0, # countries
        .0795, .1537, .1248, .1506, .0386 # sectors
    ], dtype='float32'), 
    np.array([
        0, 0, 0, 0, .0922, .3411, # countries
        .1974, .2123, .4077, .0359, .1124 # sectors
    ], dtype='float32'),
    np.array([
        .5696, .0348, .0161, .22, 0, .0362, # countries
        .6884, 0, 0, .2136, .035 # sectors
    ], dtype='float32'), 
    np.array([
        0, 0, 0, 0, 0, .9967, # countries
        .1354, .2054, .1888, .1334, .0196 # sectors
    ], dtype='float32'), 
    np.array([
        .5767, .0199, .0121, .1095, 0, 0, # countries
        .1383, .1267, .0433, .1818, 0 # sectors
    ], dtype='float32'),
]

target_vector = np.array([
    .2, .05, .03, .06, .15, .2, # countries
    .3, .1, .15, .1, .15 # sectors
])

scale_vector = np.ones(11)

main()
