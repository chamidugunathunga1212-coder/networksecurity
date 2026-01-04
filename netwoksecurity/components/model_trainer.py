import os
import sys


from netwoksecurity.exception.exception import NetworkSecurityException
from netwoksecurity.logging.logger import logging

from netwoksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from netwoksecurity.entity.config_entity import DataTransformationConfig, ModelTrainerConfig

from netwoksecurity.utils.main_utils import load_numpy_array_data,save_object


from netwoksecurity.utils.ml_utils.model.estimator import NetworkModel

from netwoksecurity.utils.main_utils import load_numpy_array_data,evaluate_models
from netwoksecurity.utils.ml_utils.metric.classification_metric import get_classification_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)