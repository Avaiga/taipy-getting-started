After creating our first web client with just one line of text, we want to create a more complicated page.

# Controls (Visual elements)

First, I have to introduce you the concept of 'controls'. A control is a Taipy graphical object that will be displayed on the client. A control can be a slider, a chart, a table, an input, a menu and so on. You can find the list here:?????.

Every control has a similar syntax. It begins with '<|' and ends with with '|>'. Each parameter of a control is seperated by a pipe '|'. For example, you can find the parameters for a slider here:????.

Now that we know how to create a control, we can add them to our page. You can see in the code below how to display the value of a variable and a slider control. We also need a dataset to create our first chart.

# Data

The data that will be displayed is a real dataset. It means that for certain days we will not have any information. The chart control is interactive, you can zoom in and out to explore your dataset and navigate in your data with the table control.

[CODE]
