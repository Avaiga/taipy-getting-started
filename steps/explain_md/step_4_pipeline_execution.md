What you have done so far is describing your graph, this graph represents your process. 

# Pipeline configuration

To configure your first pipeline you just need to list all the tasks you want to be done by the pipeline. Here this pipeline executes the cleaning (*clean_data_task*) and the predicting (*predict_baseline*). Note that the **task_configs** is a list so you don't have to worry about the order of the tasks. Taipy does that for you and optimize its execution.

```python
# Creation of the first scenario configuration
baseline_pipeline_cfg = tp.configure_pipeline(id="baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])
```

# Pipeline creation and execution

Then, you create your pipeline from its configuration, you submit it (execution) and you print the results of the "predictions" datanode.

```python
# Creation of baseline pipeline
baseline_pipeline = tp.create_pipeline(baseline_pipeline_cfg)
# Submit the pipeline (Execution)
tp.submit(baseline_pipeline)
    
# Reading data from the pipeline
baseline_predictions = baseline_pipeline.predictions.read()
print("Predictions of baseline algorithm\n", baseline_predictions)
```