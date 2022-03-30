# taipy-getting-started

**Packages needed**: *taipy (0.13), statsmodels, scikit-learn*.

The code for all the steps is stored in `src/`. For more information, on the steps, read the README.md file in their respective folder (`step_xx/README.md`) that explains the step in detail.

## Step 00

The presentation of Taipy and the minimum code to run the gui.

## Step 01

Presentation of the interactiveness of Taipy as well as different controls (slider and chart).

## Step 02

Introduction to the on_change function with the choice of the week. The week displayed on the graph is the week of the slider.

## Step 03

Introduction to Taipy Core. Creation of the configuration for a baseline model.

## Step 04

Add to the previous config, a pipeline config to create and execute the pipeline without the GUI. 

## Step 05

Add the execution of the pipeline thanks to a "Predict" button on the Gui (first button). The default parameters are used to run the pipeline. The results are shown in a chart.

## Step 06

Creation of a second pipeline (the machine learning pipeline : Auto-Regressive model). Creation and execution of the scenario with the default parameters wihout the GUI.

## Step 07

Scenario is being runned at the beginning and we can change the selected pipeline through a selector (first selector) and a button.

## Step 08

A first scenario is created. We can change the default parameters of this scenario with controls (date, number, selector); the default parameters are the date, the number of predictions and max capacity. A 'change_scenario' button is pressed to apply these changes and re-submit the scenario.

## Step 09

Now, we want to show how to create scenarios directly through the gui and keep track of them.

## Step 10

Organize the page with a menu, layouts and parts that can be not rendered.

## Step 11

Introduce the concepts of Cycles and primary scenarios. Deletion of a scenario and setting a scenario, primary.

## Step 12

Create a 'Performance' page that will compare all the primary scenarios and display metrics of these scenarios.
