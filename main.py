from typing import List

import numpy as np

from client import ClientType
from simulation import Simulation
from util import Plot, Util


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
        print(f"Clients: {n}, Attenders: {n_queues}")
        simulation = Simulation(n_clients=n, n_lines=n_queues)
        simulation.init_clients(service_time_mean, 1, 1, 9)
        simulation.run()
        carrefour_clients.append(simulation.results["carrefour"])
        coto_clients.append(simulation.results["coto"])

    print("Building reports...")
    print("Carrefour: \n")
    carrefour_waiting_times = []
    for list in carrefour_clients:
        carrefour_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias_carrefour: {Util.get_means_from_values(carrefour_waiting_times)}")

    coto_waiting_times = []
    for list in coto_clients:
        coto_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias coto: {Util.get_means_from_values(coto_waiting_times)}")
    print(f"Tiempos: {n_clients}")
    print(f"Coto: \n")
    print(coto_clients)
    print(len(coto_clients[0]))
    print("--------------------------------------")
    return


def run_with_variable_queues(
    n_queues: List[int], n_clients: int, service_time_mean: int
):
    print("--------------------------------------\n")
    print("Running with variables queues: ")
    carrefour_clients: List[List[ClientType]] = []
    coto_clients: List[List[ClientType]] = []
    for q in n_queues:
        print(f"Clients: {n_clients}, Attenders: {q}")
        simulation = Simulation(n_clients=n_clients, n_lines=q)
        simulation.init_clients(service_time_mean, 1, 1, 9)
        simulation.run()
        carrefour_clients.append(simulation.results["carrefour"])
        coto_clients.append(simulation.results["coto"])

    print("Building reports...")
    print("Carrefour: \n")
    carrefour_waiting_times = []
    for list in carrefour_clients:
        carrefour_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias_carrefour: {Util.get_means_from_values(carrefour_waiting_times)}")

    coto_waiting_times = []
    for list in coto_clients:
        coto_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias coto: {Util.get_means_from_values(coto_waiting_times)}")
    print(f"Tiempos: {n_clients}")
    print(f"Coto: \n")
    print(coto_clients)
    print(len(coto_clients[0]))
    print("--------------------------------------")
    return


def run_with_all_variable(
    n_clients: List[int], n_queues: List[int], service_time_mean: int
):
    for clients in n_clients:
        run_with_variable_queues(
            n_queues=n_queues, n_clients=clients, service_time_mean=service_time_mean
        )
    for queues in n_queues:
        run_with_variable_clients(
            n_clients=n_clients, n_queues=queues, service_time_mean=service_time_mean
        )
    return


if __name__ == "__main__":
    # Clients, queues, service time mean

    # run_with_variable_clients([100, 250, 500, 750, 1000], 100, 5)
    # run_with_variable_queues([1, 2, 4, 8, 12], 100, 5)
    run_with_all_variable(
        n_queues=[1, 2, 4, 8, 12],
        n_clients=[100, 250, 500, 750, 1000],
        service_time_mean=5,
    )
