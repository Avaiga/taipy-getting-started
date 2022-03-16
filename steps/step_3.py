import datetime as dt
import pandas as pd

import taipy as tp
from taipy import Scope

from step_1 import path_to_csv

# Datanodes (3.1)
## Input datanodes
initial_dataset_cfg = tp.configure_data_node(id="initial_dataset",
                                             storage_type="csv",
                                             path=path_to_csv)

nb_predictions_cfg = tp.configure_data_node(id="nb_predictions", default_data=40)

offset_cfg = tp.configure_data_node(id="offset", default_data="original")

day_cfg = tp.configure_data_node(id="day", default_data=dt.datetime(2014, 7, 26)) # take a normal day / with a normal week

## Remaining datanodes
cleaned_dataset_cfg = tp.configure_data_node(id="cleaned_dataset") # ,
                                                                   # cacheable=True,
                                                                   # validity_period=dt.timedelta(days=1)

predictions_cfg = tp.configure_data_node(id="predictions", scope=Scope.PIPELINE)



# Functions (3.2)
def clean_data(initial_dataset: pd.DataFrame):
    print("     Cleaning data")
    # Convert the date column to datetime
    initial_dataset['Date'] = pd.to_datetime(initial_dataset['Date'])
    cleaned_dataset = initial_dataset.copy()
    return cleaned_dataset
    



def predict_baseline(cleaned_dataset: pd.DataFrame, nb_predictions: int, day: dt.datetime, offset: int):
    print("     Predicting baseline")
    # Selecting the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date'] < day]
    
    predictions = train_dataset['Value'][-nb_predictions:].reset_index(drop=True) * offset/100
    return predictions




# Tasks (3.3)
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        function=clean_data,
                                        input=[initial_dataset_cfg],
                                        output=cleaned_dataset_cfg)

predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              function=predict_baseline,
                                              input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, offset_cfg],
                                              output=predictions_cfg)