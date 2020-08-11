import sys
import random
import math
import pprint
import pandas as pd
random.seed(0)

bids = {}
budgets = {}
data = pd.read_csv("bidder_dataset.csv")
for i in data.index:
    if data['Advertiser'][i] not in budgets.keys():
        budgets[data['Advertiser'][i]] = data['Budget'][i]
    if data['Keyword'][i] not in bids.keys():
        bids[data['Keyword'][i]] = {}
        bids[data['Keyword'][i]][data['Advertiser'][i]] = data['Bid Value'][i]
    if data['Keyword'][i] in bids.keys():
        bids[data['Keyword'][i]][data['Advertiser'][i]] = data['Bid Value'][i]


new_queries = []
f = open("queries.txt", "r").readlines()
for x in f:
    new_queries.append(x.strip())


def greedy(budgets,bids,queries):
    #for revenue calculation
    revenue = 0.0
    new_budgets = budgets.copy()
    for query in queries:
        neighbours = []
        for i in bids[query].keys():
            if new_budgets[i] >= bids[query][i]:
                neighbours.append(i)
        if len(neighbours)!=0:
            maxi = 0
            old = 0
            for neighbour in neighbours:
                if bids[query][neighbour] > old:
                    old = bids[query][neighbour]
                    maxi = neighbour
                if bids[query][neighbour] == old: #if two neighbours have same bid choose the neighbour with lowest id
                    if neighbour < maxi:
                        maxi = neighbour
                    else:
                        maxi = maxi
            new_bidder = maxi
            revenue = revenue + bids[query][new_bidder]
            new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
    print ("revenue: %f" % (revenue))
    
    OPT = sum(budgets.values())
    revenues = []


    #for competitive ratio calculation
    for i in range(100):
        random.shuffle(queries)
        revenue = 0.0
        new_budgets = budgets.copy()
#         print(len(queries))
        for query in queries:
            neighbours = []
            for i in bids[query].keys():
                if new_budgets[i] >= bids[query][i]:
                    neighbours.append(i)
            if len(neighbours)!=0:
                maxi = 0
                old = 0
                for neighbour in neighbours:
                    if bids[query][neighbour] > old:
                        old = bids[query][neighbour]
                        maxi = neighbour
                    if bids[query][neighbour] == old: #if two neighbours have same bid choose the neighbour with lowest id
                        if neighbour < maxi:
                            maxi = neighbour
                        else:
                            maxi = maxi
                new_bidder = maxi
                revenue = revenue + bids[query][new_bidder]
                new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
        print(revenue)
        revenues.append(revenue)
    
    ALG = float(sum(revenues)) / len(revenues)
#     print(sum(revenues))
    print ("competitive ratio: %f" % (ALG / OPT))


def mssv(budgets,bids,queries):
    #for revenue calculation
    revenue = 0.0
    new_budgets = budgets.copy()
    for query in queries:
        neighbours = []
        for i in bids[query].keys():
            if new_budgets[i] >= bids[query][i]:
                neighbours.append(i)
        if len(neighbours)!=0:
            who_ever_spent = {}
            for n in neighbours:
                who_ever_spent[n] = bids[query][n]*(1-math.exp(-1*new_budgets[n]/budgets[n]))
            
            maxi = 0
            old = 0
            for neighbour in neighbours:
                if who_ever_spent[neighbour] > old:
                    old = who_ever_spent[neighbour]
                    maxi = neighbour
                if who_ever_spent[neighbour] == old: #if two neighbours have same value spent choose the neighbour with lowest id
                    if neighbour < maxi:
                        maxi = neighbour
                    else:
                        maxi = maxi   
            new_bidder = maxi
            revenue = revenue + bids[query][new_bidder]
            new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
    print ("revenue: %f" % (revenue))
    OPT = sum(budgets.values())
    revenues = []
    
    #for competitive ratio calculation
    for i in range(100):
        random.shuffle(queries)
        revenue = 0.0
        new_budgets = budgets.copy()
        for query in queries:
            neighbours = []
            for i in bids[query].keys():
                if new_budgets[i] >= bids[query][i]:
                    neighbours.append(i)
            if len(neighbours)!=0:
                who_ever_spent = {}
                for n in neighbours:
                    who_ever_spent[n] = bids[query][n]*(1-math.exp(-1*new_budgets[n]/budgets[n]))

                maxi = 0
                old = 0
                for neighbour in neighbours:
                    if who_ever_spent[neighbour] > old:
                        old = who_ever_spent[neighbour]
                        maxi = neighbour
                    if who_ever_spent[neighbour] == old: #if two neighbours have same value spent choose the neighbour with lowest id
                        if neighbour < maxi:
                            maxi = neighbour
                        else:
                            maxi = maxi

                new_bidder = maxi
                revenue = revenue + bids[query][new_bidder]
                new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
        print(revenue)
        revenues.append(revenue)
    
    ALG = float(sum(revenues)) / len(revenues)
#     print(sum(revenues))
    print ("competitive ratio: %f" % (ALG / OPT))


def balance(budgets,bids,queries):
    #for revenue calculation
    revenue = 0.0
    new_budgets = budgets.copy()
    for query in queries:
        neighbours = []
        for i in bids[query].keys():
            if new_budgets[i] >= bids[query][i]:
                neighbours.append(i)
        if len(neighbours)!=0:
            maxi = 0
            old = 0
            for neighbour in neighbours:
                if new_budgets[neighbour] > old:
                    old = new_budgets[neighbour]
                    maxi = neighbour
                if new_budgets[neighbour] == old: #if two neighbours have same unspent budget choose the neighbour with lowest id
                    if neighbour < maxi:
                        maxi = neighbour
                    else:
                        maxi = maxi
            new_bidder = maxi
            revenue = revenue + bids[query][new_bidder]
            new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
    print ("revenue: %f" % (revenue))
    OPT = sum(budgets.values())
    revenues = []

    #for competitive ratio calculation
    for i in range(100):
        random.shuffle(queries)
        revenue = 0.0
        new_budgets = budgets.copy()
        for query in queries:
            neighbours = []
            for i in bids[query].keys():
                if new_budgets[i] >= bids[query][i]:
                    neighbours.append(i)
            if len(neighbours)!=0:
                maxi = 0
                old = 0
                for neighbour in neighbours:
                    if new_budgets[neighbour] > old:
                        old = new_budgets[neighbour]
                        maxi = neighbour
                    if new_budgets[neighbour] == old: #if two neighbours have same unspent budget choose the neighbour with lowest id
                        if neighbour < maxi:
                            maxi = neighbour
                        else:
                            maxi = maxi
                new_bidder = maxi
                revenue = revenue + bids[query][new_bidder]
                new_budgets[new_bidder] = new_budgets[new_bidder] - bids[query][new_bidder]
        print(revenue)
        revenues.append(revenue)
    
    ALG = float(sum(revenues)) / len(revenues)
#     print(sum(revenues))
    print ("competitive ratio: %f" % (ALG / OPT))


if sys.argv[1] == "greedy":
    greedy(budgets,bids,new_queries)
if sys.argv[1] == "mssv":
    mssv(budgets,bids,new_queries)
if sys.argv[1] == "balance":
    balance(budgets,bids,new_queries)