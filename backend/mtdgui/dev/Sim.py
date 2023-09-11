from threading import Thread
import random
import simpy

# """
# Bank renege example

# Covers:

# - Resources: Resource
# - Condition events

# Scenario:
#   A counter with a random service time and customers who renege. Based on the
#   program bank08.py from TheBank tutorial of SimPy 2. (KGM)

# """


# RANDOM_SEED = 42
# NEW_CUSTOMERS = 5  # Total number of customers
# INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
# MIN_PATIENCE = 1  # Min. customer patience
# MAX_PATIENCE = 3  # Max. customer patience


# Define the callback function outside
# def external_callback(event_type, value):
#     if event_type == 'wait':
#         print(f'External Callback: Waited for {value} units of time')

def websocket_callback(msg):
    # This is a simple callback function that sends the message through the websocket
    print(f'External Callback: Waited for {msg} units of time')

# def source(env, number, interval, counter, callback):
#     for i in range(number):
#         c = customer(env, f'Customer{i:02}', counter, 12.0, callback)
#         env.process(c)
#         t = random.expovariate(1.0 / interval)
#         yield env.timeout(t)


# def customer(env, name, counter, time_in_bank, callback):
#     arrive = env.now
#     print(f'{arrive:7.4f} {name}: Here I am')

#     with counter.request() as req:
#         patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
#         results = yield req | env.timeout(patience)

#         wait = env.now - arrive

#         if req in results:
#             print(f'{env.now:7.4f} {name}: Waited {wait:6.3f}')
#             tib = random.expovariate(1.0 / time_in_bank)
#             yield env.timeout(tib)
#             print(f'{env.now:7.4f} {name}: Finished')
#         else:
#             callback('wait', wait)  # Call the external callback function here
#             print(f'{env.now:7.4f} {name}: RENEGED after {wait:6.3f}')


# def threaded_source(env, number, interval, counter, callback):
#     # This function wraps the source process for threading
#     env.process(source(env, number, interval, counter, callback))
#     env.run()


# # Setup the simulation
# print('Bank renege')

# env = simpy.Environment()
# counter = simpy.Resource(env, capacity=1)

# # Start the source function in a separate thread
# thread = Thread(target=threaded_source, args=(
#     env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, external_callback))
# thread.start()
# thread.join()



# RANDOM_SEED = 42
# NEW_CUSTOMERS = 5
# INTERVAL_CUSTOMERS = 10.0
# MIN_PATIENCE = 1
# MAX_PATIENCE = 3

# def source(env, number, interval, counter, callback):
#     for i in range(number):
#         c = customer(env, f'Customer{i:02}', counter, time_in_bank=12.0, callback=callback)
#         env.process(c)
#         t = random.expovariate(1.0 / interval)
#         yield env.timeout(t)

# def customer(env, name, counter, time_in_bank, callback):
#     arrive = env.now
#     callback("arrive", name)

#     with counter.request() as req:
#         patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
#         results = yield req | env.timeout(patience)
#         wait = env.now - arrive

#         if req in results:
#             callback("served", f"{name} waited for {wait:6.3f}")
#             tib = random.expovariate(1.0 / time_in_bank)
#             yield env.timeout(tib)
#             callback("finished", name)
#         else:
#             callback("reneged", f"{name} after waiting for {wait:6.3f}")

# def run_simulation(callback):
#     env = simpy.Environment()
#     counter = simpy.Resource(env, capacity=1)
#     env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, callback))
#     env.run()
    
# def run_simulation(callback):
#     env = simpy.Environment()
#     counter = simpy.Resource(env, capacity=1)
#     env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter, callback))
#     env.run()



RANDOM_SEED = 42
NEW_CUSTOMERS = 5
INTERVAL_CUSTOMERS = 10.0
MIN_PATIENCE = 1
MAX_PATIENCE = 3

class MySimulator:
    def __init__(self, callback=None):
        self.message = ''
        self.callback = callback
        self.env = simpy.Environment()
        self.counter = simpy.Resource(self.env, capacity=1)

    def source(self, number, interval):
        for i in range(number):
            print(f"{self.env.now:.4f} Customer{i:02}: Here I am")
            c = self.customer('Customer%02d' % i, time_in_bank=12.0)
            self.env.process(c)
            t = random.expovariate(1.0 / interval)
            yield self.env.timeout(t)

    def customer(self, name, time_in_bank):
        arrive = self.env.now
        print(f"{arrive:.4f} {name}: Here I am")
        self.set_message(f"{arrive:.4f} {name}: Here I am")

        with self.counter.request() as req:
            patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
            results = yield req | self.env.timeout(patience)

            wait = self.env.now - arrive

            if req in results:
                print(f"{self.env.now:.4f} {name}: Waited {wait:.3f}")
                self.set_message(f"{self.env.now:.4f} {name}: Waited {wait:.3f}")
                tib = random.expovariate(1.0 / time_in_bank)
                yield self.env.timeout(tib)
                print(f"{self.env.now:.4f} {name}: Finished")
                self.set_message(f"{self.env.now:.4f} {name}: Finished")
            else:
                print(f"{self.env.now:.4f} {name}: RENEGED after {wait:.3f}")
                self.set_message(f"{self.env.now:.4f} {name}: RENEGED after {wait:.3f}")

    def set_message(self, msg):
        print(f"Setting message to {msg}")
        self.message = msg
        if self.callback:
            self.callback(self.message)

    def run(self, until=10):
        self.env.process(self.source(NEW_CUSTOMERS, INTERVAL_CUSTOMERS))
        self.env.run()


sim = MySimulator(websocket_callback)
sim_thread: Thread = Thread(target=sim.run, args=())
sim_thread.start()