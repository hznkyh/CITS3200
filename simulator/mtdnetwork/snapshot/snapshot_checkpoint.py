from mtdnetwork.snapshot.network_snapshot import NetworkSnapshot
from mtdnetwork.snapshot.adversary_snapshot import AdversarySnapshot
from collections import deque


class SnapshotCheckpoint:

    def __init__(self, env=None, checkpoints=None):
        self.env = env
        print("check env is ")
        print(env)
        self._proceed_time = 0
        self._checkpoint_stack = checkpoints

    def proceed_save(self, time_network, adversary,graph_array):
        """launch an event in simulation to save snapshots by time"""
        print("proceed save", self._checkpoint_stack )
        if self._checkpoint_stack is not None:
            self._checkpoint_stack = deque(self._checkpoint_stack)
        self.env.process(self.save_snapshots_by_time(time_network, adversary,graph_array))

    def save_snapshots_by_time(self, time_network, adversary,graph_array):
        """
        :param time_network: network object to save
        :param adversary: adversary object to save
        """
        last_checkpoint = self._proceed_time
        while len(self._checkpoint_stack) > 0:
            print(f"checkpoint stack is {self._checkpoint_stack} ")
            checkpoint = self._checkpoint_stack.popleft()
            if checkpoint < last_checkpoint:
                continue
            yield self.env.timeout(checkpoint - last_checkpoint)
            last_checkpoint = checkpoint
            NetworkSnapshot().save_network_array(time_network, adversary, graph_array)
            # NetworkSnapshot().save_network(time_network, str(self.env.now + self._proceed_time))
            # AdversarySnapshot().save_adversary(adversary, str(self.env.now + self._proceed_time))

    def load_snapshots_by_time(self, time):
        self.set_proceed_time(time)
        time_network = NetworkSnapshot().load_network(str(time))
        adversary = AdversarySnapshot().load_adversary(str(time))
        return time_network, adversary

    @staticmethod
    def load_snapshots_by_network_size(size):
        time_network = NetworkSnapshot().load_network(str(size)+'n')
        adversary = AdversarySnapshot().load_adversary(str(size)+'n')
        return time_network, adversary

    @staticmethod
    def save_snapshots_by_network_size(time_network, adversary):
        NetworkSnapshot().save_network(time_network, str(time_network.get_total_nodes()) + 'n')
        AdversarySnapshot().save_adversary(adversary, str(time_network.get_total_nodes()) + 'n')

    def save_initialised(self, time_network, adversary):
        NetworkSnapshot().save_network(time_network, str(self._proceed_time))
        AdversarySnapshot().save_adversary(adversary, str(self._proceed_time))
 
    def save_to_array(self, time_network, adversary,  graph_array: list):
        '''The `save_to_array` function saves a network snapshot and an adversary snapshot to an array.
        
        Parameters
        ----------
        time_network
            The `time_network` parameter is the network object that you want to save to an array.
        graph_array : list
            The `graph_array` parameter is a list that represents a graph. It is used as an argument to the
        `save_network_array` method of the `NetworkSnapshot` class.
        adversary
            The `adversary` parameter is an optional argument that represents an adversary object. It is used
        to save the adversary snapshot in the `save_to_array` method. If an adversary object is provided, it
        will be saved using the `AdversarySnapshot().save_adversary` method.
        
        '''
        # NetworkSnapshot().save_network(time_network, str(self._proceed_time))
        NetworkSnapshot().save_network_array(time_network, str(self.env.now), graph_array)
        # AdversarySnapshot().save_adversary(adversary, str(self._proceed_time))

    def set_proceed_time(self, proceed_time):
        self._proceed_time = proceed_time

