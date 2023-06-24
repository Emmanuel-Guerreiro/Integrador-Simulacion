import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as spy

from client import ClientType


class Plot:
    def plot_simulation_values(clients: List[ClientType], file_append: str):
        fig, ax = plt.subplots(2)
        fig.suptitle("Parametros sistema")
        ax[0].hist(
            [c.arrival_time for c in clients],
            bins=np.arange(0, 14 * 60, 30),
            align="left",
        )
        ax[0].set_title("Arrival time")
        ax[0].set_xticks(np.arange(0, 14 * 60, 60))
        ax[0].set_xticklabels(np.arange(0, 14 * 60, 60))
        ax[1].hist(
            [c.service_duration for c in clients],
            bins=np.arange(1, 11, 0.5),
            align="left",
        )
        ax[1].set_title("Service duration")
        ax[1].set_xticks(np.arange(1, 11, 1))
        ax[1].set_xticklabels(np.arange(1, 11, 1))
        fig.tight_layout()

        save_path = os.path.join(
            os.getcwd(), "results", f"datos-sistema-{file_append}.png"
        )
        plt.savefig(save_path)
        plt.close()
        return

    def plot_results(data):
        fig, ax = plt.subplots()
        ax.set_title(data["title"])
        ax.plot(data["x"], data["carrefour"])
        ax.plot(data["x"], data["coto"])
        ax.set_xlabel(data["xlabel"])
        ax.set_ylabel(data["ylabel"])
        ax.legend(["Carrefour", "Coto"])
        fig.tight_layout()
        ax.set_xticks(data["x"])
        save_path = os.path.join(os.getcwd(), "results", data["title"] + ".png")
        plt.savefig(save_path)
        plt.close()
        return


class Random:
    def __init__(self) -> None:
        pass

    def generate_normal_distribution(self, mean, deviation, min, max, amount):
        """
        Generate N int values, based on a normal distribution in the range [min, max].
        """

        s = np.rint(np.random.normal(mean, deviation, amount * 2))
        cleaned = [i for i in s if i >= min and i <= max]
        cleaned = cleaned[:amount]

        return cleaned


class Util:
    def get_means_from_values(vs: List[List[int]]) -> List[float]:
        return [np.mean(v) for v in vs]
