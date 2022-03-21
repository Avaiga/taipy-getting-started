# Building the GUI and buttons

Let's update our GUI to display the results of our pipeline. We create a "Predict" button that will create and run it. the function in the *on_action* parameter will be called whenever the button is pressed. See the button doc here.
The results is then displayed in the chart by updating it. If we were really smart about it, we could even have created the prediction dataset directly in the Scnenario Management. It is typically the good practice to put all complexicity of a pipeline in it.

[CODE]