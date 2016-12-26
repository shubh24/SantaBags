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

inds_available = [i for i in range(0, len(d))] 

def individual():

    len_ind = random.randint(3, 9) #Figure this out!
    # len_ind = 9

    ind = []

    for i in range(0, len_ind):

        ind_selected = inds_available[random.randint(0, len(inds_available)-1)]
        inds_available.remove(ind_selected)
        
        ind.append(ind_selected)

    return ind

def population(pop_count):

    return [individual() for i in range(0, pop_count)]

def fitness(individual, target = 50):

    sum_ind = sum([d.weight[i] for i in individual])
    if sum_ind <= target:
        return target - sum_ind
    else:
        return sys.maxint

def pop_fitness(pop):

    sum_pop = 0

    for i in pop:
        ind_sum = 0
        for j in i:
            ind_sum += d.weight[j]
        if ind_sum <= 50:
            sum_pop += ind_sum
    return sum_pop

def evolve(pop, target = 50, retain=0.8, random_select=0.05, mutate=0.01):

    sorted_pop = [x[1] for x in sorted([(fitness(i), i) for i in pop]) ]

    retain_length = int(len(sorted_pop)*retain)
    parents = sorted_pop[:retain_length]

    #Random Selection
    for i in sorted_pop[retain_length:]:

        if random_select > random.random():
            parents.append(i)
        else:
            for j in i:
                inds_available.append(j)

    #Mutate some individuals
    for ind_cou in range(0, len(parents)):
        
        ind = parents[ind_cou]
        ind_cou += 1

        if mutate > random.random():
            pos_to_mutate = random.randint(0, len(ind)-1)

            ind_selected = inds_available[random.randint(0, len(inds_available)-1)]
            inds_available.remove(ind_selected)
    
            ind[pos_to_mutate] = ind_selected

    desired_length = len(pop) - len(parents)
    children = []
    
    while len(children) < desired_length:
        # print len(parents), len(children)
        if len(parents) < 2:
            break

        male = random.randint(0, len(parents)-1)
        female = random.randint(0, len(parents)-1)
        
        if male != female:

            male_ind = parents[male]
            female_ind = parents[female]
            
            half_male = int(len(male_ind)/2)
            half_female = int(len(female_ind)/2)
            
            child1 = male_ind[:half_male] + female_ind[half_female:]
            child2 = male_ind[half_male:] + female_ind[:half_female]

            children.append(child1)
            children.append(child2)

            parents.remove(male_ind)
            parents.remove(female_ind)

    return children

pop = population(1000)
print pop_fitness(pop)

generation = 0
while (generation < 100):
    pop = evolve(pop)
    # inds_available = list(set(inds_available))
    print pop_fitness(pop), len(pop), len(inds_available)
    generation += 1

final = []

for i in pop:
    arr = []
    for j in i:
        arr.append(d.GiftId[j])

    final.append(arr)

pd.DataFrame({"Gifts": [" ".join(b) for b in final]}).to_csv("sub_genetic.csv", sep=",", index=False)

# f = open('sub_genetic.csv', 'wb')
# for i in final:
#     f.write()
# f.close()
