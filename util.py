import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as spy

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

        axs[0][0].hist([c.calc_service_end_time() for c in c_carrefour])
        axs[0][1].hist([c.calc_service_end_time() for c in c_coto])
        fig.tight_layout()
        save_path = os.path.join(os.getcwd(), "results", "resultados.png")
        plt.savefig(save_path)
        return


class Random:
    def __init__(self) -> None:
        pass

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

            if iter == 10000:
                raise Exception("reached: Service time generation limit")
            iter += 1

    def is_normal_distribution(self, values, p_value=0.05) -> bool:
        _, pvalue = spy.chisquare(values)
        return pvalue > p_value
