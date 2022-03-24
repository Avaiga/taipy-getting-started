# Building the GUI and buttons

Let's update the GUI to display the results of the pipeline. You can find a "Predict" [button](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/button/) on the page to create the pipeline and run it. When you press the button, Taipy calls the function in the *on_action* parameter.

`<|Text displayed on button|button|on_action=fct_name_called_when_pressed|>`
   
A chart control has been added to the markdown to see if the predictions seem correct. The chart creates two traces: the historical values and the predicted values.

```python
import numpy as np
import pandas as pd

# Initialize the predictions dataset
predictions_dataset = pd.DataFrame({"Date":[dt.datetime(2021, 6, 1)], "Historical values":[np.NaN], "Predicted values":[np.NaN]})

# This is our new string with a button and a chart for our predictions
pipeline_page = page + """
Press <|predict|button|type=bar|on_action=predict|> to predict with default parameters (30 predictions) and June 1st as day.

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
"""
```

`create_and_submit_pipeline` creates and executes the pipeline after being called by `predict`. 

```python
def predict(state):
    print("'Predict' button clicked")
    pipeline = create_and_submit_pipeline()
    update_predictions_dataset(state, pipeline)

def create_and_submit_pipeline():
    "Function called by the predict function"
    print("Execution of pipeline...")
    # Create the pipeline from the pipeline config
    pipeline = tp.create_pipeline(baseline_pipeline_cfg)
    # Submit the pipeline (Execution)
    tp.submit(pipeline)
    return pipeline
```

After the first submission of the pipeline, the data stored in the data nodes are accessible (predictions, cleaned_data, etc.). It is the use of the `.read()` function.
`create_predictions_dataset` reads the data nodes to create a prediction dataset with these columns: Date, Historical values, Predicted values. The goal is to make the prediction dataset and display it in a chart. However, a good option would have been to create this dataset directly in the pipeline. It is typically good to put all complexity in it.

```python
def create_predictions_dataset(pipeline):
    "Function called by the update_predictions_dataset function"
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
```

When you press the 'Predict' button, Taipy calls this last function. It will update the predictions dataset, and this change will propagate to the chart.

```python

def update_predictions_dataset(state, pipeline):
    print("Updating predictions dataset...")
    # Update the predictions dataset
    state.predictions_dataset = create_predictions_dataset(pipeline)

Gui(page=pipeline_page).run()
```

<p align="center">
    <img src="/steps/images/step_5_result.png" width=700>
</p>
