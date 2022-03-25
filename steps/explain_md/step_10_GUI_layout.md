With these few steps, you have created a full-AI application on which you can predict multiples days with different parameters. However, as you can see the layout of the page is not optimal. It could be greatly improved. This is the role of the code below.
To get a more aesthetically pleasing page, three useful controls to use are:
- [menu](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/menu/): creates a menu on the left to navigate through the pages.
`<|menu|label=Menu|lov={lov_pages}|on_action=menu_fct_called|>`. For example, this code creates a menu with two pages:

```python
from taipy.gui import Gui

Gui("<|menu|label=Menu|lov={['Data Visualization', 'Scenario Manager']}|>").run()
```

<p align="center">
    <img src="/steps/images/menu.png" width=50>
</p>


- [part](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/part/): is used to create a group of text/visual elements. A useful parameter of *part* is `render`. Set to `False`, it will not display the part.

```
<|part|render={bool_variable}|
Text
Or visual elements...
|>
```

- [layout](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/layout/): creates invisible columns where you can put your texts and visual elements. Columns parameter will indicate the width and number of columns. Here, we have three columns of the same width.
```
<|layout|columns=1 1 1|
Button in first column <|Press|button|>

Second column

Third column
|>
```

<p align="center">
    <img src="/steps/images/layout.png" width=500>
</p>

Here, the part with the chart will be displayed when the first scenario will be created. A menu renders or not a part depending on the 'page' variable. This is how you can create easily multiple pages; there are a lot of other ways to do so.


My first page in the menu contains the chart with dataset focused on one week and the slider related to change the week. This is the page created in one of the first code.

```python
...

# Our first page will be page
# so the page with the slider and the chart that display a week of the historical data
page_data_visualization = page
```

<p align="center">
    <img src="/steps/images/data_visualization.png" width=700>
</p>


```python

# Second page: page to create scenarios and display its results
page_scenario_manager = """
# Create your scenario

<|layout|columns=1 1 1 1|
<|
**Prediction date**\n\n <|{day}|date|with_time=False|>
|>

<|
**Max capacity**\n\n <|{max_capacity}|number|>
|>

<|
**Number of predictions**\n\n<|{n_predictions}|number|>
|>

<|
<br/>\n <|Create new scenario|button|on_action=create_scenario|>
|>
|>

<|part|render={len(scenario_selector) > 0}|
<|layout|columns=1 1|
<|
## Scenario \n <|{selected_scenario}|selector|lov={scenario_selector}|dropdown=True|>
|>

<|
## Display the pipeline \n <|{selected_pipeline}|selector|lov={pipeline_selector}|dropdown=True|>
|>
|>

<|{predictions_dataset}|chart|type=bar|x=Date|y[1]=Historical values|y[2]=Predicted values|height=80%|width=100%|>
|>
"""
```

<p align="center">
    <img src="/steps/images/scenario_manager.gif" width=700>
</p>

The menu combines these two pages. When a page will be selected, `menu_fct` will be called and update the page.

```python
# Create a menu with our pages
multi_pages = """
<|menu|label=Menu|lov={["Data Visualization", "Scenario Manager"]}|on_action=menu_fct|>

<|part|render={page=="Data Visualization"}|""" + page_data_visualization + """|>
<|part|render={page=="Scenario Manager"}|""" + page_scenario_manager + """|>
"""


# The initial page is the "Scenario Manager" page
page = "Data Visualization"
def menu_fct(state, var_name: str, fct: str, var_value: list):
    # Change the value of the state.page variable in order to render the correct page
    state.page = var_value['args'][0]

Gui(page=multi_pages).run()
```

<p align="center">
    <img src="/steps/images/multi_pages.png" width=700>
</p>
