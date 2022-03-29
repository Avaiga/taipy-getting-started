So far, you have described your graph; let's implement it with Taipy! 

# Pipeline configuration

To configure your first pipeline, you need to list all the tasks you want to be done by the pipeline. This pipeline executes the cleaning (*clean_data_task*) and the predicting (*predict_baseline*). Note that the **task_configs** is a list, so you don't have to worry about the order of the tasks. Taipy does that for you and optimizes its execution.

```python
# Create the the first scenario configuration
baseline_pipeline_cfg = tp.configure_pipeline(id="baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])
```

# Pipeline creation and execution

Then, create your pipeline from its configuration, submit it, and print the "predictions" Data Node results.

```python
# Create the pipeline
baseline_pipeline = tp.create_pipeline(baseline_pipeline_cfg)
# Submit the pipeline (Execution)
tp.submit(baseline_pipeline)
    
# Read output data from the pipeline
baseline_predictions = baseline_pipeline.predictions.read()
print("Predictions of baseline algorithm\n", baseline_predictions)
```
