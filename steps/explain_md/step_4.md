What we have done so far is describing our graph, this graph represents our process. 

# Pipeline configuration

We can configure our first pipeline that we will be able to run. We configure it; you just need to list all the tasks you want to be done by the pipeline. Here we want this pipeline to execute the cleaning (*clean_data_task*) and the predicting (*predict_baseline*). Note that the **task_configs** is a list so you don't have to worry about the order of the tasks. Taipy will do that for you and optimize its execution.

[CODE]
```python
# Creation of the first scenario configuration
baseline_pipeline_cfg = tp.configure_pipeline(id="baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])
```

# Pipeline creation and execution

Then, we create our pipeline from its configuration, we submit it (execution) and we print the results of the "predictions" datanode.

[CODE]
```python
# Creation of baseline pipeline
baseline_pipeline = tp.create_pipeline(baseline_pipeline_cfg)
# Submit the pipeline (Execution)
tp.submit(baseline_pipeline)
    
# Reading data from the pipeline
baseline_predictions = baseline_pipeline.predictions.read()
print("Predictions of baseline algorithm\n", baseline_predictions)
```