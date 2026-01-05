from netwoksecurity.components.data_ingestion import DataIngestion
from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging
from netwoksecurity.entity.config_entity import DataIngestionConfig, DataTransformationConfig,Training_PipeLine_Config,DataVAlidationConfig

from netwoksecurity.components.data_validation import DataValidation

from netwoksecurity.components.data_transformation import DataTransformation
from netwoksecurity.entity.artifact_entity import DataTransformationArtifact

from netwoksecurity.components.model_trainer import ModelTrainer
from netwoksecurity.entity.config_entity import ModelTrainerConfig

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

        logging.info("Initiate the data transformation")

        data_transformation_config = DataTransformationConfig(training_pipeline_config=train_pipeline_congig)
        data_transform = DataTransformation(data_validation_artifacts,data_transformation_config)
        data_transform_artifacts = data_transform.initiate_data_transformation()
        print(data_transform_artifacts)
        logging.info("Data transformation is completed")


        logging.info("Data taraining is started")

        data_training_config = ModelTrainerConfig(training_pipeline_config=train_pipeline_congig)
        model_trainer = ModelTrainer(data_training_config,data_transform_artifacts)
        model_trainer_artifacts = model_trainer.initiate_model_trainer()
        print(model_trainer_artifacts)



        logging.info("Data training is completed")











    except Exception as e:
        raise NetworkSecurityException(e,sys)