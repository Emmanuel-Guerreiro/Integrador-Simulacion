import typing


class Client:
    def __init__(self, arrival_time: int, service_time: int) -> None:
        self.arrival_time = arrival_time
        self.service_duration: int = service_time
        self.service_start_time: int = None
        pass

    def __str__(self) -> str:
        return f"Client: arrival: {self.arrival_time} | start: {self.service_start_time} | duration: {self.service_duration}"

    def calc_service_end_time(self) -> int:
        return self.service_start_time + self.service_start_time

    pass
