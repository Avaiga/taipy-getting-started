from step_12 import *

from sklearn.metrics import mean_absolute_error, mean_squared_error

# Initial dataset for comparison
comparison_scenario = pd.DataFrame({"Cycle Type":[], 'Scenario Name':[],
                                    'RMSE baseline':[], 'MAE baseline':[],
                                    'RMSE ML':[], 'MAE ML':[]})

# boolean to check if the comparison is done
comparison_scenario_done = False

# selector for cycle
cycle_selector = ['original', 'day', 'week', 'month']
selected_cycle = cycle_selector[0]

# selector for metric
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
    
    # We go through all the master scenarios
    for scenario in tp.get_all_masters():
        print("Scenario")
        # We go through all the pipelines
        for pipeline in scenario.pipelines.values():
            print("     Pipeline")
            # We get the predictions dataset with the historical data
            only_prediction_dataset = create_predictions_dataset(pipeline)[-nb_predictions:]
            
            historical_values = only_prediction_dataset['Historical values']
            predicted_value = only_prediction_dataset['Predicted value']
            
            # We calculate the metrics for this pipeline and master scenario
            rmse, mae = caculate_metrics(historical_values, predicted_value)
                        
            if 'baseline' in pipeline.config_id:
                rmses_baseline.append(rmse)
                maes_baseline.append(mae)
            elif 'ml' in pipeline.config_id:
                rmses_ml.append(rmse)
                maes_ml.append(mae)

        cycle_types.append(scenario.group_by.read())
        scenario_names.append(scenario.properties['display_name'])
        
    # We finally update comparison_scenario
    state.comparison_scenario = pd.DataFrame({"Cycle Type":cycle_types,
                                              'Scenario Name':scenario_names,
                                              'RMSE baseline':rmses_baseline,
                                              'MAE baseline':maes_baseline,
                                              'RMSE ML':rmses_ml,
                                              'MAE ML':maes_ml})
    state.comparison_scenario_done = True
    pass




def create_performance_md():
    # This is a function that will create the markdown file for the performance
    md = """
<|Compare masters|button|on_action=compare|>

<|layout|columns=1 1
<|{selected_cycle}|selector|lov={cycle_selector}|>
<|{selected_metric}|selector|lov={metric_selector}|>
|>
"""
    # We go through all the different types of cycle (month, week, day, original)
    for cycle_type in cycle_selector:
        # We create the part that will be rendered if we selected this cycle
        md += "\n<|part|render={selected_cycle=='" + cycle_type + "'}|"
        # We go through all the different metrics (RMSE, MAE)
        for metric in metric_selector:
            # We create the part that will be rendered if we selected this metric
            md += "\n<|part|render={selected_metric=='" + metric + "'}|"
            # We create the graph for this cycle and metric
            md += "\n<|{comparison_scenario[comparison_scenario['Cycle Type']=='" + cycle_type + "']}|chart|type=bar|x=Scenario Name|y[1]=" + metric + " baseline|y[2]=" + metric + " ML|>"
            md += "\n|>"
        md += "\n|>"
    md += '\n'
    return md

# We create the markdown file thanks to the function above
performance_md = create_performance_md()
 
 # We add the performance_md to the menu   
main_md_step_13 = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Cycle Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + data_visualization_md + """|>
<|part|render={page=="Scenario Manager"}|""" + scenario_manager_md + """|>
<|part|render={page=="Cycle Manager"}|""" + tree_md + """|>
<|part|render={page=="Performance"}|""" + performance_md + """|>
"""

if __name__ == '__main__':
    Gui(page=main_md_step_13).run()