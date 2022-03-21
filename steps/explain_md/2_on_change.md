Great! Now, the page has a lot of visual elements. The slider is interactive and is changing the value of our 'value' variable. Everything is managed by Taipy. However, in some cases, we want to connect manually this value to other variables. For example, if to create a chart that will only display one week of data, a connection has to be created between the value of the slider and the data.

# state

What is the state of the application? The state of the application is the current state of the variables so the values of all the variables. In the beginning, state.value = 10 and state.data is the dataset for the 10th week. To manipulate variables in the GUI, we pass through the state.

# How to connect two variables - the *on_change* function

The 'on_change' function is called whenever the value of a variable changes in the GUI. Taipy will look if you created a function with this name in your code and use it. It is a *callback* function and its parameter are state (the state of the variables), the variable name that has been changed and its value. In our example, it is called whenever the value of the slider changes with the state, 'value' and the current value of the slider. Each time it changes, data will be updated accordingly. Then, Taipy will update automatically the associated chart.

[CODE]