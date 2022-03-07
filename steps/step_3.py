#import taipy as tp
from taipy import Taipy as tp
import datetime as dt
import pandas as pd
from taipy import Scope

from step_1 import path_to_csv

# datanodes (3.1)
initial_dataset_cfg = tp.configure_data_node(name="initial_dataset",
                                             storage_type="csv",
                                             path = path_to_csv,
                                             scope=Scope.SCENARIO)

nb_predictions_cfg = tp.configure_data_node(name="nb_predictions",
                                            default_data=30,
                                            scope=Scope.SCENARIO)

group_by_cfg = tp.configure_data_node(name="group_by",
                                      default_data="original",
                                      scope=Scope.SCENARIO)
                                            
                                            
day_cfg = tp.configure_data_node(name="day",
                                 default_data=dt.datetime(2014,6,1),
                                 scope=Scope.SCENARIO)

cleaned_dataset_cfg = tp.configure_data_node(name="cleaned_dataset",
                                             scope=Scope.SCENARIO)

predictions_cfg = tp.configure_data_node(name="predictions")

# functions (3.2)
def clean_data(initial_dataset,day,group_by):
    print("     Cleaning data")
    # convert the date column to datetime
    initial_dataset['Date'] = pd.to_datetime(initial_dataset['Date'])

    cleaned_dataset = change_data_with_group_by(initial_dataset,group_by)
    return cleaned_dataset
    
def change_data_with_group_by(dataset,group_by):
    if group_by != "original":
        dataset = dataset.resample(group_by[0], on='Date').sum()\
                                                          .reset_index(inplace=False)
    print(dataset.head())
    return dataset

def predict_baseline(cleaned_dataset, nb_predictions, day):
    # selecting the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date']<day]
    
    print("     Predicting baseline")
    predictions = train_dataset['Value'][-nb_predictions:].reset_index(drop=True)
    return predictions

# functions (3.3)
clean_data_cfg = tp.configure_task(name="clean_data",
                                   input=[initial_dataset_cfg,day_cfg,group_by_cfg],
                                   function=clean_data,
                                   output=cleaned_dataset_cfg)

predict_baseline_cfg = tp.configure_task(name="predict_baseline",
                                         input=[cleaned_dataset_cfg,nb_predictions_cfg,day_cfg],
                                         function=predict_baseline,
                                         output=predictions_cfg)