Cycles are useful to keep track of KPI over time. The goal of the code below is to compare the primary scenario of every cycle and their pipelines over time.

To achieve this, a new dataframe has to be initialized. It will store the metrics for the `baseline` and `ml` pipeline. Then, a part will use a boolean to show or not the comparison and finally, a selector will change the displayed metrics of the graph.

```python
# Initial dataset for comparison
comparison_scenario = pd.DataFrame({'Scenario Name':[],
                                    'RMSE baseline':[], 'MAE baseline':[],
                                    'RMSE ML':[], 'MAE ML':[]})

# Boolean to check if the comparison is done
comparison_scenario_done = False

# Selector for metric
metric_selector = ['RMSE', 'MAE']
selected_metric = metric_selector[0]
```
First of all, a function has to be created to compare the primary scenarios of all the cycles. `tp.get_official_scenarios()` is the useful function to use for this effect. `compare` goes through all of these scenarios and pipelines and add the metrics in lists. At the end, `state.comparison_scenario` is updated and `comparison_scenario_done` set to `True`.

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def compute_metrics(historical_data, predicted_data):
    rmse = mean_squared_error(historical_data, predicted_data)
    mae = mean_absolute_error(historical_data, predicted_data)
    return rmse, mae

def compare(state):
    print('Comparing...')
    # Initial lists for comparison
    scenario_names = []
    rmses_baseline = []
    maes_baseline = []
    rmses_ml = []
    maes_ml = []
    
    # Go through all the official scenarios
    all_scenarios = tp.get_official_scenarios()
    all_scenarios_ordered = sorted(all_scenarios, key=lambda x: x.creation_date.timestamp()) # delete?
    
    for scenario in all_scenarios_ordered:
        print("Scenario...", scenario.name)
        # Go through all the pipelines
        for pipeline in scenario.pipelines.values():
            print("     Pipeline...", pipeline.config_id)
            # Get the predictions dataset with the historical data
            only_prediction_dataset = create_predictions_dataset(pipeline)[-pipeline.n_predictions.read():]
            
            # Series to compute the metrics (true values and predicted values)
            historical_values = only_prediction_dataset['Historical values']
            predicted_values = only_prediction_dataset['Predicted values']
            
            # Compute the metrics for this pipeline and official scenario
            rmse, mae = compute_metrics(historical_values, predicted_values)
            
            # Add to the correct lists, the correct values    
            if 'baseline' in pipeline.config_id:
                rmses_baseline.append(rmse)
                maes_baseline.append(mae)
            elif 'ml' in pipeline.config_id:
                rmses_ml.append(rmse)
                maes_ml.append(mae)

        scenario_names.append(scenario.name)
        
    # Update comparison_scenario
    state.comparison_scenario = pd.DataFrame({'Scenario Name':scenario_names,
                                              'RMSE baseline':rmses_baseline,
                                              'MAE baseline':maes_baseline,
                                              'RMSE ML':rmses_ml,
                                              'MAE ML':maes_ml})
    
    # When comparison_scenario_done will be set to True,
    # the part with the graphs will be finally rendered
    state.comparison_scenario_done = True
    
```

Let's create a page related to this comparison. As said before, this page will contain a graph to compare scenarios and pipelines and a selector to choose the metric on which to compare. The button at the bottom of the page when pressed calls the `compare` function. When finished, the rest of the page will be shown thanks to the `render` parameter of the *part*.

A new Taipy's block is present in the Markdown: [expandable](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/expandable/).

```python
# Create the performance page
page_performance = """
<|part|render={comparison_scenario_done}|

<|Table|expanded=False|expandable|
<|{comparison_scenario}|table|width=100%|>
|>

<|{selected_metric}|selector|lov={metric_selector}|dropdown=True|>

<|part|render={selected_metric=='RMSE'}|
<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|height=80%|width=100%|>
|>

<|part|render={selected_metric=='MAE'}|
<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|height=80%|width=100%|>
|>

|>

<center>
<|Compare officials|button|on_action=compare|>
</center>
"""
```

<p align="center">
    <img src="/steps/images/page_performance.gif" width=700>
</p>


```python
# Add the page_performance to the menu   
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
<|part|render={page=="Performance"}|""" + page_performance + """|>
"""

Gui(page=multi_pages).run() 
```

<p align="center">
    <img src="/steps/images/step_12_result.png" width=700>
</p>
