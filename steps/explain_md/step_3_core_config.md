With this last code, you should understand the basics of Taipy GUI. Let's go for a moment to the Scenario Management aspect of Taipy.

There are a lot of reasons to use Taipy Core.
- Efficiently manage the execution of your functions
- Keep track of data and KPIs.
- Handy to manage multiple pipelines in the context of Machine Learning or Mathematical optimization.

Taipy allows you to manage them effortlessly. To apprehend the Scenario Management aspect of Taipy, you need to understand four essential concepts.

## Four basic [concepts](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/) in Taipy Core:
- [**Datanodes**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/data-node/): are the translation of variables in Taipy. They don't contain the data itself but knows how to retrieve it. It can refer to any type of data: any *Python* object (string, int, list, dict, model, dataframe, etc), Pickle, CSV file or even SQL database. They know how to read and write data. You can even write your own custom data node if needed to access a particular data.
- [**Tasks**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/task/): are the translation of functions in Taipy.
- [**Pipelines**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/pipeline/): are a list of tasks executed with intelligent scheduling created automatically by Taipy. They usually represent a series of tasks for different algorithms like a baseline or Machine-Learning algorithm.
- [**Scenarios**](https://didactic-broccoli-7da2dfd5.pages.github.io/manuals/core/concepts/scenario/): are your business problem with some parameters. They usually consist of one or multiple pipelines.


Let's create a Machine Learning example to make it clearer. In a Machine Learning problem, it is usual to have numerous training and testing pipelines for different algorithms.
For simplification, one baseline pipeline will be configured in this step. Therefore, the goal is to create a Directed Acyclic Graph (DAG) that represents this pipeline. This single pipeline takes the initial dataset, cleans it, and gives predictions for the *day* without knowing the days after *day*.

<p align="center">
            <img src="/steps/images/baseline_pipeline.svg" width=500>
</p>


The creation of this graph is done by configuring data nodes (variables) and tasks (functions). This configuration doesn't execute anything; it is just a setup to create the DAG.

# Datanodes configuration

Data nodes can point to anykind of *Python* variables by default: int, string, dict, list, np.array, pd.DataFrame, models, etc. Taipy has the ability to read and write a CSV, Pickle file or SQL database through a data node.

Let me introduce some parameters for data nodes :
- **Storage_type**: There are multiple storage types. You can read csv file, SQL database, pickle file, etc.
            Here, you are going to create a csv datanode to read/store the initial dataset. Taipy knows how to access it thanks to the path.

- **Scope**: You can find in the code below two types of Scope: the Pipeline and Scenario scope (by default). 
            Basically, with Scenario scope, datanodes are shared between all the pipelines of the scenario.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, a 'predictions' datanode is created for each pipeline. So, adding pipelines/algorithms will create predictions stored in different "predictions" datanodes.

"""- **Cacheable**: It is a parameter used for more performance. If the datanode has already been created and the inputs didn't    change. It is not necessary to run it again."""


## Input data nodes configuration
These are my input data nodes. These data nodes represent my variables in Taipy when a pipeline is executed. Still, first, we have to configure them to create the DAG.

- *initial_dataset* is simply the initial CSV file. Taipy needs some parameters to read this data like *path* and *header*. 

- *day* is the beginning of the predictions. The default value is the 26th of July. It means my training data will end before the 26th of July, and my predictions will begin on this day.

- *n_predictions* is the number of predictions you want to make while predicting. The default value is 40. Each algorithm creates its own *prediction* data node hence `scope=Scope.PIPELINE`. 

- *max_capacity* is the maximum value that can take a prediction; it is the ceiling of the projections. The default value is 200.

```python
## Input datanodes
initial_dataset_cfg = tp.configure_data_node(id="initial_dataset",
                                             storage_type="csv",
                                             path=path_to_csv)

day_cfg = tp.configure_data_node(id="day", default_data=dt.datetime(2021, 7, 26))

n_predictions_cfg = tp.configure_data_node(id="n_predictions", default_data=40)

max_capacity_cfg = tp.configure_data_node(id="max_capacity", default_data=200)

```

 ## Remaining data nodes

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


def predict_baseline(cleaned_dataset: pd.DataFrame, n_predictions: int, day: dt.datetime, max_capacity: int):
    ...
    return predictions # returns a pd.DataFrame
```

# Tasks

Tasks are the translation of functions in Taipy. These tasks combined with data nodes create your graph. Creating a task is simple; you need:
- An id
- A function
- Inputs
- Outputs

## clean_data_task

The first task that you want to create is your *clean_data* task. It will take your initial dataset and clean it.

<p align="center">
            <img src="/steps/images/clean_data.svg" width=300>
</p>

```python
clean_data_task_cfg = tp.configure_task(id="clean_data",
                                        function=clean_data,
                                        input=initial_dataset_cfg,
                                        output=cleaned_dataset_cfg)
```

## predict_baseline_task

This task will take your cleaned dataset and predict it according to your parameters.

<p align="center">
            <img src="/steps/images/predict_baseline.svg" width=300>
</p>

```python
predict_baseline_task_cfg = tp.configure_task(id="predict_baseline",
                                              function=predict_baseline,
                                              input=[cleaned_dataset_cfg, n_predictions_cfg, day_cfg, max_capacity_cfg],
                                              output=predictions_cfg)
```
