import random
from typing import List

from carrefour import Carrefour
from client import Client
from coto import Coto

MAX_SERVICE_TIME = 100
MAX_ARRIVAL_TIME = 100
# This is just a security flag
MAX_WORKING_TIME = (MAX_SERVICE_TIME + MAX_ARRIVAL_TIME) * 2


class Main:
    """
    Clients: It is a stack because is easier to move to the following
    client inside the algorithms (Just pop from the non completed
    clients list). The stack will be storted by arrival time in descended
    order
    """

    def __init__(self, n_clients: int, n_lines: int) -> None:
        self.n_clients = n_clients
        self.n_lines = n_lines
        self.clients: List[Client] = []  # A stack
        pass

    def init_clients(self):
        # The last time makes defines the upper bond to the
        # next client arrival, naturally sorting it by arrival time
        # In descended way
        last_at = 0
        for _ in range(self.n_clients):
            at = random.randint(last_at, 100)
            # last_at = at
            st = random.randint(1, MAX_SERVICE_TIME)
            self.clients.append(Client(arrival_time=at, service_time=st))

        self.sort_clients()
        return

    def sort_clients(self):
        self.clients.sort()

    def print_clients(self):
        print(self.clients)

    def run(self):
        self.init_clients()
        #list = Carrefour(clients=self.clients, n_queues=self.n_lines).run()
        #print(list)

        list = Coto(clients=self.clients, n_queues=self.n_lines, max_time=MAX_WORKING_TIME).run()
        pass


if __name__ == "__main__":
    main = Main(n_clients=10, n_lines=1)
    # main.print_clients()
    main.run()
