# Define a function to execute a task asynchronously
def execute_task_async(task):
    try:
        return task.execute_async().result()  # Executes the task asynchronously and waits for the result
    except Exception as e:
        print(f"Error executing task {task.description}: {e}")
        return None