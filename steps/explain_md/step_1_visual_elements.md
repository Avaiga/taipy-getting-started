## Data

The data used in the following codes will be retrieved this way.

```python
import pandas as pd

def get_data(path_to_csv: str):
    # pandas.read_csv() returns a pd.DataFrame
    dataset = pd.read_csv(path_to_csv)
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    return dataset

# Read the dataframe
path_to_csv = "dataset.csv"
dataset = get_data(path_to_csv)

...
```

`dataset` is a `pd.DataFrame`, a basic *Python* object representing, in this case, a real time series. Because of that, there will be no information for specific days. The columns are:
- Index: a unique identifier for each data point.
- Date: the date of the data point.
- Value: its value.

<p align="center">
    <img src="/steps/images/table.png" width=500>
</p>

After creating your first web client with just one line of code and reading your data with this code, let's create a more detailed page with visual elements.

# Visual elements

Taipy GUI can be considered as an **augmented** Markdown; it adds the concept of **'[Visual elements](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/)'** on top of all the Markdown syntax.  A visual element is a Taipy graphical object displayed on the client. It can be a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/), a [chart](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/chart/), a [table](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/table/), an [input](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/input/), a [menu](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/menu/), etc. Check the list [here](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/controls/).

Every visual element has a similar syntax.`<|{variable}|visual_element_name|param_1=param_1|param_2=param_2| ... |>`. For example, a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/) is written this way :`<|{variable}|slider|min=min_value|max=max_value|>`.
To add it on a page, write this syntax wherever you want in your string representing your page.

The first part of the new string will show the value of a *Python* variable and a slider with this syntax.
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

from taipy import Gui

dataset = get_data(path_to_csv)

# Initial value
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

# Create a Gui object with our page content
Gui(page=page).run()
```

<p align="center">
    <img src="/steps/images/step_1_result.gif" width=700>
</p>
