from step_12 import *

from sklearn.metrics import mean_absolute_error, mean_squared_error

comparison_scenario = pd.DataFrame({"Cycle Type":[], 'Scenario Name':[], 'Pipeline':[], 'RMSE':[], 'MAE':[]})

comparison_scenario_done = False

def compare(state):
    print('Comparing...')
    cycle_types = []
    scenario_names = []
    pipelines = []
    rmses = []
    maes = []
    for scenario in tp.get_all_masters():
        print("Scenario")
        for pipeline in scenario.pipelines.values():
            print("     Pipeline")
            predictions = pipeline.predictions.read()
            day = pipeline.day.read()
            nb_predictions = pipeline.nb_predictions.read()
            cleaned_data = pipeline.cleaned_dataset.read()
            
            # We create the historical dataset that will be displayed
            new_length = len(cleaned_data[cleaned_data['Date'] < day]) + nb_predictions
            temp_df = cleaned_data[:new_length]
            historical_values = temp_df[-nb_predictions:]
                        
            rmse, mae = caculate_metrics(historical_values['Value'], predictions)
            
            name = f"Scenario {day} - {nb_predictions} predictions - type {scenario.group_by.read()}"
            
            cycle_types.append(scenario.group_by.read())
            scenario_names.append(name)
            pipelines.append(pipeline.config_id)
            rmses.append(rmse)
            maes.append(mae)
            
        
    state.comparison_scenario = pd.DataFrame({"Cycle Type":cycle_types,
                                              'Scenario Name':scenario_names,
                                              'Pipeline':pipelines,
                                              'RMSE':rmses,
                                              'MAE':maes})
    state.comparison_scenario_done = True    
    pass

def caculate_metrics(historical_data, predicted_data):
    rmse = mean_squared_error(historical_data, predicted_data)
    mae = mean_absolute_error(historical_data, predicted_data)
    return rmse, mae

performance_md = """
<|Compare masters|button|on_action=compare|>

<|{comparison_scenario}|table|>

<|{comparison_scenario[comparison_scenario['Cycle Type']=='original']}|chart|type=bar|x=Scenario Name|y=MAE|>
<|{comparison_scenario[comparison_scenario['Cycle Type']=='original']}|chart|type=bar|x=Scenario Name|y=RMSE|>

<|{comparison_scenario[comparison_scenario['Cycle Type']=='day']}|chart|type=bar|x=Scenario Name|y=MAE|>
<|{comparison_scenario[comparison_scenario['Cycle Type']=='day']}|chart|type=bar|x=Scenario Name|y=RMSE|>

<|{comparison_scenario[comparison_scenario['Cycle Type']=='week']}|chart|type=bar|x=Scenario Name|y=MAE|>
<|{comparison_scenario[comparison_scenario['Cycle Type']=='week']}|chart|type=bar|x=Scenario Name|y=RMSE|>

<|{comparison_scenario[comparison_scenario['Cycle Type']=='month']}|chart|type=bar|x=Scenario Name|y=MAE|>
<|{comparison_scenario[comparison_scenario['Cycle Type']=='month']}|chart|type=bar|x=Scenario Name|y=RMSE|>
"""

main_md_step_13 = main_md_step_11 = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager", "Cycle Manager", "Performance"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + data_visualization_md + """|>
<|part|render={page=="Scenario Manager"}|""" + scenario_manager_md + """|>
<|part|render={page=="Cycle Manager"}|""" + tree_md + """|>
<|part|render={page=="Performance"}|""" + performance_md + """|>
"""

if __name__ == '__main__':
    Gui(page=main_md_step_13).run()