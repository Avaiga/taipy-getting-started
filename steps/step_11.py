from step_10 import *

from taipy import Frequency

scenario_dayly_cfg = tp.configure_scenario(name="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.DAILY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

scenario_weekly_cfg = tp.configure_scenario(name="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.WEEKLY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

scenario_montly_cfg = tp.configure_scenario(name="scenario",
                                     pipeline_configs=[pipeline_baseline_cfg, pipeline_ml_cfg],
                                     frequency=Frequency.MONTHLY)# We want to create scenarios each day and compare them
# Frequency will create a Cycle object, it will be used much later in the code to navigate through the scenarios

tree = ["Monthly", "Weekly", "Daily"]

# We change the create_scenario function in order to change the default parameters
# and to be able to create multiple scenarios
def create_scenario(state):
    print("Execution of scenario...")
    # We create a scenario
    day = dt.datetime(state.day.year, state.day.month, state.day.day)
    
    if state.group_by == "month":
        scenario = tp.create_scenario(scenario_montly_cfg, creation_date=day)
    elif state.group_by == "week":
        scenario = tp.create_scenario(scenario_weekly_cfg, creation_date=day)
    else:
        scenario = tp.create_scenario(scenario_dayly_cfg, creation_date=day)
    
    update_tree(state, scenario)

    # We put the new scenario as the current selected_scenario
    state.selected_scenario = scenario.id
    # Change the scenario that is currently selected
    scenario = submit_scenario(state)
    return scenario  

def update_tree(state,scenario):
    state.tree["e"]=1
    pass


tree_dict={
  "Monthly": {
    #"California": ["Sacramento", "Los Angeles"],
    #"Texas": ["Austin", "Houston"],
    #"Florida": ["Tallahassee", "Jacksonville"]
  },
  "Weekly": {
    #"Guangdong": ["Guangzhou", "Shaoguan"],
    #"Shandong": ["Jinan", "Qingdao"],
    #"Henan": ["Zhengzhou", "Pingdingshan"]
  },
  "Daily": {
    #"Moscow": ["Balashikha", "Khimki"],
    #"Kemerovo": ["Novokuznetsk", "Tayga"],
    #"Nizhny Novgorod": ["Navashino", "Pervomaysk"]
  },
}

items = []
frequency_counter  = 0
period_counter = 0
scenario_counter     = 0
def build_tree(state,scenario,name):
    if state.group_by == "month":
        period = f"Month {state.day.month}"
    if state.group_by == "week":
        period = f"Week {state.day.week()}"
    else:
        period = f"Week {state.day.strftime('%A, %d %b %Y')}"
        
    
    try:
        tree_dict[state.group_by][period] += [(scenario.id,name)]
    except:
        tree_dict[state.group_by][period] = [(scenario.id,name)]
        
    for frequencies, periods in tree_dict.items():
        def build_period(periods):
            period_array = []

            def build_scenario(scenarios):
                global scenario_counter
                scenario_array = []
                for scenario in scenarios:
                    scenario_tuple = (str(scenario[0]), scenario[1], None)
                    scenario_array.append(scenario_tuple)
                return scenario_array

            for period, scenario in periods.items():
                global period_counter
                period_tuple = (f"P{period_counter}", period, build_scenario(scenario))
                period_counter += 1
                period_array.append(period_tuple)
                return period_array

    frequency_tuple = (f"C{frequency_counter}", frequencies, build_period(periods))
    frequency_counter += 1
    items.append(frequency_tuple)

from taipy.gui import Gui

selected = None

page_tree = """
<|{selected}|tree|lov={items}|>
The value of tree is: <|{selected}|>
"""

if __name__ == '__main__':
    gui = Gui(page=page_tree)
    gui.run()