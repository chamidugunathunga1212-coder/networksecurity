from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionConfig,Training_PipeLine_Config,DataVAlidationConfig

from netwoksecurity.components.data_validation import DataValidation

import sys

if __name__=='__main__':
    try:
        train_pipeline_congig = Training_PipeLine_Config()
        dataIngestionConfig = DataIngestionConfig(train_pipeline_congig)
        data_ingestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
        logging.info("Data ingestion is completed")

        dataValidationConfig = DataVAlidationConfig(train_pipeline_congig)
        
        data_validation = DataValidation(data_ingestion_artifacts,dataValidationConfig)
        logging.info("Initiate the data validation")
        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts)
        logging.info("Data validation is completed")




    except Exception as e:
        raise NetworkSecurityException(e,sys)