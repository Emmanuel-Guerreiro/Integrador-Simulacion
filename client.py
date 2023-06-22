import math
from typing import Type

import numpy as np


class Client:
    def __init__(self, arrival_time: int, service_time: int) -> None:
        self.arrival_time = arrival_time
        self.service_duration: int = service_time
        self.service_start_time: int = None
        self.drop_rate: float = self.start_drop_rate()
        self.drop_time = None

    def __str__(self) -> str:
        return f"Client: arrival: {self.arrival_time} | start: {self.service_start_time} | duration: {self.service_duration} | end: {self.calc_service_end_time()} | drop: {self.drop_time} \n"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __eq__(self, other):
        """self == other"""
        if isinstance(other, Client):
            # We can only compare if `other` is a Shape as well
            return (
                self.arrival_time == other.arrival_time
                and self.service_duration == other.service_duration
            )
        return NotImplemented

    def __ne__(self, other):
        """self != other"""
        eq = Client.__eq__(self, other)
        return NotImplemented if eq is NotImplemented else not eq

    def calc_service_end_time(self) -> int:
        if self.service_start_time == None or not self.service_duration:
            return None
        return self.service_start_time + self.service_duration

    def start_drop_rate(self):
        """Generate a random number with exponential distribution"""
        return np.random.exponential(scale=1) / 1000

    def get_drop_rate(self, t: int):
        if t <= 1:
            return self.drop_rate

        return (
            math.log(1 + self.drop_rate * (t - self.arrival_time), 1000)
            if math.log(1 + self.drop_rate * (t - self.arrival_time), 1000) < 1
            else 1
        )

    def will_drop_on_time(self, t) -> bool:
        """Will drop arrived clients based on the drop rate at the
        instant t"""
        return (
            t > self.arrival_time
            and self.service_start_time is None
            and np.random.uniform(high=1, low=0) < self.get_drop_rate(t)
        )


ClientType = Type[Client]
