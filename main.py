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
        "title": f"Mean waiting time with {n_queues} servers",
        "xlabel": "Number of clients",
        "ylabel": "Attendance mean",
    }

    idle_result = {
        "x": n_clients,
        "carrefour": [],
        "coto": [],
        "title": f"Mean idle queues with {n_queues} servers",
        "xlabel": "Number of clients",
        "ylabel": "Idle servers mean",
    }

    carrefour_idle: List[float] = []
    coto_idle: List[float] = []
    carrefour_clients: List[List[ClientType]] = []
    coto_clients: List[List[ClientType]] = []
    for n in n_clients:
        print(f"Clients: {n}, Attenders: {n_queues}")
        simulation = Simulation(n_clients=n, n_lines=n_queues)
        simulation.init_clients(service_time_mean, 1, 1, 9)
        simulation.run()
        carrefour_clients.append(simulation.results["carrefour"])
        coto_clients.append(simulation.results["coto"])
        carrefour_idle.append(simulation.mean_idle["carrefour"])
        coto_idle.append(simulation.mean_idle["coto"])

    print("Building reports...")
    print("Carrefour: \n")
    carrefour_waiting_times = []
    for list in carrefour_clients:
        carrefour_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias_carrefour: {Util.get_means_from_values(carrefour_waiting_times)}")

    coto_waiting_times = []
    for list in coto_clients:
        coto_waiting_times.append([c.get_waiting_time() for c in list])

    result["carrefour"] = Util.get_means_from_values(carrefour_waiting_times)
    result["coto"] = Util.get_means_from_values(coto_waiting_times)
    Plot.plot_results(result)
    print(f"Medias coto: {Util.get_means_from_values(coto_waiting_times)}")
    print(f"Tiempos: {n_clients}")

    idle_result["carrefour"] = carrefour_idle
    idle_result["coto"] = coto_idle
    Plot.plot_results(idle_result)

    print("--------------------------------------")
    return (result["carrefour"], result["coto"])


def run_with_variable_queues(
    n_queues: List[int], n_clients: int, service_time_mean: int
):
    print("--------------------------------------\n")
    print("Running with variables queues: ")
    result = {
        "x": n_queues,
        "carrefour": [],
        "coto": [],
        "title": f"Mean waiting time with {n_clients} clients",
        "xlabel": "Number of servers",
        "ylabel": "Attendance mean",
    }

    idle_result = {
        "x": n_queues,
        "carrefour": [],
        "coto": [],
        "title": f"Mean idle queues with {n_clients} clients",
        "xlabel": "Number of servers",
        "ylabel": "Idle servers mean",
    }

    carrefour_idle: List[float] = []
    coto_idle: List[float] = []
    carrefour_clients: List[List[ClientType]] = []
    coto_clients: List[List[ClientType]] = []
    for q in n_queues:
        print(f"Clients: {n_clients}, Attenders: {q}")
        simulation = Simulation(n_clients=n_clients, n_lines=q)
        simulation.init_clients(service_time_mean, 1, 1, 9)
        simulation.run()
        carrefour_clients.append(simulation.results["carrefour"])
        coto_clients.append(simulation.results["coto"])
        carrefour_idle.append(simulation.mean_idle["carrefour"])
        coto_idle.append(simulation.mean_idle["coto"])

    print("Building reports...")
    print("Carrefour: \n")
    carrefour_waiting_times = []
    for list in carrefour_clients:
        carrefour_waiting_times.append([c.get_waiting_time() for c in list])
    print(f"Medias_carrefour: {Util.get_means_from_values(carrefour_waiting_times)}")

    coto_waiting_times = []
    for list in coto_clients:
        coto_waiting_times.append([c.get_waiting_time() for c in list])

    result["carrefour"] = Util.get_means_from_values(carrefour_waiting_times)
    result["coto"] = Util.get_means_from_values(coto_waiting_times)
    Plot.plot_results(result)

    print(f"Medias coto: {Util.get_means_from_values(coto_waiting_times)}")
    print(f"Tiempos: {n_clients}")

    idle_result["carrefour"] = carrefour_idle
    idle_result["coto"] = coto_idle
    print(idle_result)
    Plot.plot_results(idle_result)

    print("--------------------------------------")
    return


def run_with_all_variable(
    n_clients: List[int], n_queues: List[int], service_time_mean: int
):
    result_carrefour = {
        "x": n_clients,
        "y": n_queues,
        "title": "Mean waiting time carrefour",
        "xlabel": "Number of clients",
        "ylabel": "Number of servers",
        "top": None,
    }
    result_coto = {
        "x": n_clients,
        "y": n_queues,
        "title": "Mean waiting time coto",
        "xlabel": "Number of clients",
        "ylabel": "Number of servers",
        "top": None,
    }

    times_carrefour = []
    times_coto = []

    for clients in n_clients:
        run_with_variable_queues(
            n_queues=n_queues, n_clients=clients, service_time_mean=service_time_mean
        )

    for queues in n_queues:
        t_carrefour, t_coto = run_with_variable_clients(
            n_clients=n_clients, n_queues=queues, service_time_mean=service_time_mean
        )
        times_carrefour.append(t_carrefour)
        times_coto.append(t_coto)
    result_carrefour["top"] = times_carrefour
    result_coto["top"] = times_coto
    Plot.plot_3dHistogram(result_carrefour)
    Plot.plot_3dHistogram(result_coto)

    dirty_dif = np.array(times_coto) - np.array(times_carrefour)
    dif = np.where(dirty_dif >= float(0), dirty_dif, float(0))
    result_difference = {
        "x": n_clients,
        "y": n_queues,
        "title": "Mean Coto - Mean Carrefour",
        "xlabel": "Number of clients",
        "ylabel": "Number of servers",
        "top": dif,
    }

    Plot.plot_3dHistogram(result_difference)
    print(f"n_queues: {n_queues}")
    print(f"n_clients: {n_clients}")
    return


if __name__ == "__main__":

    run_with_all_variable(
        n_queues=[2, 4, 6, 8, 10, 12],
        n_clients=[200, 400, 600, 800, 1000],
        service_time_mean=5,
    )
