# --- Logging Configuration ---
# 10:DEBUG, 20:INFO, 30:WARNING, 40:ERROR, 50:CRITICAL
LOG_LEVEL = 10

def log_msg(level, label, message):
    if level >= LOG_LEVEL:
        time = get_time()
        tick = get_tick_count()
        formatted_msg = '[' + label + '] T:' + str(time) + ' | K:' + str(tick) + ' | ' + str(message)
        quick_print(formatted_msg)

def log_debug(message):
    log_msg(10, 'DEBUG', message)

def log_info(message):
    log_msg(20, 'INFO', message)

def log_warning(message):
    log_msg(30, 'WARN', message)

def log_error(message):
    log_msg(40, 'ERROR', message)

def log_critical(message):
    log_msg(50, 'CRITICAL', message)

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
    time1 = get_time()
    tick1 = get_tick_count()

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

    time2 = get_time()
    tick2 = get_tick_count()
    log_info('Period: ' + str(time2 - time1) + ', Ticks: ' + str(tick2 - tick1))

# --- Main --- 
def main():
    # Initialization
    change_hat(Hats.Pumpkin_Hat)
    do_a_flip()
    clear()
    print('Hello, World!')
    
    log_info('Start')

    toroidal_serpentine_traverse(harvest_and_till)

    # while True:
    #     traverse(work)

    # 6x6 pumpkin
    while True:
        plant_6x6_pumpkin()

if __name__ == "__main__":
    main()