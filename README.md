# taipy-getting-started
The repo with the Getting Started scripts

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
### Step 4 - backend

Add to the previous config, a pipeline config. Then, creation and execution of the pipeline without the gui. 

### Step 4 - gui

Add the execution of the pipeline thanks to a "Predict" button on the Gui (first button). The default parameters are used to run the pipeline. The results are shown in a chart.

## Step 5
### Step 5 - backend

Creation of a second pipeline (the machine learning pipeline : Auto-Regressive model). Creation and execution of the scenario with the default parameters wihout the gui.

### Step 5 - gui

Scenario is being runned and we can change the selected pipeline through a selector (first selector) and a button.

## Step 6

Now, we want to show how to create and change scenarios directly through the gui. We can change the default parameters with controls (date, number, selector); the default parameters are the date, the number of predictions and how to group-by the data. This part can be a huge step from step 5 gui.

## Step 7

Organize the page with a menu, layouts and parts that can be not rendered.
