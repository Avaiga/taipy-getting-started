After creating our first web client with just one line of text, we want to create a more complicated page.

# Visual elements

First, I have to introduce you the concept of 'controls'. A control is a Taipy graphical object that will be displayed on the client. A control can be a slider, a chart, a table, an input, a menu and so on. You can find the list here:?????.

Every visual element has a similar syntax. <|{desired_variable}|visual_elements_name|param_1=param_1|param_1=param_1| ... |>
For example, a slider is written this way : <|{variable}|slider|min=min_value|max=mx_value|> (min and max are optional).

The first part of the page shows the value of a Python variable and a slider. You can also create charts and tables.

# Data

The data represents a real time serie. It means that for certain days we will not have any information. It is composed of these Index,Date,Value. The Index is a unique identifier for each data point. The Date is the date of the data point. The Value is the value of the data point.

"""The chart control is interactive, you can zoom in and out to explore your dataset and navigate in your data with the table control."""

[CODE]
