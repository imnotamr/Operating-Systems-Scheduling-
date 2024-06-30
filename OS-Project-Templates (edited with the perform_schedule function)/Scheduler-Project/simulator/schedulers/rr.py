from simulator.schedulers.scheduler import Scheduler

class RoundRobin(Scheduler):
    """Round Robin (RR) scheduler."""
    def __init__(self, quantum=2):
        super(RoundRobin, self).__init__()
        self.quantum = quantum

    def perform_schedule(self):
        """
        We run each process for a fixed time interval (quantum).
        """
        from collections import deque

        ready_queue = deque()
        current_time = 0
        idx = 0
        while idx < len(self.processes) or ready_queue:
            while idx < len(self.processes) and self.processes[idx].arrive_time <= current_time:
                ready_queue.append(self.processes[idx])
                idx += 1
            if ready_queue:
                process = ready_queue.popleft()
                if process.start_time is None:
                    process.start_time = current_time
                exec_time = min(self.quantum, process.burst_time)
                current_time += exec_time
                process.burst_time -= exec_time
                if process.burst_time == 0:
                    process.finish_time = current_time
                    self.waiting_time += process.start_time - process.arrive_time
                else:
                    ready_queue.append(process)
            else:
                current_time += 1

        return self.processes

    def __repr__(self):
        """Return the scheduler's statistics as a string."""
        s = ['# processes: {}'.format(self.processes),
             'current time: {}'.format(self.current_time),
             'waiting time: {}'.format(self.waiting_time),
             'avg waiting time: {}'.format(self.avg_waiting_time)]

        return '\n'.join(s)
