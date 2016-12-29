import numpy as np 
import pandas as pd 
import random, sys

def Weight(mType):
    if mType == "horse":
        return max(0, np.random.normal(5,2,1)[0])
    if mType == "ball":
        return max(0, 1 + np.random.normal(1,0.3,1)[0])
    if mType == "bike":
        return max(0, np.random.normal(20,10,1)[0])
    if mType == "train":
        return max(0, np.random.normal(10,5,1)[0])
    if mType == "coal":
        return 47 * np.random.beta(0.5,0.5,1)[0]
    if mType == "book":
        return np.random.chisquare(2,1)[0]
    if mType == "doll":
        return np.random.gamma(5,1,1)[0]
    if mType == "blocks":
        return np.random.triangular(5,10,20,1)[0]
    if mType == "gloves":
        return 3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0]



d = pd.read_csv("gifts.csv")
d['type'] = d['GiftId'].apply(lambda x: x.split('_')[0])
d['id'] = d['GiftId'].apply(lambda x: x.split('_')[1])
d['weight'] = d['type'].apply(lambda x: Weight(x))

toy_map = {0:"horse", 1:"ball", 2:"bike", 3:"train", 4:"coal", 5:"book", 6:"doll", 7:"blocks", 8:"gloves"}

def individual():

    knapsack = [random.random() for i in range(0, 9)]
    max_toys = []
    while(sum(knapsack) < 3):
        knapsack = [random.randint(0,1) for i in knapsack]

    

def population(pop_count):

    return [individual() for i in range(0, pop_count)]

# def fitness(individual, target = 50):

#     sum_ind = sum([d.weight[i] for i in individual])

#     if sum_ind <= target:
#         return target - sum_ind
#     else:
#         return sys.maxint

# def pop_fitness(pop):

#     sum_pop = 0

#     for i in pop:
#         ind_sum = 0
#         for j in i:
#             ind_sum += d.weight[j]
#         if ind_sum <= 50:
#             sum_pop += ind_sum
#     return sum_pop