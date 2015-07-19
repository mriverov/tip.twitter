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

# armo el "adjencency list" como string
adj_list = []

for user in users_filter:
    followers = ""
    if user['followers']:
        followers = " " + " ".join(str(x) for x in user['followers'])
    adj_list.append(str(user['id']) + followers)

# armo el grafo a partir del string
g = nx.parse_adjlist(adj_list, nodetype = int)

# calculo centralidad de grado
degree_centrality = nx.degree_centrality(g)
# closeness_centrality = nx.closeness_centrality(g)
# betweenness_centrality = nx.betweenness_centrality(g)
# eigenvector_centrality = nx.eigenvector_centrality(g)

# obtengo el usuario con mayor centralidad
max = max(degree_centrality.iterkeys(), key = lambda k: degree_centrality[k])
user = db.user.find_one({u'id': max})
