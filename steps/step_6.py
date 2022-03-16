from statsmodels.tsa.ar_model import AutoReg

from step_4 import *
from step_3 import cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, offset_cfg, predictions_cfg, pd, dt

# This is the function that will be used by the task
def predict_ml(cleaned_dataset: pd.DataFrame, nb_predictions: int, day: dt.datetime, offset: int):
    print("     Predicting with ML")
    # Select the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date'] < day]
    
    # Fit the AutoRegressive model
    model = AutoReg(train_dataset['Value'], lags=7).fit()
    
    # Get the nb_predictions forecasts
    predictions = model.forecast(nb_predictions).reset_index(drop=True) * offset/100
    return predictions

# Create the task configuration of the predict_ml function.
## We use the same input and ouput as the previous predict_baseline task but we change the funtion
predict_ml_task_cfg = tp.configure_task(id="predict_ml",
                                        function=predict_ml,
                                        input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, offset_cfg],
                                        output=predictions_cfg)

# Create a ml pipeline that will clean and predict with the ml model
ml_pipeline_cfg = tp.configure_pipeline(id="ml", task_configs=[clean_data_task_cfg, predict_ml_task_cfg])


# Configure our scenario which is our business problem.
## Different scenarios would represent different solution to our business problem.
## Here, our scenario is influenced by the group_by, day and number of predictions.
## We have two pipelines in our scenario (baseline and ml), they represent our different models
scenario_cfg = tp.configure_scenario(id="scenario", pipeline_configs=[baseline_pipeline_cfg, ml_pipeline_cfg]) 

# The configuration is now complete

if __name__=='__main__':
    # Create the scenario
    scenario = tp.create_scenario(scenario_cfg)
    # Execute it
    tp.submit(scenario)
    # Get the resulting scenario
    
    # Print the predictions of the two pipelines (baseline and ml)
    print("\nBaseline predictions\n", scenario.baseline.predictions.read())
    print("\nMachine Learning predictions\n", scenario.ml.predictions.read())        