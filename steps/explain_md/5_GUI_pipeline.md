# Building the GUI and buttons

Let's update your GUI to display the results of your pipeline. You create a "Predict" button that will create and run it. the function in the *on_action* parameter will be called whenever the button is pressed.

<|Text displayed on button|button|on_action=fct_name_called_when_pressed|>

The results is then displayed in the chart by updating it. A good option would have been to directly create the results in the piepline before. It is typically the good practice to put all complexicity of a pipeline in it.

[CODE]