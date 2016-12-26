import numpy as np 
import pandas as pd 

d = pd.read_csv("gifts.csv")
d['type'] = d['GiftId'].apply(lambda x: x.split('_')[0])
d['id'] = d['GiftId'].apply(lambda x: x.split('_')[1])

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

d['weight'] = d['type'].apply(lambda x: Weight(x))

sorted_weights = d.sort_values(by=['weight'], ascending = [False])

data = pd.DataFrame(pd.np.empty((1000, 1)) * pd.np.nan, columns = ['bag_weights']) 
data['bag_weights'] = 0
data['gifts'] = np.empty((1000, 0)).tolist()

for idx, row in sorted_weights.iterrows():
	data = data.sort_values(by = ['bag_weights'], ascending = [True])

	for b_idx, b_row in data.iterrows():

		if row.weight + b_row.bag_weights <= 50 and len(b_row.gifts) < 9:
			b_row.gifts.append(row.GiftId)
			data.set_value(b_idx, 'bag_weights',float(b_row.bag_weights) + float(row.weight))
			break

packed_bags = [[]]
total_sum = 0

for b_idx, b_row in data.iterrows():
	if len(b_row.gifts) >= 3:
		total_sum += b_row.bag_weights
		packed_bags.append(" ".join(b_row.gifts))

print total_sum

f = open('sub.csv', 'wb')
for i in packed_bags:
	f.write(str(i)+"\n")
f.close()
