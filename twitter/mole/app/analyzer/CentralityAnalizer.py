__author__ = 'Marina'

import networkx as nx


class CentralityAnalyzer:

    def __init__(self):
        pass

    def get_centrality_by_user(self, users):

        # armo el "adjencency list" como string
        adj_list = []

        for user in users:
            followers = ""
            user_followers = [follower.user_id for follower in user.followers.all()]
            if user.followers:
                followers = " " + " ".join(str(x) for x in user_followers)
            adj_list.append(str(user.user_id) + followers)

        # armo el grafo a partir del string
        g = nx.parse_adjlist(adj_list, nodetype=int)

        # calculo centralidad de grado
        degree_centrality = nx.degree_centrality(g)
        # closeness_centrality = nx.closeness_centrality(g)
        # betweenness_centrality = nx.betweenness_centrality(g)
        # eigenvector_centrality = nx.eigenvector_centrality(g)

        return degree_centrality