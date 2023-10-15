import simpy
env = simpy.Environment()
end_time = 20
def get_time(event):


def add_events(start_time,end_time,env): 
    for i in range(start_time,end_time+1,5): 
        yield env.timeout(i-env.now)

        # event = env.timeout(i-env.now)
        # event.callbacks.append(get_time)

env.process(add_events(env=env,start_time=0,end_time=50))    
env.run(until=end_time)