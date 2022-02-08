# https://smlee729.github.io/python/simulation/2015/04/28/1-monty-hall.html
import random

doors = [1,2,3]

N = 10000
success_count = 0

def monty_door_random(doors, alice_door, prize_door):
    monty_door = random.choice(doors)
    return monty_door

def monty_door_avoid_prize(doors, alice_door, prize_door):
    candidates = list(set(doors) - {prize_door})
    monty_door = random.choice(candidates)
    return monty_door

def monty_door_avoid_alice(doors, alice_door, prize_door):
    candidates = list(set(doors) - {alice_door})
    monty_door = random.choice(candidates)
    return monty_door

def monty_door_avoid_both(doors, alice_door, prize_door):
    candidates = list(set(doors) - {prize_door, alice_door})
    monty_door = random.choice(candidates)
    return monty_door


for i in range(N):
    alice_door = random.choice(doors)
    prize_door = random.choice(doors)
    #month_door = monty_door_random(doors, alice_door, prize_door)
    monty_door = monty_door_avoid_both(doors, alice_door, prize_door)
    remaining_doors = set(doors) - {alice_door} - {monty_door}
    alice2_door = random.choice(list(remaining_doors)) 
    success = alice_door == prize_door
    #print(f"{prize_door}{alice_door}{monty_door} prize={prize_door} alice1={alice_door} monty={monty_door} alice2={alice2_door} success={success}")
    if success:
        success_count += 1

f = success_count / N
print(f)

    
