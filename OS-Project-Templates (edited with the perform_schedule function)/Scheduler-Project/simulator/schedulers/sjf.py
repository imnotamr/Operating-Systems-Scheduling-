from simulator.core.pq import PriorityQueue
from simulator.schedulers.scheduler import Scheduler

class SJF(Scheduler):
    """Shortest Job First (SJF) scheduler."""
    def __init__(self, alpha=0.5):
        super(SJF, self).__init__()
        self.alpha = alpha

        
        self.q = PriorityQueue()

        # Keeps track of all estimates for CPU burst time
        self.tau = {}

    def schedule(self, processes):
        """
        We make use of a heap to keep track of the task with the longest burst
        time left.
        """
        self.tau = {process.id: 0 for process in processes}
        return super(SJF, self).schedule(processes)

    def enqueue_new_jobs(self):
        """
        (OVERRIDE) - Scheduler.enqueue_new_jobs
        We need to override this to make use of our PriorityQueue API instead.
        """
        while self.ordered and self.ordered[0].arrive_time <= self.current_time:
            nxt = self.ordered.popleft()
            self.q.add(nxt, priority=self.tau[nxt.id])

    def perform_schedule(self):
        """
        Returns the order of processes that the CPU executed.
        """
        current_time = 0
        while not self.q.empty():
            process = self.q.pop()
            if current_time < process.arrive_time:
                current_time = process.arrive_time
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            current_time = process.finish_time
            self.waiting_time += process.start_time - process.arrive_time
            self.enqueue_new_jobs()
        
        return self.q

    def __repr__(self):
        """Return the scheduler's statistics as a string."""
        s = ['# processes: {}'.format(self.processes),
             'current time: {}'.format(self.current_time),
             'waiting time: {}'.format(self.waiting_time),
             'avg waiting time: {}'.format(self.avg_waiting_time)]

        return '\n'.join(s)
