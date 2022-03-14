from step_3 import tp, clean_data_task_cfg, predict_baseline_task_cfg, dt

# Creation of the first scenario configuration
baseline_pipeline_cfg = tp.configure_pipeline(id="baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])

## Execution of baseline pipeline
if __name__ == "__main__":
    # Creation of baseline pipeline
    baseline_pipeline = tp.create_pipeline(baseline_pipeline_cfg)
    # Submitting it
    tp.submit(baseline_pipeline)
    
    # Reading data from the pipeline
    baseline_predictions = baseline_pipeline.predictions.read()
    print("Predictions of baseline algorithm\n", baseline_predictions)