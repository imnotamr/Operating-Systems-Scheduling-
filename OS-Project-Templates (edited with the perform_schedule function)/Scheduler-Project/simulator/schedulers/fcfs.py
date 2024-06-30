from simulator.schedulers.scheduler import Scheduler

class FCFS(Scheduler):
    """First Come First Serve (FCFS) scheduler."""

    def __init__(self):
        super(FCFS, self).__init__()

    def perform_schedule(self):
        """
        We simply sort the processes by the time that they come in by, and
        only change process as the processes finish their execution on the
        CPU.
        """
        # Sort the processes by their arrival time
        self.processes.sort(key=lambda x: x.arrive_time)

        current_time = 0
        for process in self.processes:
            if current_time < process.arrive_time:
                current_time = process.arrive_time
            process.start_time = current_time
            process.finish_time = current_time + process.burst_time
            current_time = process.finish_time
            self.waiting_time += process.start_time - process.arrive_time

        return self.processes
