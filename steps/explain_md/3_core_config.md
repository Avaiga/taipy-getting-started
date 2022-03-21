With this step, you already know the basics of the Taipy Graphical User Interface. Let's go for a moment to the Scenario Management aspect of Taipy.

Taipy Core can be used for a lot of different reasons. With it, you can manage efficiently the execution of your functions, keep track of data and/or KPI. It is extremely useful in the context of Machine Learning or Mathematical optimization for example where you can have a lot of different models with a lot of initial parameters. Taipy will allow to manage all of them in a very simple way.

To understand the Scenario Management aspect of Taipy, there are just 4 concepts to understand.

## Four basic concepts in Taipy Core:
- **Datanodes**: are the translation of variables in Taipy. They are objects that will point to your data whatever it is (pickle, csv, json, etc.). Thery are able to read and write data.
- **Tasks**: are translation of functions in Taipy.
- **Pipelines**: are a list of tasks that will be executed with a smart scheduling automatically created by Taipy. They usually represent series of tasks for different algorithms like a baseline or machine algorithm.
- **Scenarios**: are your business problem with some parameters. They usually consist of one or multiple pipelines.


Let's a Machine Learning example. In a Machine Learning, we normally have a training and a testing pipeline. In a lot of situations, we have a lot of testing pipelines with different models.
To simplify this problem for the Getting Started, just a baseline pipeline will be configured in this step. Therefore, the goal is to create a Directed Acyclic Graph (DAG) that represents this pipeline so our problem for the moment. This single pipeline will take the initial dataset, clean it and give predictions for the the *day* without knowing the days after *day*.

<center>
<img src="/steps/images/baseline_pipeline.svg" height=700 width=700px />
</center>

The creation of this graph is done by configuring datanodes (variables) and tasks (functions). Nothing will be executed, it is just a setup to create the DAG.

# Datanodes configuration

Anykind of serializable object can be used as a datanode: int, string, dict, list, np.array, pd.DataFrame, models etc...

Let me introduce some parameters for datanodes :
- **Storage_type**: There are multiple storage types. You can read csv file, SQL database, pickle file, etc.
            Here, we are going to create a csv datanode to read/store the initial dataset. Taipy will know how to access it thanks to the path.

- **Scope**: You can find in the code below two types of Scope: the Pipeline and Scenario scope. 
            Basically, With Scenario scope, datanodes are shared between all the pipelines of the scenario. A pipeline can call a datanode that is not created by itself but by another pipeline.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, I will have one 'predictions' datanode for each pipeline. So, if I add pipelines/algorithms, predictions will be all stored in different "predictions" datanodes.

- **Cacheable**: It is a parameter used for more performance. If the datanode has already been created and the inputs didn't    change. It is not necessary to run it again.


## Input datanodes
These are my input datanodes. The one that I will change to create different scenarios.

- *initial_dataset* is simply the initial csv file. We put some parameters to be able to read this data like *path* and *header*. 

- *day* is the beginning of the predictions. The default value is 26th of July. It means my training data will end before 26th of July and my predictions will begin on this day.

- *nb_predictions* is the number of predictions we want to make while predicting. The default value is 40. We want to have a *prediction* datanode for each algorithm. This is why we specify **Scope.PIPELINE**. 

- *max_capacity* is the maximum value that can take a prediction; it is the seiling of predictions problem. The default value is 200.

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

```python
## Remaining datanodes
cleaned_dataset_cfg = tp.configure_data_node(id="cleaned_dataset") # ,
                                                                   # cacheable=True,
                                                                   # validity_period=dt.timedelta(days=1)

predictions_cfg = tp.configure_data_node(id="predictions", scope=Scope.PIPELINE)
```


# Functions

Let's declare my functions: *clean_data* and *predict_baseline*. Their goal is respectively to clean the data and to predict the data.

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

<center>
<img src="/steps/images/clean_data.svg" height=300px width=500px />
</center>

```python
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        function=clean_data,
                                        input=initial_dataset_cfg,
                                        output=cleaned_dataset_cfg)
```

## predict_baseline_task

This task will take our cleaned dataset and predict according our parameters.

<center>
<img src="/steps/images/predict_baseline.svg" height=500px width=500px/>
</center>

```python
predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              function=predict_baseline,
                                              input=[cleaned_dataset_cfg, nb_predictions_cfg, day_cfg, max_capacity_cfg],
                                              output=predictions_cfg)
```