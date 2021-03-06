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
    for ind in parents:

        if mutate > random.random():
            pos_to_mutate = random.randint(0, len(ind)-1)

            ind_selected = inds_available[random.randint(0, len(inds_available)-1)]

            inds_available.remove(ind_selected)            
            inds_available.append(ind[pos_to_mutate])    

            ind[pos_to_mutate] = ind_selected

    children = parents
    # while len(parents) > 1:

    #     male = random.randint(0, len(parents)-1)
    #     female = random.randint(0, len(parents)-1)
    
    #     if male != female:
    #         male_ind = parents[male]
    #         female_ind = parents[female]

    #         half_male = int(len(male_ind)/2)
    #         half_female = int(len(female_ind)/2)
            
    #         children.append(male_ind[:half_male] + female_ind[half_female:])
    #         children.append(male_ind[half_male:] + female_ind[:half_female])
    #         parents.remove(male_ind)
    #         parents.remove(female_ind)
    
    while len(children) < 1000:

        male_ind = []
        female_ind = []

        len_ind = random.randint(3, 9) #Figure this out!
        half_ind = int(len_ind/2)

        for i in range(0, len_ind):
            ind_selected = inds_available[random.randint(0, len(inds_available)-1)]
            male_ind.append(ind_selected)
            inds_available.remove(ind_selected)        

        for i in range(0, len_ind):
            ind_selected = inds_available[random.randint(0, len(inds_available)-1)]
            female_ind.append(ind_selected)
            inds_available.remove(ind_selected)        
        
        children.append(male_ind[:half_ind] + female_ind[half_ind:])
        children.append(male_ind[half_ind:] + female_ind[:half_ind])

    return children

if __name__ == '__main__':
    
    pop = population(1000)

    generation = 0
    while (generation < 150):
        pop = evolve(pop)
        generation += 1
        p_fitness = pop_fitness(pop)
        print generation, round(p_fitness,2), len(inds_available)

    final = []

    for i in pop:
        arr = []
        for j in i:
            arr.append(d.GiftId[j])
        final.append(arr)

    pd.DataFrame({"Gifts": [" ".join(b) for b in final]}).to_csv("sub_genetic.csv", sep=",", index=False)
