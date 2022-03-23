import numpy as np
import pandas as pd

from step_4_pipeline_execution import tp, baseline_pipeline_cfg, dt
from step_2_on_change import *


# Initialize the predictions dataset
predictions_dataset = pd.DataFrame({"Date":[dt.datetime(2021, 6, 1)], "Historical values":[np.NaN], "Predicted values":[np.NaN]})

# This is our new string with a button and a chart for our predictions
pipeline_page = page + """
Press <|predict|button|on_action=predict|> to predict with default parameters (30 predictions) and June 1st as day.

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

def predict(state):
    print("'Predict' button clicked")
    pipeline = create_and_submit_pipeline()
    update_predictions_dataset(state, pipeline)

def create_and_submit_pipeline():
    print("Execution of pipeline...")
    # Create the pipeline from the pipeline config
    pipeline = tp.create_pipeline(baseline_pipeline_cfg)
    # Submit the pipeline (Execution)
    tp.submit(pipeline)
    return pipeline


def create_predictions_dataset(pipeline):
    print("Creating predictions dataset...")
    # Read data from the pipeline
    predictions = pipeline.predictions.read()
    day = pipeline.day.read()
    n_predictions = pipeline.n_predictions.read()
    cleaned_data = pipeline.cleaned_dataset.read()
    
    # Set the time window for the chart (5 days, 5 weeks, 5 months,...)
    window = 5 * n_predictions

    # Create the historical dataset that will be displayed
    new_length = len(cleaned_data[cleaned_data['Date'] < day]) + n_predictions
    temp_df = cleaned_data[:new_length]
    temp_df = temp_df[-window:].reset_index(drop=True)
    
    # Create the series that will be used in the concat
    historical_values = pd.Series(temp_df['Value'], name="Historical values")
    predicted_values = pd.Series([np.NaN]*len(temp_df), name="Predicted values") # change ? Fred
    predicted_values[-len(predictions):] = predictions
    
    # Create the predictions dataset
    # Columns : [Date, Historical values, Predicted values]
    return pd.concat([temp_df['Date'], historical_values, predicted_values], axis=1)
    

def update_predictions_dataset(state, pipeline):
    print("Updating predictions dataset...")
    # Update the predictions dataset
    state.predictions_dataset = create_predictions_dataset(pipeline)
    

if __name__ == "__main__":
    Gui(page=pipeline_page).run()
    