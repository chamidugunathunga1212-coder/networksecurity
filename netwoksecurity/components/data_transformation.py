import sys
import os
import pandas as pd
from netwoksecurity.constants import training_pipeline
from netwoksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from netwoksecurity.entity.config_entity import DataVAlidationConfig,DataTransformationConfig
from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging
from netwoksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

from netwoksecurity.constants.training_pipeline import TARGET_COLUMN
from netwoksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from typing import Optional
import numpy as np


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_validation_artifacts:DataValidationArtifact = data_validation_artifacts
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            logging.info(f"Reading data from file: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)    
        
    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info(f"Creating data transformer object")
            ## create imputer object
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            scaler = StandardScaler()
            pipeline:Pipeline = Pipeline(steps=[
                ("imputer", imputer),
                ("scaler", scaler)
            ])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Initiating data transformation")
            # load train and test file path
            valid_train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            valid_test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)
            logging.info(f"Loading training and testing data")

            ## training dataframe
            input_feature_train_df = valid_train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_df = valid_train_df[TARGET_COLUMN]
            target_train_df = target_train_df.replace(-1,0)

            ## testing dataframe
            input_feature_test_df = valid_test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_df = valid_test_df[TARGET_COLUMN]
            target_test_df = target_test_df.replace(-1,0)
            

            logging.info(f"Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

        
            ## transforming using preprocessor object
            logging.info(f"Applying preprocessing object on training and testing data")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)



            # # target encoder
            # label_encoder = LabelEncoder()
            # target_feature_train_arr = label_encoder.fit_transform(target_feature_train_df)
            # target_feature_test_arr = label_encoder.transform(target_feature_test_df)

            # concatenate input and target feature array
            train_arr = np.c_[input_feature_train_arr, np.array(target_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_test_df)]

            # save numpy arrays
            logging.info(f"Saving transformed training and testing arrays")

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)

            # save preprocessing object
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessing_obj)

            # prepare artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            logging.info(f"Data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        