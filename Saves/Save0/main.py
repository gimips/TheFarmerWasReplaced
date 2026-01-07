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

def toroidal_serpentine_traverse(func):
	size = get_world_size()
	for y in range(size):
		for x in range(size - 1):
			func()
			if is_even(y):
				move(East)
			else:
				move(West)
		func()

		if y < size - 1:
			move(North)
	move(North)

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

def move_to(target_x, target_y):
	size = get_world_size()

	curr_x = get_pos_x()
	dx = (target_x - curr_x + size) % size

	if dx > size // 2:
		for _ in range(size - dx):
			move(West)
	else:
		for _ in range(dx):
			move(East)

	curr_y = get_pos_y()
	dy = (target_y - curr_y + size) % size

	if dy > size // 2:
		for _ in range(size - dy):
			move(South)
	else:
		for _ in range(dy):
			move(North)	

def plant_6x6_pumpkin():
	time_1 = get_time()
	tick_1 = get_tick_count()
	quick_print(time_1, tick_1)
	
	def _plant_pumpkin():
		water()
		plant(Entities.Pumpkin)

	def _replant():
		if get_entity_type() == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)
			x, y = get_pos_x(), get_pos_y()
			replant_list.append((x, y))
		
	# TODO: sort the list
	replant_list = []

	# Start to plant
	toroidal_serpentine_traverse(_plant_pumpkin)

	toroidal_serpentine_traverse(_replant)

	while True:
		if not replant_list:
			break
		
		next_replant_list = []
		for (tx, ty) in replant_list:
			move_to(tx, ty)
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
				next_replant_list.append((tx, ty))
			replant_list = next_replant_list

	# TODO: start from anywhere
	move_to(0, 0)
	harvest()

	time_2 = get_time()
	tick_2 = get_tick_count()
	quick_print(time_2, tick_2)
	quick_print('interval:', time_2 - time_1, tick_2 - tick_1)

# --- Main --- 
def main():
	# Initialization
	change_hat(Hats.Pumpkin_Hat)
	do_a_flip()
	clear()
	print('Hello, World!')

	quick_print('time, tick')
	time_i = get_time()
	tick_i = get_tick_count()
	quick_print(time_i, tick_i)

	toroidal_serpentine_traverse(harvest_and_till)

	# while True:
	#     traverse(work)

	# 6x6 pumpkin
	while True:
		plant_6x6_pumpkin()

if __name__ == "__main__":
	main()