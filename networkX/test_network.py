import networkx as nx
import pymongo as p

# import matplotlib.pyplot as plt

client = p.MongoClient()
db = client['mole']

#ids usuarios
users_topico = []

# defino topico
topico = ["messi"]

# me quedo con los tweets del topico
tweet = db.tweet.find({'text': {'$regex': topico[0]}})

# me quedo con lo usuarios de esos tweets
for record in tweet:
    users_topico.append(record['user']['id'])

users_filter = db.user.find({"id": {"$in": users_topico}})

adj_list=[]

for user in users_filter:
    followers = ""
    if user['followers']:
        followers = " " + " ".join(str(x) for x in user['followers'])
    adj_list.append(str(user['id']) + followers)

g = nx.parse_adjlist(adj_list, nodetype = int)

degree_centrality = nx.degree_centrality(g)
# closeness_centrality = nx.closeness_centrality(g)
# betweenness_centrality = nx.betweenness_centrality(g)
# eigenvector_centrality = nx.eigenvector_centrality(g)












#g = nx.read_adjlist("C:\Users\Marina\Desktop\TIP\To_test\miniSedEdgeList.csv", delimiter=", ", create_using=nx.Graph(), encoding = 'utf-8')







# to get more that one element
# e= max(eigenvector_centrality.values())
# keys = [x for x,y in eigenvector_centrality.items() if y ==e]

max = max(degree_centrality.iterkeys(), key=lambda k: degree_centrality[k])
user = db.user.find_one({u'id': max})

print user
# print keys
