from __builtins__ import *

# --- Configuration & Constants ---
WATER_THRESHOLD = 0.75

# --- Utilities ---
 
def smart_harvest():
	if can_harvest():
		harvest()

def harvest_and_till():
	smart_harvest()
	till()

def is_even(n): 
	return n % 2 == 0

def traverse(func):
	size = get_world_size()
	for i in range(size):
		for j in range(size):
			func()
			move(North)
		move(East)

def water():
	if get_water() < WATER_THRESHOLD and num_items(Items.Water) > 0:
		use_item(Items.Water)

def work():
	water()
	smart_harvest()

	x, y=get_pos_x(), get_pos_y()
	if is_even(x + y):
		plant(Entities.Tree)
	elif x == 0:
		plant(Entities.Grass)
	else:
		plant(Entities.Carrot)

# TODO: add last replant mark
def plant_6x6_pumpkin():
	time_1 = get_time()
	tick_1 = get_tick_count()
	quick_print(time_1, tick_1)
	
	state = {'replanted': False}
	def _plant_pumpkin():
		water()
		plant(Entities.Pumpkin)

	def _replant():
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			state['replanted'] = True
		
	traverse(_plant_pumpkin)

	while True:
		state['replanted'] = False
		traverse(_replant)

		if not state['replanted']:
			harvest()
			break

	time_2 = get_time()
	tick_2 = get_tick_count()
	quick_print(time_2, tick_2)

# --- Main --- 
def main():
	# Initialization
	change_hat(Hats.Pumpkin_Hat)
	do_a_flip()
	clear()
	print('Hello, World!')

	time_i = get_time()
	tick_i = get_tick_count()
	quick_print(time_i, tick_i)

	traverse(harvest_and_till)

	# while True:
	#     traverse(work)

	# 6x6 pumpkin
	while True:
		plant_6x6_pumpkin()

if __name__ == "__main__":
	main()