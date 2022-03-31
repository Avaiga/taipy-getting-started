from step_03 import tp, clean_data_task_cfg, predict_baseline_task_cfg, dt

# Create the the first scenario configuration
baseline_pipeline_cfg = tp.configure_pipeline(id="baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])

## Execute the 'baseline' pipeline
if __name__ == "__main__":
    # Create the pipeline
    baseline_pipeline = tp.create_pipeline(baseline_pipeline_cfg)
    # Submit the pipeline (Execution)
    tp.submit(baseline_pipeline)
    
    # Read output data from the pipeline
    baseline_predictions = baseline_pipeline.predictions.read()
    print("Predictions of baseline algorithm\n", baseline_predictions)
