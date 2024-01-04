import pytest
import logging
#from homepage import Testpage


@pytest.mark.usefixtures('login')
class Baseclass():
    
    @staticmethod
    def logger():
        
        logger=logging.getLogger(__name__)
        filehandler = logging.FileHandler('logfile.log',mode='a')
        logger.addHandler(filehandler) #filehandler object

        formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s: %(message)s :")
        filehandler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        return logger
        

