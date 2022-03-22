# Building the GUI and buttons

Let's update the GUI to display the results of the pipeline. You can find a "Predict" [button](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/button/) on the page that will create and run it. The function in the *on_action* parameter will be called whenever the button is pressed.

`<|Text displayed on button|button|on_action=fct_name_called_when_pressed|>`

The results is then displayed in the chart by updating it. A good option would have been to directly create the results in the piepline before. It is typically the good practice to put all complexicity of a pipeline in it.


```python
import numpy as np
import pandas as pd

# Initialize the predictions dataset
predictions_dataset = pd.DataFrame({"Date":[dt.datetime(2021, 6, 1)], "Historical values":[np.NaN], "Predicted values":[np.NaN]})

# This is our new string with a button and a chart for our predictions
pipeline_page = page + """
Press <|predict|button|on_action=predict|> to predict with default parameters (30 predictions) and June 1st as day. 
<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

def create_and_submit_pipeline():
    "Function called by the predict function"
    print("Execution of pipeline...")
    # Create the pipeline from the pipeline config
    pipeline = tp.create_pipeline(baseline_pipeline_cfg)
    # Submit the pipeline (Execution)
    tp.submit(pipeline)
    return pipeline


def create_predictions_dataset(pipeline):
    "Function called by the update_predictions_dataset function"
    print("Creating predictions dataset...")
    # Read data from the pipeline
    predictions = pipeline.predictions.read()
    day = pipeline.day.read()
    number_predictions = pipeline.number_predictions.read()
    cleaned_data = pipeline.cleaned_dataset.read()
    
    # Set the time window for the chart (5 days, 5 weeks, 5 months,...)
    window = 5 * number_predictions

    # Create the historical dataset that will be displayed
    new_length = len(cleaned_data[cleaned_data['Date'] < day]) + number_predictions
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
    
def predict(state):
    print("'Predict' button clicked")
    pipeline = create_and_submit_pipeline()
    update_predictions_dataset(state, pipeline)


Gui(page=pipeline_page).run()
```
    