import random
import simpy

class Kitchen:
    def __init__(self, env, num_chefs):
        self.env = env
        self.chefs = simpy.Resource(env, num_chefs)

    def prepare_dish(self, dish):
        prep_time = random.uniform(5, 15)
        yield self.env.timeout(prep_time)
        print(f"Prepared {dish} in {prep_time:.2f} minutes at {self.env.now:.2f}")

def customer(env, name, kitchen):
    print(f"Customer {name} arrives at {env.now:.2f}")
    with kitchen.chefs.request() as request:
        yield request
        yield env.process(kitchen.prepare_dish(name))
        print(f"Customer {name} leaves at {env.now:.2f}")

def setup(env, num_chefs):
    kitchen = Kitchen(env, num_chefs)
    for i in range(5):
        env.process(customer(env, f"Dish {i+1}", kitchen))
        yield env.timeout(random.uniform(1, 10))

if __name__ == '__main__':
    env = simpy.Environment()
    env.process(setup(env, 2))
    env.run(until=60)
