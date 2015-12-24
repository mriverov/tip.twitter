from mole.app.models import UrlsGraph, CentralityUrl
import networkx as nx

from mole.app.utils import LoggerFactory

logger = LoggerFactory.create_logger()


class Centrality:

    def __init__(self):
        pass

    def calculate_cetrality_by_url(self):

        logger.info("Starting calculating centrality")
        adj_list = []

        for user in UrlsGraph.objects.all():
            adj_list.append(str(user.user_oid_i) + " " + str(user.user_oid_j))

        g = nx.parse_adjlist(adj_list, nodetype=int)

        # calculo centralidad de grados
        degree_centrality = nx.degree_centrality(g)
        logger.info("Finish calculating centrality")

        logger.info("Starting saving centrality")
        for user_id, centrality in degree_centrality.iteritems():
            url_centrality = CentralityUrl(user_id=user_id, centrality=centrality)
            url_centrality.save()
        logger.info("Finish saving centrality")




