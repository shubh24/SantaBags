import numpy as np 
import pandas as pd 
import random, sys, math

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

toy_arr = {
0:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "horse"],
1:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "ball"],
2:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "bike"],
3:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "train"],
4:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "coal"],
5:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "book"],
6:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "doll"],
7:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "blocks"],
8:[d.GiftId[i] for i in range(0, len(d)) if d.type[i] == "gloves"],
}

toy_map = {0:"horse", 1:"ball", 2:"bike", 3:"train", 4:"coal", 5:"book", 6:"doll", 7:"blocks", 8:"gloves"}
max_toys = [2,2,2,2,2,2,2,2,2]

def individual():

    knapsack = [int(math.floor(random.random()*max_toys[i])) for i in range(0, 9)]

    return knapsack

def population(pop_count):

    return [individual() for i in range(0, pop_count)]

def fitness(individual, target = 50):

    if sum(individual) < 3:
        return 0

    sum_pop = 0

    for i in range(0, 1000):
        sum_ind = sum([individual[i]*Weight(toy_map[i]) for i in range(0, len(individual))])

        if sum_ind <= target:
            sum_pop += sum_ind

    return sum_pop

def pop_fitness(pop):

    return sum([fitness(i) for i in pop])/len(pop)


def evolve(pop, target = 50, retain=0.55, random_select=0.05, mutate=0.01):

    sorted_pop = [x[1] for x in sorted([(fitness(i), i) for i in pop], reverse = True)]

    retain_length = int(len(sorted_pop)*retain)
    parents = sorted_pop[:retain_length]

    #Random Selection
    for i in sorted_pop[retain_length:]:

        if random_select > random.random():
            parents.append(i)

    #Mutate some individuals
    for ind in parents:

        if mutate > random.random():
            pos_to_mutate = random.randint(0, len(ind)-1)

            ind[pos_to_mutate] = int(math.floor(random.random()*max_toys[pos_to_mutate]))

    children = parents
     
    while len(children) < len(pop):

        male_ind = parents[random.randint(0, len(parents)-1)]
        female_ind = parents[random.randint(0, len(parents)-1)]
        half_ind = int(len(male_ind)/2)

        children.append(male_ind[:half_ind] + female_ind[half_ind:])
        children.append(male_ind[half_ind:] + female_ind[:half_ind])

    return children

if __name__ == '__main__':
    
    pop = population(100)

    generation = 0

    while (generation < 50):
        pop = evolve(pop)
        generation += 1
        p_fitness = pop_fitness(pop)
        print generation, round(p_fitness,2)

    final = []
    top_ind_counter = 0
    top_ind = pop[top_ind_counter]    
    
    for i in range(0, 1000):
        flag = 1
        arr = []
        print i
        while (flag == 1):
            top_ind = pop[random.randint(0, len(pop) - 1)]

            for j in range(0, len(top_ind)):
        
                for k in range(0, top_ind[j]):

                    try:
                        toy_selected = toy_arr[j][random.randint(0, len(toy_arr[j])-1)]
                        toy_arr[j].remove(toy_selected)

                        arr.append(toy_selected)
                        flag = 0
                    except:
                        pop.remove(top_ind)
                        flag = 1
                        print 'breaking', top_ind
                        break

                if flag == 1:
                    break

        final.append(arr)

    pd.DataFrame({"Gifts": [" ".join(b) for b in final]}).to_csv("sub_eff_genetic.csv", sep=",", index=False)
