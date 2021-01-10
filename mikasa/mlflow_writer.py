import mlflow
from mlflow.exceptions import RestException
from mlflow.tracking import MlflowClient


class MlflowWriter(object):
    def __init__(self, experiment_name, **kwargs):
        self.client = MlflowClient(**kwargs)
        self.experiment_name = experiment_name
        self.experiment_id = self.get_experiment_id(experiment_name)
        self.run_id = self.client.create_run(self.experiment_id).info.run_id

    def get_experiment_id(self, experiment_name):
        experiment_names = self.get_list_experiment_names()
        if experiment_name in experiment_names:
            experiment_id = self.client.get_experiment_by_name(
                experiment_name
            ).experiment_id
        else:
            experiment_id = self.client.create_experiment(experiment_name)
        return experiment_id

    def get_list_experiment_names(self):
        experiments = self.client.list_experiments()
        experiment_names = [exp.name for exp in experiments]
        return experiment_names

    def log_param_from_dict(self, param_dict: dict, prefix=""):
        for key, value in param_dict.items():
            if len(prefix) > 0:
                key = prefix + key
            self.log_param(key, value)

    def log_param(self, key, value):
        self.client.log_param(self.run_id, key, value)

    def log_metric(self, key, value):
        self.client.log_metric(self.run_id, key, value)

    def log_artifact(self, local_path):
        self.client.log_artifact(self.run_id, local_path)

    def set_terminated(self):
        self.client.set_terminated(self.run_id)
