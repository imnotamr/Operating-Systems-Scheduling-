from simulator.schedulers.scheduler import Scheduler

class SRTF(Scheduler):
    """Shortest Remaining Time First (SRTF) scheduler."""
    def __init__(self):
        super(SRTF, self).__init__()

    def perform_schedule(self):
        """
        We always pick the process with the shortest remaining time to finish.
        """
        import heapq

        ready_queue = []
        current_time = 0
        idx = 0
        while idx < len(self.processes) or ready_queue:
            while idx < len(self.processes) and self.processes[idx].arrive_time <= current_time:
                heapq.heappush(ready_queue, (self.processes[idx].burst_time, self.processes[idx]))
                idx += 1
            if ready_queue:
                remaining_time, process = heapq.heappop(ready_queue)
                if process.start_time is None:
                    process.start_time = current_time
                current_time += 1
                process.burst_time -= 1
                if process.burst_time == 0:
                    process.finish_time = current_time
                    self.waiting_time += process.start_time - process.arrive_time
                else:
                    heapq.heappush(ready_queue, (process.burst_time, process))
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
