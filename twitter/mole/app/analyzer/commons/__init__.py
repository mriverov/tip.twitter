from mole.app.utils import LoggerFactory
from mole.app.analyzer.commons.filterService import FilterService
from mole.app.analyzer.commons.projectService import ProjectService
import pymongo as p
from datetime import datetime


logger = LoggerFactory.create_logger()

client = p.MongoClient()
db = client['mole']


if __name__ == '__main__':

    # logger.info("start")
    # regex = '|'.join(["lanata", "macri", "90"])
    # #tweets = db.tweet.find({"text": {"$regex": regex, "$options": "i"} , 'entities.hashtags': {"$in": ["TVRKalabaza"]} })#,
    #                         #'entities.urls': {"$in": [""]}
    #                         #})
    #
    # tweets = db.tweet.find({
    #         "$or": [{
    #             "text": {"$regex": regex, "$options": "i"}
    #         }, {
    #             "entities.hashtags": {"$in": ["TVRKalabaza"]}
    #         }, {
    #             "entities.urls": {"$in": [""]}
    #         }]
    #     });
    #
    # logger.info("Finish")
    # logger.info((tweets.count()))

    # filterService = FilterService()
    project_service = ProjectService()
    from_date = datetime.strptime('2015-09-10', '%Y-%m-%d')
    to_date = datetime.strptime('2015-09-14', '%Y-%m-%d')
    # filters = filterService.generate_filters(["macri"], date_from, date_to)
    # logger.info(str(filters))

    project_id = project_service.save_project("Test")
    project_service.start(project_id, ["macri"], from_date, to_date)



    '''
    date_from = datetime.strptime('2015-12-13', '%Y-%m-%d')
    date_to = datetime.strptime('2015-12-14', '%Y-%m-%d')

    moleConfiguration = MoleConfigurationService()
    project = moleConfiguration.save_project("Test")

    analyzer = AnalizerService()
    analyzer.start_analyzer(project, ["lanata", "macri", "90"], "TVRKalabaza", None, date_from, date_to)
    '''
