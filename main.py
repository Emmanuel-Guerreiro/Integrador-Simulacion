from typing import List

import numpy as np

from client import ClientType
from simulation import Simulation


def get_means_from_values(vs: List[List[int]]) -> List[float]:
    return [np.mean(v) for v in vs]


def run_with_variable_clients(
    n_clients: List[int], n_queues: int, service_time_mean: int
):
    print("--------------------------------------\n")
    print("Running with variables clients: ")
    result = {
        "x": n_clients,
        "carrefour": [],
        "coto": [],
        "title": "Number of clients variable",
        "xlabel": "Number of clients",
        "ylable": "Attendance mean",
    }
    carrefour_clients: List[List[ClientType]] = []
    coto_clients: List[List[ClientType]] = []
    for n in n_clients:
        print(n)
        simulation = Simulation(
            n_clients=n, n_lines=n_queues, service_init_hour=0, service_end_hour=12
        )
        simulation.init_clients(service_time_mean, 1, 5, 30)
        simulation.run()
        carrefour_clients.append(simulation.results["carrefour"])
        coto_clients.append(simulation.results["coto"])

    print("Building reports...")
    print("Carrefour: \n")
    carrefour_waiting_times = []
    for list in carrefour_clients:
        carrefour_waiting_times.append(
            [c.service_start_time - c.arrival_time for c in list]
        )
    print(f"Medias_carrefour: {get_means_from_values(carrefour_waiting_times)}")

    coto_waiting_times = []
    for list in coto_clients:
        coto_waiting_times.append([c.service_start_time - c.arrival_time for c in list])
    print(f"Medias coto: {get_means_from_values(coto_waiting_times)}")
    print(f"Tiempos: {n_clients}")
    print(f"Coto: \n")
    print(coto_clients)
    print("--------------------------------------")

    return


if __name__ == "__main__":

    run_with_variable_clients([10, 20, 30], 2, 15)
