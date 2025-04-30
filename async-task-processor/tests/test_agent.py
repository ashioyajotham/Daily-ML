import unittest
from src.core.agent import Agent
from src.core.timer import Timer

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()
        self.timer = Timer()

    def test_add_task(self):
        self.agent.add_task("task1")
        self.assertIn("task1", self.agent.tasks)

    def test_task_progress(self):
        self.agent.add_task("task2")
        self.agent.start_task("task2")
        self.assertTrue(self.agent.is_task_running("task2"))

    def test_timer_functionality(self):
        self.timer.start()
        self.timer.stop()
        elapsed_time = self.timer.elapsed()
        self.assertGreater(elapsed_time, 0)

if __name__ == '__main__':
    unittest.main()