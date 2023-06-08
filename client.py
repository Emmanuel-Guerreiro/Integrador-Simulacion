from typing import Type


class Client:
    def __init__(self, arrival_time: int, service_time: int) -> None:
        self.arrival_time = arrival_time
        self.service_duration: int = service_time
        self.service_start_time: int = None
        pass

    def __str__(self) -> str:
        return f"Client: arrival: {self.arrival_time} | start: {self.service_start_time} | duration: {self.service_duration} | end: {self.calc_service_end_time()} \n"

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
        if not self.service_start_time or not self.service_duration:
            return None
        return self.service_start_time + self.service_duration

    pass


ClientType = Type[Client]
