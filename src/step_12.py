from step_11 import *

from sklearn.metrics import mean_absolute_error, mean_squared_error

# Initial dataset for comparison
comparison_scenario = pd.DataFrame(columns=["Scenario Name",
                                            "RMSE baseline",
                                            "MAE baseline",
                                            "RMSE ML",
                                            "MAE ML"])


# Selector for metrics
metric_selector = ["RMSE", "MAE"]
selected_metric = metric_selector[0]


def compute_metrics(historical_data, predicted_data):
    rmse = mean_squared_error(historical_data, predicted_data)
    mae = mean_absolute_error(historical_data, predicted_data)
    return rmse, mae


def compare(state):
    print("Comparing...")
    # Initial lists for comparison
    scenario_names = []
    rmses_baseline = []
    maes_baseline = []
    rmses_ml = []
    maes_ml = []

    # Go through all the primary scenarios
    all_scenarios = tp.get_primary_scenarios()
    all_scenarios_ordered = sorted(all_scenarios, key=lambda x: x.creation_date.timestamp())

    for scenario in all_scenarios_ordered:
        print(f"Scenario {scenario.name}")
        # Go through all the pipelines
        for pipeline in scenario.pipelines.values():
            print(f"     Pipeline {pipeline.config_id}")
            # Get the predictions dataset with the historical data
            only_prediction_dataset = create_predictions_dataset(pipeline)[-pipeline.n_predictions.read():]

            # Series to compute the metrics (true values and predicted values)
            historical_values = only_prediction_dataset["Historical values"]
            predicted_values = only_prediction_dataset["Predicted values"]

            # Compute the metrics for this pipeline and primary scenario
            rmse, mae = compute_metrics(historical_values, predicted_values)

            # Add values to the appropriate lists
            if "baseline" in pipeline.config_id:
                rmses_baseline.append(rmse)
                maes_baseline.append(mae)
            elif "ml" in pipeline.config_id:
                rmses_ml.append(rmse)
                maes_ml.append(mae)

        scenario_names.append(scenario.creation_date.strftime("%A %d %b"))

    # Update comparison_scenario
    state.comparison_scenario = pd.DataFrame({"Scenario Name": scenario_names,
                                              "RMSE baseline": rmses_baseline,
                                              "MAE baseline": maes_baseline,
                                              "RMSE ML": rmses_ml,
                                              "MAE ML": maes_ml})



# Performance page
page_performance = """
<|part|render={len(comparison_scenario)>0}|

<|Table|expanded=False|expandable|
<|{comparison_scenario}|table|width=100%|>
|>

<|{selected_metric}|selector|lov={metric_selector}|dropdown|>

<|part|render={selected_metric=="RMSE"}|
<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|>
|>

<|part|render={selected_metric=="MAE"}|
<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|>
|>
|>


<center><|Compare primarys|button|on_action=compare|></center>
"""


lov_menu = [("Data-Visualization", "Data Visualization"),
            ("Scenario-Manager", "Scenario Manager"),
            ("Performance", "Performance")]

# Create a menu with our pages
root_md = "<|menu|label=Menu|lov={lov_menu}|on_action=menu_fct|>"

pages = {"/":root_md,
         "Data-Visualization":page_data_visualization,
         "Scenario-Manager":page_scenario_manager,
         "Performance":page_performance}


def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    navigate(state, var_value["args"][0])
    
if __name__ == "__main__":
    tp.Core().run()
    scenario_selector = tp.get_scenarios()
    selected_scenario = None
    Gui(pages=pages).run(dark_mode=False, port=5001)
