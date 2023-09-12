from concurrent.futures import ProcessPoolExecutor
from threading import Thread
import random
import simpy


class MySimulator:
    
    RANDOM_SEED = 42
    NEW_CUSTOMERS = 5
    INTERVAL_CUSTOMERS = 10.0
    MIN_PATIENCE = 1
    MAX_PATIENCE = 3
    
    def __init__(self, seed, callback=None, debug=False):
        self.seed = seed
        self.callback = callback
        self.debug = debug
        random.seed(self.seed)
        self.env = simpy.Environment()
        self.counter = simpy.Resource(self.env, capacity=1)
        
    def source(self, number, interval):
        for i in range(number):
            if self.debug: print(f"{self.env.now:.4f} Customer{i:02}: Here I am")
            c = self.customer('Customer%02d' % i, time_in_bank=12.0)
            self.env.process(c)
            t = random.expovariate(1.0 / interval)
            yield self.env.timeout(t)
            
    def customer(self, name, time_in_bank):
        arrive = self.env.now
        if self.debug: print(f"{arrive:.4f} {name}: Here I am")

        with self.counter.request() as req:
            patience = random.uniform(self.MIN_PATIENCE, self.MAX_PATIENCE)
            results = yield req | self.env.timeout(patience)

            wait = self.env.now - arrive

            if req in results:
                if self.debug: print(f"{self.env.now:.4f} {name}: Waited {wait:.3f}")
                tib = random.expovariate(1.0 / time_in_bank)
                yield self.env.timeout(tib)
                if self.debug: print(f"{self.env.now:.4f} {name}: Finished")
                self.callback(name, "Wait Finished",wait)
            else:
                if self.debug: print(f"{self.env.now:.4f} {name}: RENEGED after {wait:.3f}")
                if self.callback:
                    self.callback(name, "",wait)
                
    def run(self, until=10):
        self.env.process(self.source(self.NEW_CUSTOMERS, self.INTERVAL_CUSTOMERS))
        if self.debug: print(f"Running simulation until {until}")
        self.env.run(until=until)
        return f"Simulation Completed for seed {self.seed}"

# if __name__ == '__main__':
#     seeds = [random.randint(1, 1000) for _ in range(4)]  # Four random seeds for four processes

#     def reneged_notify(name, wait):
#         print(f"Notification: {name} reneged after waiting for {wait:.3f} time units.")
    
#     def process_simulation(seed):
#         sim = MySimulator(seed, callback=reneged_notify)
#         return sim.run()
    
#     with Pool() as pool:
#         results = pool.map(process_simulation, seeds)
        
#     for result in results:
#         print(result)
