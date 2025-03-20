import tensorflow as tf
import time

# Extract training time from a TensorBoard event file.
def get_training_time(event_file):
    start_time = None
    end_time = None

    for event in tf.compat.v1.train.summary_iterator(event_file):
        if event.wall_time:
            if start_time is None:
                start_time = event.wall_time
            end_time = event.wall_time

    if start_time and end_time:
        duration = end_time - start_time
        return duration
    else:
        return None

event_file_path = "D:/Downloads/JN/logs/events.out.tfevents.1740028403.MSI.3992.0"
training_time = get_training_time(event_file_path)

if training_time:
    print(f"Training time: {training_time:.2f} seconds")
    print(f"Training time: {time.strftime('%H:%M:%S', time.gmtime(training_time))}")
else:
    print("Could not extract training time.")