import json

# Opening JSON file
f = open('responses.json')

# returns JSON object as 
# a dictionary
data = json.load(f)

# analysis follows https://tech.ebayinc.com/engineering/measuring-search-relevance/

all_ndcg = []

for query in data['data']:
    
    # find the gain and remove any bad sessions
    g = data['data'][query]['rankings']
    if -1 in g: continue
    if all(item == 0 for item in g): continue

    # calculate discounted gain
    dg = g[:]
    for i in range(len(dg)):
        dg[i] = dg[i] / (i+1)

    # calculated discounted cumulative gain
    dcg = []
    sum = 0
    for i in range(len(dg)):
        sum += dg[i]
        dcg.append(sum)
    
    # calculate ideal discounted gain
    idg = g[:]
    idg.sort(reverse=True)
    for i in range(len(dg)):
        idg[i] = idg[i] / (i+1)
    
    # calculate ideal discounted cumulative gain
    idcg = []
    sum = 0
    for i in range(len(idg)):
        sum += idg[i]
        idcg.append(sum)

    # calculate normalized discounted cumulative gain
    ndcg = []
    for i in range(len(dcg)):
        ndcg.append(dcg[i]/idcg[i])
    
    all_ndcg.extend(ndcg)

sum = 0
for item in all_ndcg:
    sum += item

print(sum / len(all_ndcg))