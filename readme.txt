
<|Compare masters|button|on_action=compare|>
<|{comparison_scenario}|table|>
<|{selected_cycle}|selector|lov={cycle_selector}|>
<|{selected_metric}|selector|lov={metric_selector}|>

<|part|render={selected_cycle=='original'}|
<|part|render={selected_metric=='RMSE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='original']}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|>
|>
<|part|render={selected_metric=='MAE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='original']}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|>
|>
|>
<|part|render={selected_cycle=='day'}|
<|part|render={selected_metric=='RMSE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='day']}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|>
|>
<|part|render={selected_metric=='MAE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='day']}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|>
|>
|>
<|part|render={selected_cycle=='week'}|
<|part|render={selected_metric=='RMSE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='week']}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|>
|>
<|part|render={selected_metric=='MAE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='week']}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|>
|>
|>
<|part|render={selected_cycle=='month'}|
<|part|render={selected_metric=='RMSE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='month']}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|>
|>
<|part|render={selected_metric=='MAE'}|
<|{comparison_scenario[comparison_scenario['Cycle Type']=='month']}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|>
|>
|>