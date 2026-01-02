import sys
import os
import json

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            logging.info("Enter to the ETL pipeline")
            logging.info("Take the data from the dataset...")
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            logging.info("Convert the data to the json format...")
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logging.error("csv_to_json_convertor function error...")
            raise NetworkSecurityException(e,sys) 

    def insert_data_to_mongodb(self,records,database,collection):

        try:
            logging.info("Enter to the ETL pipline Load part")
            self.records = records
            self.database = database
            self.collection = collection

            logging.info("Connect to the Mongo db")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[collection]

            self.collection.insert_many(self.records)
            logging.info("End the ETL pipeline")
            return(len(self.records))




        except Exception as e:
            logging.error("insert_data_to_mongodb function error...")
            raise NetworkSecurityException(e,sys)
        


if __name__=="__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "ChamiduAI"
    COLLECTION = "NetworkData"


    networkDataExtractObj= NetworkDataExtract()
    records=networkDataExtractObj.csv_to_json_convertor(FILE_PATH)
    print(records)
    number_of_records=networkDataExtractObj.insert_data_to_mongodb(records,DATABASE,COLLECTION)
    print(number_of_records)