With this last code, you should understand the basics of Taipy GUI. Let's go for a moment to the Scenario Management aspect of Taipy.

Taipy Core can be used for a lot of different reasons. With it, you can manage efficiently the execution of your functions, keep track of data and/or KPI. It is extremely useful in the context of Machine Learning or Mathematical optimization for example where you can have a lot of different models with a lot of initial parameters. Taipy allows you to manage them in a very simple way.

To apprehend the Scenario Management aspect of Taipy, there are just 4 concepts to understand.

## Four basic [concepts](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/) in Taipy Core:
- [**Datanodes**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/data-node/): are the translation of variables in Taipy. They are objects that points to your data whatever it is (pickle, csv, json, etc.). Thery are able to read and write data.
- [**Tasks**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/task/): are translation of functions in Taipy.
- [**Pipelines**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/pipeline/): are a list of tasks that is executed with a smart scheduling created automatically by Taipy. They usually represent series of tasks for different algorithms like a baseline or Machine-Learning algorithm.
- [**Scenarios**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/scenario/): are your business problem with some parameters. They usually consist of one or multiple pipelines.


Let's create a Machine Learning example. In a Machine Learning, you normally have a training and a testing pipeline. In a lot of situations, you also have a lot of testing pipelines with different models.
To simplify this problem for the **Getting Started**, one baseline pipeline will be configured in this step. Therefore, the goal is to create a Directed Acyclic Graph (DAG) that represents this pipeline. This single pipeline takes the initial dataset, clean it and give predictions for the the *day* without knowing the days after *day*.

<img src="/steps/images/baseline_pipeline.svg" height=700 width=700px alt="centered image"/>

The creation of this graph is done by configuring datanodes (variables) and tasks (functions). Nothing is executed, it is just a setup to create the DAG.

# Datanodes configuration

Anykind of serializable object can be used as a datanode: int, string, dict, list, np.array, pd.DataFrame, models etc...

Let me introduce some parameters for datanodes :
- **Storage_type**: There are multiple storage types. You can read csv file, SQL database, pickle file, etc.
            Here, you are going to create a csv datanode to read/store the initial dataset. Taipy knows how to access it thanks to the path.

- **Scope**: You can find in the code below two types of Scope: the Pipeline and Scenario scope (by default). 
            Basically, with Scenario scope, datanodes are shared between all the pipelines of the scenario.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, a 'predictions' datanode is created for each pipeline. So, adding pipelines/algorithms will create predictions stored in different "predictions" datanodes.

"""- **Cacheable**: It is a parameter used for more performance. If the datanode has already been created and the inputs didn't    change. It is not necessary to run it again."""


## Input datanodes
These are my input datanodes. These datanodes will create different scenarios depending on their value.

- *initial_dataset* is simply the initial csv file. Taipy needs some parameters to be able to read this data like *path* and *header*. 

- *day* is the beginning of the predictions. The default value is 26th of July. It means my training data will end before 26th of July and my predictions will begin on this day.

- *number_predictions* is the number of predictions you want to make while predicting. The default value is 40. For each algorithm,a *prediction* datanode will be created hence `scope=Scope.PIPELINE`. 

- *max_capacity* is the maximum value that can take a prediction; it is the seiling of predictions problem. The default value is 200.

```python
## Input datanodes
initial_dataset_cfg = tp.configure_data_node(id="initial_dataset",
                                             storage_type="csv",
                                             path=path_to_csv)

number_predictions_cfg = tp.configure_data_node(id="number_predictions", default_data=40)

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
    return cleaned_dataset # returns a pd.DataFrame


def predict_baseline(cleaned_dataset: pd.DataFrame, number_predictions: int, day: dt.datetime, max_capacity: int):
    ...
    return predictions # returns a pd.DataFrame
```

# Tasks

Tasks are the translation of functions in Taipy. This is through these tasks that you will create your graph. Creating a task is simple: you need an id, a function, inputs and outputs.


## clean_data_task

The first task that you want to create is your *clean_data* task. It will take your initial dataset and clean it. 

<img src="/steps/images/clean_data.svg" height=300px width=500px alt="centered image"/>

```python
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        function=clean_data,
                                        input=initial_dataset_cfg,
                                        output=cleaned_dataset_cfg)
```

## predict_baseline_task

This task will take your cleaned dataset and predict according your parameters.

<img src="/steps/images/predict_baseline.svg" height=500px width=500px alt="centered image"/>

```python
predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              function=predict_baseline,
                                              input=[cleaned_dataset_cfg, number_predictions_cfg, day_cfg, max_capacity_cfg],
                                              output=predictions_cfg)
```
