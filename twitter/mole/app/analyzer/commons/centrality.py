from mole.app.models import UrlsGraph, CentralityUrl
import networkx as nx

from mole.app.utils import LoggerFactory

logger = LoggerFactory.create_logger()


class Centrality:

    def __init__(self):
        pass

    def calculate_cetrality(self, data):

        logger.info("Starting calculating centrality")
        adj_list = []

        for user in data:
            adj_list.append(str(user.user_oid_i) + " " + str(user.user_oid_j))

        g = nx.parse_adjlist(adj_list, nodetype=int)
        logger.info(str(len(adj_list)))
        # calculo centralidad de grados
        degree_centrality = nx.degree_centrality(g)
        logger.info("Finish calculating centrality")

        return degree_centrality





