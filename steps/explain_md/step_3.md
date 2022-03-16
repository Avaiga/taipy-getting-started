We have seen tha basics of the Taipy Graphical User Inerface. Let's go to the Scenario Management aspect of Taipy.

BENEFITS...

Firstly, our goal is to create a Directed Acyclic Graph (DAG) that represents a scenario. Here, we will just create a single pipeline that will take our initial dataset, clean it and give predictions.

[IMAGE GRAPH] lucid chart / powerpoint / google drawing / call Jean Robin

We are going to describe this graph by configuring datanodes (variables) and tasks (functions). Nothing will be executed, it is just a setup.

# Datanodes

Datanodes are the translation of variables in Taipy. Datanodes are pointers to the data; they are able to read and write data. Anykind of serializable object can be used as a datanode: int, string, dict, list, np.array, pd.DataFrame, models etc...

Let me introduce some concept for datanodes :
    [] - Storage_type: There are multiple storage types. You can read csv file, SQL database, pickle file, etc.
            Here, we are going to create a csv datanode to read/store our initial dataset. Taipy will know how to access it thanks to the path.

    [] - Scope: You can find in the code below two types of Scope: the Pipeline and Scenario scope. 
            Basically, With Scenario scope, datanodes are shared between all the pipelines of the scenario. A pipeline can call a datanode that is not created by itself but by another pipeline.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, I will have one 'predictions' datanode for each pipeline. So, if I add pipelines/algorithms, predictions will be all stored in different "predictions" datanodes.

    [] - Cacheable: It is a parameter used for more performance. If the datanode has already been created and the inputs didn't    change. It is not necessary to run it again.


## Input datanodes

- *initial_dataset* is simply our initial csv file. We put some parameters to be able to read this data like *path* or *header*. 

- *day* is the beginning of the predictions. The default value is 26th of July. It means my training data will end before 26th of July and my predictions will begin on this day.

- *nb_predictions* is the number of predictions we want to make while predicting. The default value is 40. We want to have a *prediction* datanode for each algorithm. This is why we specify **Scope.PIPELINE**. 

- *max_capacity* is the maximum value that can take a prediction; this is a constraint on our problem. The default value is 00.

[CODE]

## Remaining datanodes

- *cleaned_dataset* is the dataset after cleaning (after the *clean_data* function).

- *predictions* is the predictions of the model. Here, it is the return of my *predict_baseline* function.

[CODE]

# Functions

Let's declare my functions: *clean_data* and *predict_baseline*. Their goal is respectively to clean the data and to predict the data.

[CODE]

# Tasks

Tasks are the translation of functions in Taipy. This is through these tasks that we will create our graph. Creating a task is simple: we need an id, a function, a list of inputs or just an input and a list of output or an output.


## clean_data_task

The first task that we want to create is our *clean_data* task. It will take our initial dataset and clean it. 

[IMAGE GRAPH]

[CODE]

## predict_baseline_task

This task will take our cleaned dataset and predict according our parameters.

[IMAGE GRAPH]

[CODE]
