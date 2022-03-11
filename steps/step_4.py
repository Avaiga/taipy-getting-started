from step_3 import tp, clean_data_task_cfg, predict_baseline_task_cfg, dt

# Creation of the first scenario configuration
pipeline_baseline_cfg = tp.configure_pipeline(id="pipeline_baseline",
                                              task_configs=[clean_data_task_cfg, predict_baseline_task_cfg])

if __name__ == "__main__":
    # Creation of the first pipeline
    first_pipeline = tp.create_pipeline(pipeline_baseline_cfg)
    # Submitting it
    tp.submit(first_pipeline)
    
    # Reading data from the pipeline
    baseline_predictions = first_pipeline.predictions.read()
    print("Predictions of baseline\n", baseline_predictions)