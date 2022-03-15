from step_12 import *

from sklearn.metrics import mean_absolute_error, mean_squared_error

# Initial dataset for comparison
comparison_scenario = pd.DataFrame({"Cycle Type":[], 'Scenario Name':[],
                                    'RMSE baseline':[], 'MAE baseline':[],
                                    'RMSE ML':[], 'MAE ML':[]})

# Boolean to check if the comparison is done
comparison_scenario_done = False

# Selector for cycle
cycle_selector = ['original', 'day', 'week', 'month']
selected_cycle = cycle_selector[0]

# Selector for metric
metric_selector = ['RMSE', 'MAE']
selected_metric = metric_selector[0]


def caculate_metrics(historical_data, predicted_data):
    rmse = mean_squared_error(historical_data, predicted_data)
    mae = mean_absolute_error(historical_data, predicted_data)
    return rmse, mae

def compare(state):
    print('Comparing...')
    # Initial lists for comparison
    cycle_types = []
    scenario_names = []
    rmses_baseline = []
    maes_baseline = []
    rmses_ml = []
    maes_ml = []
    
    # Go through all the master scenarios
    for scenario in tp.get_all_masters():
        print("Scenario...", scenario.properties['display_name'])
        # Go through all the pipelines
        for pipeline in scenario.pipelines.values():
            print("     Pipeline...", pipeline.config_id)
            # Get the predictions dataset with the historical data
            only_prediction_dataset = create_predictions_dataset(pipeline)[-pipeline.nb_predictions.read():]
            
            historical_values = only_prediction_dataset['Historical values']
            predicted_values = only_prediction_dataset['Predicted values']
            
            # Calculate the metrics for this pipeline and master scenario
            rmse, mae = caculate_metrics(historical_values, predicted_values)
            
            # Add to the correct lists, the correct values    
            if 'baseline' in pipeline.config_id:
                rmses_baseline.append(rmse)
                maes_baseline.append(mae)
            elif 'ml' in pipeline.config_id:
                rmses_ml.append(rmse)
                maes_ml.append(mae)

        cycle_types.append(scenario.group_by.read())
        scenario_names.append(scenario.properties['display_name'])
        
    # Update comparison_scenario
    state.comparison_scenario = pd.DataFrame({"Cycle Type":cycle_types,
                                              'Scenario Name':scenario_names,
                                              'RMSE baseline':rmses_baseline,
                                              'MAE baseline':maes_baseline,
                                              'RMSE ML':rmses_ml,
                                              'MAE ML':maes_ml})
    
    # When comparison_scenario will be set to True,
    # the part with the graphs will be finally rendered
    state.comparison_scenario_done = True
    pass



def create_performance_md():
    # This is a function that will create the markdown file for the performance
    md = """
<|part|render={comparison_scenario_done}|

<|Table|expanded=False|expandable|
<|{comparison_scenario}|table|width=100%|>
|>

<|layout|columns=1 1|
<|{selected_cycle}|selector|lov={cycle_selector}|dropdown=True|>

<|{selected_metric}|selector|lov={metric_selector}|dropdown=True|>
|>

"""
    # Go through all the different types of cycle (month, week, day, original)
    for cycle_type in cycle_selector:
        # Create the part that will be rendered if we selected this cycle
        md += "\n<|part|render={selected_cycle=='" + cycle_type + "'}|"
        # Go through all the different metrics (RMSE, MAE)
        for metric in metric_selector:
            # Create the part that will be rendered if we selected this metric
            md += "\n<|part|render={selected_metric=='" + metric + "'}|"
            
            # Create the graph for this cycle and metric
            data = "comparison_scenario[comparison_scenario['Cycle Type']=='" + cycle_type + "']"
            
            md += "\n<|{" + data + "}|chart|type=bar|x=Scenario Name|y[1]=" + metric + " baseline|y[2]=" + metric + " ML|height=80%|width=100%|>"
            
            md += "\n|>"
        md += "\n|>"
    md += '\n|>\n'
    md += """
<center>    
<|Compare masters|button|on_action=compare|>
</center>
"""
    return md

# Create the markdown file thanks to the function above
page_performance = create_performance_md()
 
 # Add the performance_md to the menu   
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Cycle Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
<|part|render={page=="Cycle Manager"}|""" + page_cycle_manager + """|>
<|part|render={page=="Performance"}|""" + page_performance + """|>
"""

if __name__ == '__main__':
    Gui(page=multi_pages).run()