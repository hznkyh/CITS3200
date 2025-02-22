# from simulator.mtdnetwork.data.constants import MTD_DURATION, MTD_PRIORITY
from simulator.mtdnetwork.configs import config


class MTD:
    def __init__(self, name: str, mtd_type: str, resource_type: str, network=None):
        """
        :param name: name of the MTD strategy
        :param mtd_type: shuffle / diversity
        :param resource_type: application / network / reserve
        :param network: network object

        execution_time_mean: mean time for executing the implemented MTD strategy
        execution_time_std: std for executing the implemented MTD strategy
        priority: priority value of the implemented MTD strategy
        """
        self._name = name
        self._mtd_type = mtd_type
        self._resource_type = resource_type
        self._execution_time_mean = config["MTD_DURATION"][name][0]
        self._execution_time_std = config["MTD_DURATION"][name][1]
        self._priority = config["MTD_PRIORITY"][name]
        self.network = network

    def __lt__(self, other):
        return self._priority < other.get_priority()

    def __gt__(self, other):
        return self._priority > other.get_priority()

    def __le__(self, other):
        return self._priority <= other.get_priority()

    def __ge__(self, other):
        return self._priority >= other.get_priority()

    def __str__(self):
        return self._name + ' ' + self._resource_type + ' ' + str(self._execution_time_mean)

    def mtd_operation(self, adversary=None):
        raise NotImplementedError

    def get_mtd_type(self):
        return self._mtd_type

    def get_resource_type(self):
        return self._resource_type

    def get_name(self):
        return self._name

    def get_execution_time_mean(self):
        return self._execution_time_mean

    def get_execution_time_std(self):
        return self._execution_time_std

    def get_priority(self):
        return self._priority

    def set_priority(self, priority):
        self._priority = priority
