from step_3 import *

pipeline_baseline_cfg = tp.configure_pipeline(name="pipeline_baseline",
                                              task_configs=[clean_data_cfg,
                                                            predict_baseline_cfg])

if __name__ == "__main__":
    first_pipeline = tp.create_pipeline(pipeline_baseline_cfg)
    tp.submit(first_pipeline)
    first_pipeline = tp.get(first_pipeline.id)

    baseline_predictions = first_pipeline.predictions.read()
    print(baseline_predictions)