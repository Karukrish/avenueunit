import configparser
import random



confobj = configparser.RawConfigParser()
confobj.read('config.ini')



class Readconfig():

    
    @staticmethod
    def getusername():
        nameofuser = confobj.get('commoninfo','agentname')
        return nameofuser
    
    @staticmethod
    def getpassword():
        password = confobj.get('commoninfo','password')
        return password
    
    @staticmethod
    def getdevice():
        device =  confobj.get('commoninfo','device')
        return device
    
    @staticmethod
    def getid():
        versionid = f'{random.randrange(16**24):024x}'
        return versionid

