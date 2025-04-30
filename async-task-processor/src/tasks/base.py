class BaseTask:
    def __init__(self, task_name):
        self.task_name = task_name

    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method.")

    def get_task_name(self):
        return self.task_name

    def on_success(self):
        print(f"Task '{self.task_name}' completed successfully.")

    def on_failure(self):
        print(f"Task '{self.task_name}' failed.")