from typing import List

from client import Client

# What to fix:
#   Actualmente estoy pasando la lista por referencia y le voy haciendo pop
#   El problema es que necesito retornarlos a la clase que lo llame,
#   Poder sacar estadisticos.

#   Entonces, una opcion es armar una clase de queue propia que
#   no borre cosas, si no que vaya moviendo un index. Y que un get_first
#   o algo asi me de el proximo elemento a trabajar

#   Porque si trabajo con el idx en la misma clase del carrefour,
#   y voy haciendo controles, se ensucia demasiado la logica

# Handle multiples available clients at the same time


class Carrefour:
    def __init__(self, max_time, n_queues, clients: List[Client]) -> None:
        self.time = 0
        self.max_time = max_time
        self.clients = clients
        # TODO: Explain why this decision
        self.completed = []
        self.client_index = 0
        # Queues: List[Client | 0].
        # I did a few tries with None and it kept failing during the empty
        # process. 0 seems to work fine
        # If the queue is being used (check empty_finished_queues method)
        self.queues: List[Client] = [0 for _ in range(n_queues)]
        pass

    def start_service(self, client: Client):
        client.service_start_time = self.time

    def empty_finished_queues(self):
        """
        Will set as None the queues where the current client has been
        completed
        """

        for i, client in enumerate(self.queues):
            # If there is a client in the queue and the time of completition
            # Is the current, end it
            if client != 0:
                end_time = client.calc_service_end_time()
                if end_time <= self.time:
                    self.completed.append(client)
                    self.queues[i] = 0
        return

    def is_client_waiting(self) -> bool:
        return self.clients[-1].arrival_time <= self.time

    def get_empty_queues(self) -> List[int]:
        return [i for i in range(len(self.queues)) if self.queues[i] == 0]

    def assign_client_to_queue(self, available_queues: List[int]) -> None:
        """
        This algortithm could be as complex as we want. Handling
        variables as time from main queue to the seller queue,
        or any other heuristic consideration.

        At the moment the algorithm will pick the first queue from
        the available list. To make it simpler

        available_queues: List with the index of the available queues
        """

        chosen_queue = available_queues[0]
        self.queues[chosen_queue] = self.clients[-1]
        self.clients[-1].service_start_time = self.time
        self.clients.pop(-1)
        return

    def run(self) -> List[Client]:
        """
        clients: A priority queue -already sorted- by ascendent arrival time
        """

        # For + If instead of while avoids infinite loops
        for _ in range(self.max_time):
            if len(self.clients) > 0:
                self.empty_finished_queues()
                if self.is_client_waiting():
                    queues = self.get_empty_queues()
                    if len(queues) > 0:
                        # Assign the client to the queue and remove from
                        # waiting list
                        self.assign_client_to_queue(queues)
                self.time += 1
        return self.completed

    pass
