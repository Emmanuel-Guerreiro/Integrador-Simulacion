import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as spy

from client import ClientType


class Plot:
    def plot_simulation_values(clients: List[ClientType]):
        fig, ax = plt.subplots(2)
        fig.suptitle("Parametros sistema")
        ax[0].hist([c.arrival_time for c in clients],bins=np.arange(0, 14, 0.5), align='left')
        ax[0].set_title("Arrival time")
        ax[0].set_xticks(np.arange(0, 14, 1))
        ax[0].set_xticklabels(np.arange(8, 22, 1))
        ax[1].hist([c.service_duration for c in clients], bins=np.arange(10, 22, 0.5), align='left' )
        ax[1].set_title("Service duration")
        ax[1].set_xticks(np.arange(10, 22, 1))
        ax[1].set_xticklabels(np.arange(10, 22, 1))
        fig.tight_layout()

        save_path = os.path.join(os.getcwd(), "results", "datos-sistema.png")
        plt.savefig(save_path)
        return
    
    def plot_results(data):
        fig,ax = plt.subplots()
        ax.set_title(data['title'])
        ax.plot(data['x'], data['carrefour'])
        ax.plot(data['x'], data['coto'])
        ax.set_xlabel(data['xlabel'])
        ax.set_ylabel(data['ylabel'])
        ax.legend(['Carrefour', 'Coto'])
        fig.tight_layout()
        ax.set_xticks(data['x'])
        save_path = os.path.join(os.getcwd(), "results", data['title'] + ".png")
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
        print("La distribucion es normal?")
        print(pvalue)
        return pvalue > p_value
