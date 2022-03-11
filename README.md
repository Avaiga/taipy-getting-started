# taipy-getting-started
Packages nedded: taipy (0.13), pandas, numpy, statsmodels, scikit-learn.

Make sure to have the good path for the csv. This path could change depending on how you run the scripts.

## Step 0

The minimum code to run the gui.

## Step 1

Presentation of the interactiveness of Taipy as well as different controls (slider and chart).

## Step 2

Introduction to the on_change function with the choice of the week. The week displayed on the graph is the week of the slider.

## Step 3

Creation of the backend configuration for a baseline model. The predictions of this model is just the historical data with a shift in time.

## Step 4


Add to the previous config, a pipeline config. Then, creation and execution of the pipeline without the gui. 

## Step 5

Add the execution of the pipeline thanks to a "Predict" button on the Gui (first button). The default parameters are used to run the pipeline. The results are shown in a chart.

## Step 6

Creation of a second pipeline (the machine learning pipeline : Auto-Regressive model). Creation and execution of the scenario with the default parameters wihout the gui.

### Step 7

Scenario is being runned and we can change the selected pipeline through a selector (first selector) and a button.

## Step 8

A first scenario is created. We can change the default parameters with controls (date, number, selector) of this scenario; the default parameters are the date, the number of predictions and how to group-by the data. A 'change_scenario' button is pressed to apply these changes and re-submit the scenario.

## Step 9

Now, we want to show how to create scenarios directly through the gui and keep track of them.

## Step 10

Organize the page with a menu, layouts and parts that can be not rendered.

## Step 11

Introduce the concepts of Cycle and masters. We can delete a scenario and we can make a scenario master.

## Step 12

Create a 'Cycle Manager' page dedicated to cycles. It is another way to present the scenarios in a tree and how to update this tree.

## Step 13

Create a 'Performance' page that will compare all the master scenarios of the same group-by and display metrics of these scenarios.
