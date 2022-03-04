from statsmodels.tsa.ar_model import AutoReg

from step_4_backend import *

# the function that will be used by the task
def predict_ml(cleaned_dataset, nb_predictions, day, group_by):
    # selecting the train data
    train_dataset = cleaned_dataset[cleaned_dataset['Date']<day]
    
    print("     Predicting with ML")
    if group_by == "original":
        lags = 40
    elif group_by == "day":
        lags = 7
    elif group_by == "week":
        lags = 4
    elif group_by == "month":
        lags = 2
    
    model = AutoReg(cleaned_dataset['Value'],lags=lags).fit()
    predictions = model.forecast(nb_predictions).reset_index(drop=True)
    return predictions

# This is the task configuration. We use the same input and ouput as the previous predict_baseline task
# but we change the funtion
predict_ml_cfg = tp.configure_task(name="predict_baseline",
                                  input=[cleaned_dataset_cfg,nb_predictions_cfg,day_cfg],
                                  function=predict_ml,
                                  output=predictions_cfg)

# we create a ml pipeline that will clean and predict with the ml model
pipeline_ml_cfg = tp.configure_pipeline(name="pipeline_ml",
                                        task_configs=[clean_data_cfg,predict_ml_cfg])

# we configure our scenario which is our business problem
# we have two pipelines in our scenario (baseline and ml), they represent our different models
scenario_cfg = tp.configure_scenario(name="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg,pipeline_ml_cfg])

if __name__=='__main__':
    # we create the scenario
    scenario = tp.create_scenario(scenario_cfg)
    # we execute it
    tp.submit(scenario)
    # we get the resulting scenario
    scenario = tp.get(scenario.id)
    
    # we print the predictions of the two pipelines
    print("\nBaseline predictions\n",scenario.pipelines['pipeline_baseline'].predictions.read())
    print("\nModel predictions\n",scenario.pipelines['pipeline_ml'].predictions.read())
    