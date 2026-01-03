from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionConfig,Training_PipeLine_Config

import sys

if __name__=='__main__':
    try:
        train_pipeline_congig = Training_PipeLine_Config()
        dataIngestionConfig = DataIngestionConfig(train_pipeline_congig)
        data_ingestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
    except Exception as e:
        raise NetworkSecurityException(e,sys)