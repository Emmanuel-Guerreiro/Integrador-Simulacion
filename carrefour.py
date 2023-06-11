from typing import List, Tuple

from client import Client, ClientType


class Carrefour:
    def __init__(self, n_queues, clients: List[ClientType]) -> None:
        """
        clients: A priority queue -already sorted- by ascendent arrival time
        """
        self.time = 0
        self.clients = clients
        # This is returned from run method. The idea to move the already
        # completed clients to a different list, makes it easier
        # to send data back to the main method
        self.completed = []
        self.client_index = 0
        # Queues: List[Client | 0].
        # I did a few tries with None and it kept failing during the empty
        # process. 0 seems to work fine
        # If the queue is being used (check empty_finished_queues method)
        self.n_queues = n_queues
        self.queues: List = [None for _ in range(n_queues)]
        pass

    def is_some_queue_busy(self):
        return self.queues.count(None) != len(self.queues)

    def start_service(self, client: Client):
        client.service_start_time = self.time

    def empty_finished_queues(self):
        """
        Will set as None the queues where the current client has been
        completed
        """
        for idx, client in enumerate(self.queues):
            # If there is a client in the queue and the time of completition
            # Is the current, end it
            if not client:
                continue
            # client = self.queues[i]
            end_time = client.calc_service_end_time()
            if not end_time:
                # This is used for debugging
                raise Exception(f"Not end time for the client {client}")
            if end_time <= self.time:
                self.completed.append(client)
                self.queues[idx] = None
        return

    def is_client_waiting(self) -> bool:
        return (
            len(
                [
                    c
                    for c in self.clients
                    if c.arrival_time <= self.time and not c.service_start_time
                ]
            )
            != 0
        )

    def get_clients_waiting(self) -> List[ClientType]:
        """
        Returns the list of enumerate tuple[index, Client].
        """
        return [
            client
            for client in self.clients
            if client.arrival_time <= self.time and not client.service_start_time
        ]

    def get_empty_queues(self) -> List[int]:
        """Returns the idx of every empty queue"""
        return [i for i, c in enumerate(self.queues) if not c]

    def assign_client_to_queue(self) -> None:
        """
        This algortithm could be as complex as we want. Handling
        variables as time from main queue to the seller queue,
        or any other heuristic consideration.

        At the moment the algorithm will pick the first queue from
        the available list. To make it simpler

        available_queues: List with the index of the available queues
        """

        if not self.is_client_waiting():
            return

        clients_waiting = self.get_clients_waiting()
        # If there is no waiting client. Jump, to advance time
        if len(clients_waiting) == 0:
            return
        # If there is no waiting queue. Jump, to advance time
        available_queues_idx = self.get_empty_queues()
        if len(available_queues_idx) == 0:
            return
        for iter, av_idx in enumerate(available_queues_idx):

            if iter == len(clients_waiting):
                break

            client_to_assign = clients_waiting[iter]
            self.queues[av_idx] = client_to_assign

            self.clients.remove(client_to_assign)
            self.start_service(client_to_assign)

        return

    def run(self) -> List[ClientType]:
        # For + If instead of while avoids infinite loops

        print(self.clients)

        while len(self.clients) > 0 or self.is_some_queue_busy():
            self.empty_finished_queues()
            self.assign_client_to_queue()

            self.time += 1

        self.completed.sort()
        return self.completed

    pass
