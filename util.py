import os
from typing import List

import matplotlib.pyplot as plt

from client import ClientType


class Plot:
    def plot_simulation_values(clients: List[ClientType]):
        fig, ax = plt.subplots(2)
        fig.suptitle("Tiempos del sistema")
        ax[0].hist([c.arrival_time for c in clients])
        ax[0].set_title("Tiempo de llegada")
        ax[1].hist([c.service_duration for c in clients])
        ax[1].set_title("Duracion del servicio")
        fig.tight_layout()

        save_path = os.path.join(os.getcwd(), "results", "datos-sistema.png")
        plt.savefig(save_path)
        return

    def plot_results(c_carrefour: List[ClientType], c_coto: List[ClientType]):
        fig, axs = plt.subplots(3, 2)
        fig.suptitle("Resultados de la simulacion")
        for ax in axs[0]:
            ax.hist([c.calc_service_end_time() for c in c_carrefour])
        fig.tight_layout()
        save_path = os.path.join(os.getcwd(), "results", "resultados.png")
        plt.savefig(save_path)
        return
