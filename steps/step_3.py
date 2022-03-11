import datetime as dt
import pandas as pd

import taipy as tp
from taipy import Scope

from step_1 import path_to_csv

# Datanodes (3.1)
## Input datanodes
initial_dataset_cfg = tp.configure_data_node(id="initial_dataset",
                                             storage_type="csv",
                                             path=path_to_csv,
                                             scope=Scope.SCENARIO)

nb_predictions_cfg = tp.configure_data_node(id="nb_predictions",
                                            default_data=40,
                                            scope=Scope.SCENARIO)

group_by_cfg = tp.configure_data_node(id="group_by",
                                      default_data="original",
                                      scope=Scope.SCENARIO)
                                            
                                            
day_cfg = tp.configure_data_node(id="day",
                                 default_data=dt.datetime(2014, 6, 1),
                                 scope=Scope.SCENARIO)

## Rest of datanodes
cleaned_dataset_cfg = tp.configure_data_node(id="cleaned_dataset",
                                             scope=Scope.SCENARIO) # ,
                                                                   # cacheable=True,
                                                                   # validity_period=dt.timedelta(days=1)

predictions_cfg = tp.configure_data_node(id="predictions",
                                         scope=Scope.PIPELINE)



# Functions (3.2)
def clean_data(initial_dataset: pd.DataFrame, group_by: str):
    print("     Cleaning data")
    # Convert the date column to datetime
    initial_dataset['Date'] = pd.to_datetime(initial_dataset['Date'])

    cleaned_dataset = change_data_with_group_by(initial_dataset, group_by)
    return cleaned_dataset
    
def change_data_with_group_by(cleaned_dataset: pd.DataFrame, group_by: str):
    if group_by != "original":
        cleaned_dataset = cleaned_dataset.resample(group_by[0], on='Date').sum()\
                                                                          .reset_index(inplace=False)
    return cleaned_dataset




def predict_baseline(cleaned_dataset: pd.DataFrame, nb_predictions: int, day: dt.datetime):
    print("     Predicting baseline")
    # Selecting the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date'] < day]
    
    predictions = train_dataset['Value'][-nb_predictions:].reset_index(drop=True)
    return predictions




# Tasks (3.3)
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        input=[initial_dataset_cfg, group_by_cfg],
                                        function=clean_data,
                                        output=cleaned_dataset_cfg)

predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg],
                                              function=predict_baseline,
                                              output=predictions_cfg)