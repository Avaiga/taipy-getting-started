# Creation and execution of Scenarios

Now that we have seen how to create and run a single pipeline, we are going to configure a scenario that will run two pipelines: the one we created (*baseline*) and another one (*ml*) that will predict through a different algorithm.

A scenario is our business problem. Different scenarios would represent different solutions to our business problem. Here, our scenario is influenced by the *max_capacity*, *day* and *number of predictions*. With just a couple more lines you could add more pipelines/algorithms. Different scenarios would represent different solution to our business problem.

When creating your scenario, it will create your pipelines and when you execute it, it will execute your pipelines through smart scheduling. Taipy knows which tasks to do before which one and will be able to cancel Jobs if a task is repetitive. If you didn't forget, it is the use of the 'cacheable' parameter.
