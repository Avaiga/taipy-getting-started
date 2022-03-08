from statsmodels.tsa.ar_model import AutoReg

from taipy import Frequency

from step_4 import *

# This is the function that will be used by the task
def predict_ml(cleaned_dataset: pd.DataFrame, nb_predictions: int, day: dt.datetime, group_by: str):
    print("     Predicting with ML")
    # Selecting the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date'] < day]
    
    # Choosing the lags based on the 'group_by'
    if group_by == "original":
        lags = 40
    elif group_by == "day":
        lags = 7
    elif group_by == "week":
        lags = 4
    elif group_by == "month":
        lags = 2
    
    # Fitting the AutoRegressive model
    model = AutoReg(train_dataset['Value'], lags=lags).fit()
    
    # Getting the nb_predictions forecasts
    predictions = model.forecast(nb_predictions).reset_index(drop=True)
    return predictions

# This is the task configuration if the predict_ml function.
# We use the same input and ouput as the previous predict_baseline task but we change the funtion
predict_ml_task_cfg = tp.configure_task(name="predict_ml",
                                  input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, group_by_cfg],
                                  function=predict_ml,
                                  output=predictions_cfg)

# We create a ml pipeline that will clean and predict with the ml model
pipeline_ml_cfg = tp.configure_pipeline(name="pipeline_ml",
                                        task_configs=[clean_data_task_cfg, predict_ml_task_cfg])


# We configure our scenario which is our business problem. Different scenarios would represent different solution to our business problem.
# Here, our scenario is influenced by the group_by, day and number of predictions.
# We have two pipelines in our scenario (baseline and ml), they represent our different models
scenario_cfg = tp.configure_scenario(name="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.DAILY) # We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

# The configuration is now complete, we will not come back to it later.

if __name__=='__main__':
    # We create the scenario
    scenario = tp.create_scenario(scenario_cfg)
    # We execute it
    tp.submit(scenario)
    # We get the resulting scenario
    scenario = tp.get(scenario.id) # delete
    
    # We print the predictions of the two pipelines
    print("\nBaseline predictions\n", scenario.pipeline_baseline.predictions.read())
    print("\nModel predictions\n", scenario.pipeline_ml.predictions.read())
    