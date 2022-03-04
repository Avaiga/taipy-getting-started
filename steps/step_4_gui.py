import numpy as np

from step_4_backend import *
from step_2 import *

# initialize the predictions dataset
predictions_dataset = pd.DataFrame({"Date":[dt.datetime(2014,6,1)],"Historical values":[np.NaN],"Predicted values":[np.NaN]})

md_step_4 = md_step_2 + """
Press <|predict|button|on_action=predict|> to predict with default parameters (30 predictions) and June 1st as day. 
<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|type=bar|>
"""

def create_and_submit_pipeline():
    print("Execution of pipeline...")
    # we create the pipeline from the pipeline config
    pipeline = tp.create_pipeline(pipeline_baseline_cfg)
    # we execute the pipeline
    tp.submit(pipeline)
    # we get the resulting pipeline
    pipeline = tp.get(pipeline.id)
    return pipeline

def create_predictions_dataset(state,pipeline):
    print("Updating predictions dataset...")
    predictions,day,nb_predictions,cleaned_data = pipeline.predictions.read(),pipeline.day.read(),pipeline.nb_predictions.read(),pipeline.cleaned_dataset.read()
    
    # we will display 5*nb_predictions elements
    window = 5*nb_predictions
    
    # we create the historical dataset that will be displayed
    new_length = len(cleaned_data[cleaned_data['Date'] < day]) + nb_predictions
    temp_df = cleaned_data[:new_length]
    temp_df = temp_df[-window:].reset_index(drop=True)
    
    # we create the series that will be used in the concat
    historical_values = pd.Series(temp_df['Value'],name="Historical values")
    predicted_values = pd.Series([np.NaN]*len(temp_df), name="Predicted values")
    predicted_values[-len(predictions):] = predictions
    
    # we update the predictions dataset
    state.predictions_dataset = pd.concat([temp_df['Date'],historical_values,predicted_values],axis=1)
    pass

def predict(state):
    print("'Predict' button clicked")
    pipeline = create_and_submit_pipeline()
    create_predictions_dataset(state,pipeline)
    pass

if __name__ == "__main__":
    gui = Gui(page=md_step_4)
    gui.run()
    