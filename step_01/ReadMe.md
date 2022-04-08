> You can download the final code of this step [here](../src/step_01.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

# Step 1: Visual elements

Many visual elements can be added to the basic code viewed in Step 0. This Step shows how to use visual elements like charts, sliders and tables and implement them in the GUI.

## Importing the Dataset

Suppose that you have a [`dataset.csv`](dataset.csv) file, using the *Pandas* library, you can retrieve this dataset with the following codes:

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

![Table](table.png){ width=700 style="margin:auto;display:block" }

After creating your first web client with just one line of code and reading your data with this code, let's create a more detailed page with visual elements.

## Visual elements

Taipy GUI can be considered as an **augmented** Markdown; it adds the concept of **'[Visual elements](https://docs.taipy.io/manuals/gui/viselements/)'** on top of all the Markdown syntax.  A visual element is a Taipy graphical object displayed on the client. It can be a [slider](https://docs.taipy.io/manuals/gui/viselements/slider/), a [chart](https://docs.taipy.io/manuals/gui/viselements/chart/), a [table](https://docs.taipy.io/manuals/gui/viselements/table/), an [input](https://docs.taipy.io/manuals/gui/viselements/input/), a [menu](https://docs.taipy.io/manuals/gui/viselements/menu/), etc. Check the list [here](https://docs.taipy.io/manuals/gui/controls/).

Every visual element has a similar syntax.`<|{variable}|visual_element_name|param_1=param_1|param_2=param_2| ... |>`. For example, a [slider](https://docs.taipy.io/manuals/gui/viselements/slider/) is written this way :`<|{variable}|slider|min=min_value|max=max_value|>`.
To add it to a page, write this syntax wherever you want in your string representing your Page.

For the first half of the Page, a variable **n_week** and add a slider to modify its value will be created; here is the overall syntax:
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

## Dataset:

Display the last three months of data:
<|{dataset[9000:]}|chart|type=bar|x=Date|y=Value|height=100%|>

<|{dataset}|table|height=400px|width=95%|>
"""

# Create a Gui object with our page content
Gui(page=page).run()
```

![Visual Elements](result.gif){ width=700 style="margin:auto;display:block" }
