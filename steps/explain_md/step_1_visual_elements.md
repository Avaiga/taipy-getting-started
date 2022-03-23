# Data

The data used in the following codes will be retrieved this way.

```python
import pandas as pd

def get_data(path_to_csv: str):
    # "pd.read_csv()" function returns a dataframe
    dataset = pd.read_csv(path_to_csv)
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    return dataset

# Get the dataframe
path_to_csv = "dataset.csv"
dataset = get_data(path_to_csv)

...
```

`dataset` is a `pd.DataFrame`, a basic *Python* object representing a real time series. Because of that, there will be no information for specific days. The columns are Index, Date, and Value.
- Index is a unique identifier for each data point.
- Date is the date of the data point.
- Value is its value.
After creating your first web client with just one line of code and reading your data with this code, let's create a more detailed page.


# Visual elements

First, I have to introduce you to the concept of '[Visual elements](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/)'.  A visual element is a Taipy graphical object displayed on the client. A visual element can be a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/), a [chart](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/chart/), a [table](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/table/), an [input](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/input/), a [menu](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/menu/), etc. Check the list [here](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/controls/).

Every visual element has a similar syntax.`<|{desired_variable}|visual_elements_name|param_1=param_1|param_2=param_2| ... |>` To add it on a page, write this syntax wherever you want in your string representing your page.
For example, a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/) is written this way :`<|{variable}|slider|min=min_value|max=mx_value|>`(min and max are optional).

The first part of the page will show the value of a Python variable and a slider with this syntax.
```
*<|{n_week}|>*
<|{n_week}|slider|min=1|max=52|>
```
The second half will create a chart and a table.
```
<|{dataset}|chart|type=bar|x=Date|y=Value|height=100%|>
<|{dataset}|table|height=400px|width=95%|>
```

Here is the code combined:

```python
...

from taipy.gui import Gui

dataset = get_data(path_to_csv)

# Initial value of n_week
n_week = 10

# Definition of the page
page = """
# Getting started with Taipy

Week number: *<|{n_week}|>*

Interact with this slider to change the week number:
<|{n_week}|slider|min=1|max=52|>

## Full dataset:

<|{dataset}|chart|type=bar|x=Date|y=Value|height=100%|>

<|{dataset}|table|height=400px|width=95%|>
"""

# Create a Gui object with our String
Gui(page=page).run()
```
<img src="/steps/images/step_1_result.png" />