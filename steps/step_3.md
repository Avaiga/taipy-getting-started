We have seen tha basics of the Taipy Graphical User Inerface. Let's go to the Scenario Management aspect of Taipy.

BENEFITS

Our goal is to create a Directed Acyclic Graph (DAG) that represents a scenario. Here, we will just create a single pipeline that will take our initial dataset, clean it and give predictions.

[IMAGE GRAPH]

We are going to describe this graph by configuring datanodes (variables) and tasks (functions).

Concepts :
    [] - Storage_type: There are multiple storage types. You can read csv file, SQL database, pickle file, etc. Here, we are going to      create a csv datanode to read/store our initial dataset. Taipy will know how to access it thanks to the path.

    [] - Scope: You can find in the code below two types of Scope: the Pipeline and Scenario scope. 
            Basically, With Scenario scope, datanodes are shared between all the pipelines of the scenario. A pipeline can call a datanode that is not created by itsself but by another pipeline.
            With Pipeline scope, datanodes are not shared between pipelines and don't have access to other datanodes from other pipelines. For example, here, I will have one 'predictions' datanode for each pipeline. So, if I add pipelines/algorithms, it will be all stored in the "predictions" datanodes but in different pipelines.

    [] - Cacheable: It is a performance parameter. If the datanode has already been created and the inputs didn't change. It is not necessary to run it again.