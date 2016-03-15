'''
Created on 23/3/2015

@author: Charly
'''
import coloredlogs
import logging
import traceback

import gspread

from requests.packages.urllib3 import  disable_warnings


class ErrorHandler:

    def __init__(self):

        disable_warnings()

        lf = LoggerFactory()
        self.logger = lf.create_logger()

    def handle_error(self, e):
        self.logger.error(e)
        self.logger.error(traceback.format_exc())


class LoggerFactory:
    
    _instance = None
    
    @classmethod
    def create_logger(cls, name='ungoliant'):
        if not cls._instance:  
                
            coloredlogs.install()
            FORMAT = '%(asctime)-15s-8s %(message)s'
            logging.basicConfig(fomat=FORMAT)

            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
    
            logger.info("Mole Logger initialized")
            cls._instance = logger
        else:
            logger = cls._instance
        
        return logger

class GSpreadSheetFactory():

    def create(self,name, tab):
        gc = gspread.login('charly.lizarralde@gmail.com', 'oycobe77')
        wks = gc.open(name).worksheet(tab)
        return wks



class ServiceFactory:

    loggerFactory = LoggerFactory()
