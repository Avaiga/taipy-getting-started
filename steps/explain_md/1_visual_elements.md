After creating your first web client with just one line of code, let's create a more complicated page.

# [Visual elements](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/)

First, I have to introduce you the concept of ['Visual elements'](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/). A visual element is a Taipy graphical object that will be displayed on the client. A visual element can be a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/), a [chart](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/chart/), a [table](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/table/), an [input](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/input/), a [menu](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/menu/) and so on. Check the list [here](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/controls/).

Every visual element has a similar syntax. <|{desired_variable}|visual_elements_name|param_1=param_1|param_1=param_1| ... |>
For example, a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/) is written this way :
<|{variable}|slider|min=min_value|max=mx_value|> (min and max are optional).

The first part of the page shows the value of a Python variable and a [slider](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/slider/). You can also create [charts](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/charts/) and [tables](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/gui/viselements/table/).

# Data

The data represents a real time serie. It means that for certain days we will not have any information. It is composed of these Index,Date,Value. The Index is a unique identifier for each data point. The Date is the date of the data point. The Value is the value of the data point.

"""The chart control is interactive, you can zoom in and out to explore your dataset and navigate in your data with the table control."""

[CODE]
