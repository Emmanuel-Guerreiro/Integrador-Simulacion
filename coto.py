from typing import List

from client import Client


class Coto:
    def __init__(self, max_time, n_queues, clients: List[Client]) -> None:
        self.time = 0
        self.max_time = max_time
        self.clients = clients
        self.dropped_clients = []

        # We create a list of queues where each queue is a list of clients
        self.queues: List[List[Client]] = [[] for _ in range(n_queues)]
        self.completed: List[Client] = []
        return

    def get_less_charged_queue(self) -> int:
        """
        Return the index of the queue with less clients
        """
        # Key specifies the function to be used to determine the order
        return min(range(len(self.queues)), key=lambda i: len(self.queues[i]))

    def check_queue(self, queue: List[Client]):
        """
        Check if the first client in the queue is done
        """
        if len(queue) > 0:
            if queue[0].calc_service_end_time() <= self.time:
                self.completed.append(queue.pop(0))
        return

    def attend_client(self, queue: List[Client]):
        """
        Attend the first client in the queue
        """
        if len(queue) > 0 and queue[0].service_start_time == None:
            queue[0].service_start_time = self.time
        return

    def check_arrival_time(self, clients: List[Client]) -> List[Client]:
        """
        Check if there are clients that have arrived
        """
        return [client for client in clients if client.arrival_time == self.time]

    def add_client_to_queue(self, client: Client):
        """
        Add clients to the queue with less clients
        """
        clients_to_add = self.check_arrival_time(self.clients)
        # Can be different queues
        for i in range(len(clients_to_add)):
            self.queues[self.get_less_charged_queue()].append(clients_to_add[i])
        return

    def drop_clients(self):
        for queue in self.queues:
            for idx, client in enumerate(queue):
                if client.will_drop_on_time(self.time):
                    self.dropped_clients.append(client)
                    queue.pop(idx)
        return

    def run(self):

        for _ in range(self.max_time):
            if len(self.clients) > 0:

                # Add client to the queue with less clients
                self.add_client_to_queue(self.clients)

                # Check if the clients in the queues are done and attend the first client
                for queue in self.queues:
                    self.attend_client(queue)
                    self.check_queue(queue)
                self.time += 1

        return self.completed

    pass
