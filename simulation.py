import copy
from typing import List

import numpy as np

from carrefour import Carrefour
from client import Client, ClientType
from coto import Coto
from util import Plot, Random

MAX_SERVICE_TIME = 100
MAX_ARRIVAL_TIME = 100
# This is just a security flag
MAX_WORKING_TIME = 720


class Simulation:
    def __init__(
        self,
        n_clients: int,
        n_lines: int,
    ) -> None:
        self.n_clients = n_clients
        self.n_lines = n_lines
        self.clients: List[ClientType] = []
        self.results: dict = {}
        self.mean_idle: dict = {}
        self.dropped_clients: dict = {}
        pass

    def init_clients(self, mean, deviation, min, max):
        services = self.init_service_times(
            mean, deviation, min, max, amount=self.n_clients
        )
        arrivals = self.init_arrival_times(
            total=self.n_clients, min_arrival=0, max_arrival=12 * 60
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
        Plot.plot_simulation_values(
            coto_copy, file_append=f"C{self.n_clients}Q{self.n_lines}"
        )
        coto = Coto(clients=coto_copy, n_queues=self.n_lines, max_time=MAX_WORKING_TIME)

        self.results["coto"] = coto.run().completed
        self.mean_idle["coto"] = np.mean(coto.idle_queues_in_time)
        self.dropped_clients["coto"] = len(coto.dropped_clients)

        print("Clientes atendidos en Coto " + str(len(self.results["coto"])))

        carrefour_copy = copy.deepcopy(self.clients)
        carrefour = Carrefour(
            max_time=MAX_WORKING_TIME,
            clients=carrefour_copy,
            n_queues=self.n_lines,
        )

        self.results["carrefour"] = carrefour.run().completed
        self.mean_idle["carrefour"] = np.mean(carrefour.idle_queues_in_time)
        self.dropped_clients["carrefour"] = len(carrefour.dropped_clients)
        print("Clientes atendidos en Carrefour " + str(len(self.results["carrefour"])))
