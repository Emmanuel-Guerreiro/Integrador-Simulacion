import random
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as spy

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

    def __init__(
        self,
        n_clients: int,
        n_lines: int,
        service_init_hour: int,
        service_end_hour: int,
    ) -> None:
        self.n_clients = n_clients
        self.n_lines = n_lines
        self.clients: List[Client] = []  # A stack
        self.service_init = service_init_hour
        self.service_end = service_end_hour
        self.results: dict = {}
        pass

    def init_clients(self, mean, deviation, min, max):
        services = self.init_service_times(
            mean, deviation, min, max, amount=self.n_clients
        )
        arrivals = self.init_arrival_times(
            total=self.n_clients, min_arrival=0, max_arrival=12
        )
        for i in range(len(services)):
            c = Client(arrival_time=arrivals[i], service_time=services[i])
            self.clients.append(c)

        self.sort_clients()
        return

    def generate_normal_distribution(self, mean, deviation, min, max, amount):
        """
        Generate N int values, based on a normal distribution in the range [min, max].
        """
        # When the values are cleaned (set as int and limited to the
        # valid range) the distribution may not be normal.
        # Will try again while the distribution is not normal
        iter = 0
        while True:
            s = np.rint(np.random.normal(mean, deviation, amount * 2))
            cleaned = [i for i in s if i >= min and i <= max]
            cleaned = cleaned[:amount]
            if self.is_normal_distribution(cleaned):
                return cleaned

            if iter == 100:
                raise Exception("reached: Service time generation limit")
            iter += 1

    def is_normal_distribution(self, values, p_value=0.05) -> bool:
        _, pvalue = spy.chisquare(values)
        return pvalue > p_value

    def init_service_times(self, mean, deviation, min, max, amount) -> List[int]:
        return self.generate_normal_distribution(
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
        print(f"TOTAL: {total}")
        iter = 0
        while True:
            morning = self.generate_normal_distribution(
                mean=3.647,
                deviation=1.9,
                amount=int(total),
                min=min_arrival,
                max=max_arrival,
            )
            afternoon = self.generate_normal_distribution(
                mean=10,
                deviation=1.9,
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
        print(self.clients)
        self.results["coto"] = Coto(
            clients=self.clients, n_queues=self.n_lines, max_time=MAX_WORKING_TIME
        ).run()
        pass


if __name__ == "__main__":
    main = Main(n_clients=1000, n_lines=1, service_init_hour=0, service_end_hour=12)
    main.init_clients(15, 1, 5, 30)
    main.run()

    from util import Plot

    Plot.plot_simulation_values(main.clients)
    Plot.plot_results(c_carrefour=main.results["coto"], c_coto=[])
