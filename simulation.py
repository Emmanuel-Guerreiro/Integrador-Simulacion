import copy
from typing import List

import numpy as np

from carrefour import Carrefour
from client import Client, ClientType
from coto import Coto
from util import Random
from util import Plot

MAX_SERVICE_TIME = 100
MAX_ARRIVAL_TIME = 100
# This is just a security flag
MAX_WORKING_TIME = 720


class Simulation:
    """
    Clients: It is a stack because is easier to move to the following
    client inside the algorithms (Just pop from the non completed
    clients list). The stack will be storted by arrival time in descended
    order
    """

    def __init__(
        self,
        n_clients: int,
        n_lines: int,
        service_init_hour: int,
        service_end_hour: int,
    ) -> None:
        self.n_clients = n_clients
        self.n_lines = n_lines
        self.clients: List[ClientType] = []  # A stack
        self.service_init = service_init_hour
        self.service_end = service_end_hour
        self.results: dict = {}
        pass

    def init_clients(self, mean, deviation, min, max):
        services = self.init_service_times(
            mean, deviation, min, max, amount=self.n_clients
        )
        arrivals = self.init_arrival_times(
            total=self.n_clients, min_arrival=0, max_arrival=12*60
        )
        for i in range(len(services)):
            c = Client(arrival_time=arrivals[i], service_time=services[i])
            self.clients.append(c)

        self.sort_clients()
        return

    def init_service_times(self, mean, deviation, min, max, amount) -> List[int]:
        return Random().generate_normal_distribution(
            mean=mean, amount=amount, deviation=deviation, min=min, max=max
        )

    def init_arrival_times(self, total, min_arrival, max_arrival):
        """
        The histogram of supermarket population during the day, shows
        two local max, at 12pm and 6pm.
        Two normal distribution, with different means, and the same deviation,
        generate considerably good values

        For more information, check the project documentation
        """
        iter = 0
        while True:
            morning = Random().generate_normal_distribution(
                mean=240,
                deviation=100,
                amount=int(total),
                min=min_arrival,
                max=max_arrival,
            )
            afternoon = Random().generate_normal_distribution(
                mean=600,
                deviation=100,
                amount=int(total),
                min=min_arrival,
                max=max_arrival,
            )
            concat = np.concatenate((morning, afternoon))
            if len(concat) > total:
                arrivals = np.random.choice(concat, total)
                return arrivals

            if iter == 0:
                raise Exception("reached: Arrival times generation limit")
            iter += 1

    def sort_clients(self):
        self.clients.sort()

    def run(self):
        coto_copy = copy.deepcopy(self.clients)
        Plot.plot_simulation_values(coto_copy)
        coto = Coto(clients=coto_copy, n_queues=self.n_lines, max_time=MAX_WORKING_TIME)
        self.results["coto"] = coto.run()

        carrefour_copy = copy.deepcopy(self.clients)
        carrefour = Carrefour(
            clients=carrefour_copy,
            n_queues=self.n_lines,
        )
        self.results["carrefour"] = carrefour.run()
