You already know the basics of the Taipy Graphical User Interface. Let's go to the Scenario Management aspect of Taipy.

You want to use Taipy to efficiently and easily manage your data wether it is datasets, objects or KPIs. It helps you tracking your KPIs over time....

To understand the Scenario Management aspect of Taipy, there are just 4 concepts to understand.

## Four basic concepts in Taipy Core:
- **Datanodes**: are the translation of variables in Taipy. They are objects that will point to your data whatever it is (pickle, csv, json, etc.). Thery are able to read and write data.
- **Tasks**: are translation of functions in Taipy.
- **Pipelines**: are a list of tasks that will be executed with a smart scheduling automatically created by Taipy. They usually represent series of tasks for different algorithms like a baseline or machine algorithm.
- **Scenarios**: are your business problem with some parameters. They usually consist of one or multiple pipelines.


Firstly, the goal is to create a Directed Acyclic Graph (DAG) that represents a scenario so our problem. Here, we will just create a single pipeline that will take the initial dataset, clean it and give predictions.

<img src="/steps/images/baseline_pipeline.svg"/>

We are going to describe this graph by configuring datanodes (variables) and tasks (functions). Nothing will be executed, it is just a setup to create the DAG.

# Datanodes

Anykind of serializable object can be used as a datanode: int, string, dict, list, np.array, pd.DataFrame, models etc...

Let me introduce some concepts for datanodes :
- **Storage_type**: There are multiple storage types. You can read csv file, SQL database, pickle file, etc.
            Here, we are going to create a csv datanode to read/store the initial dataset. Taipy will know how to access it thanks to the path.

- **Scope**: You can find in the code below two types of Scope: the Pipeline and Scenario scope. 
            Basically, With Scenario scope, datanodes are shared between all the pipelines of the scenario. A pipeline can call a datanode that is not created by itself but by another pipeline.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, I will have one 'predictions' datanode for each pipeline. So, if I add pipelines/algorithms, predictions will be all stored in different "predictions" datanodes.

- **Cacheable**: It is a parameter used for more performance. If the datanode has already been created and the inputs didn't    change. It is not necessary to run it again.


## Input datanodes

- *initial_dataset* is simply the initial csv file. We put some parameters to be able to read this data like *path* and *header*. 

- *day* is the beginning of the predictions. The default value is 26th of July. It means my training data will end before 26th of July and my predictions will begin on this day.

- *nb_predictions* is the number of predictions we want to make while predicting. The default value is 40. We want to have a *prediction* datanode for each algorithm. This is why we specify **Scope.PIPELINE**. 

- *max_capacity* is the maximum value that can take a prediction; it is the seiling of predictions problem. The default value is 200.

[CODE]
```python
## Input datanodes
initial_dataset_cfg = tp.configure_data_node(id="initial_dataset",
                                             storage_type="csv",
                                             path=path_to_csv)

nb_predictions_cfg = tp.configure_data_node(id="nb_predictions", default_data=40)

max_capacity_cfg = tp.configure_data_node(id="max_capacity", default_data=200)

day_cfg = tp.configure_data_node(id="day", default_data=dt.datetime(2021, 7, 26))
```


## Remaining datanodes

- *cleaned_dataset* is the dataset after cleaning (after the *clean_data* function).

- *predictions* is the predictions of the model. Here, it is the return of my *predict_baseline* function.

[CODE]
```python
## Remaining datanodes
cleaned_dataset_cfg = tp.configure_data_node(id="cleaned_dataset") # ,
                                                                   # cacheable=True,
                                                                   # validity_period=dt.timedelta(days=1)

predictions_cfg = tp.configure_data_node(id="predictions", scope=Scope.PIPELINE)
```


# Functions

Let's declare my functions: *clean_data* and *predict_baseline*. Their goal is respectively to clean the data and to predict the data.

[CODE]
```python
def clean_data(initial_dataset: pd.DataFrame):
    ...
    return cleaned_dataset


def predict_baseline(cleaned_dataset: pd.DataFrame, nb_predictions: int, day: dt.datetime, max_capacity: int):
    ...
    return predictions
```

# Tasks

Tasks are the translation of functions in Taipy. This is through these tasks that we will create our graph. Creating a task is simple: we need an id, a function, inputs and outputs.


## clean_data_task

The first task that we want to create is our *clean_data* task. It will take our initial dataset and clean it. 

<img src="/steps/images/clean_data.svg"/>


[CODE]
```python
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        function=clean_data,
                                        input=initial_dataset_cfg,
                                        output=cleaned_dataset_cfg)
```

## predict_baseline_task

This task will take our cleaned dataset and predict according our parameters.

<img src="/steps/images/predict_baseline.svg"/>

[CODE]
```python
predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              function=predict_baseline,
                                              input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, max_capacity_cfg],
                                              output=predictions_cfg)
```