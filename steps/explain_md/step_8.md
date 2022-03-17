We have created our GUI to show a scenario. However, we had some input variables that we didn't change so far: the number of predictions, the group_by and the day. It will be great if we could interact in real time with these parameters, change them and rerun our scenario. It is something that can easily be done with the 'write' function of datanodes. We are going to create control to change these values and we will run our scenario by clicking on a 'Change scenario' button.

## The submit is called in two different ways:
## 1. when we create our first scenario, here state is None
## 2. when the user clicks on the submit button, here state is the state of the app