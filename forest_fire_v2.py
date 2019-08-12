# Name: Forest Fire
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
import random

# States for phases of fire development
CHAPARRAL = 0
LAKE = 1
DENSEFOREST = 2
CANYON = 3
PRE_HEATING = 4
IGNITION = 5
COMBUSTION = 6 
EXTINCTION = 7

#Select if wind is applied to grid
wind_applied = False

testing_water_prevention = False
water_x_values = (100, 140)
water_y_values = (60, 100)

def transition_func(grid, neighbourstates, neighbourcounts, decaygrid, randomgrid, terraingrid, probabilitygrid, windgrid):
    # dead = state == 0, live = state == 1
    # unpack state counts for state 0 and state 1
    probabilitygrid = np.zeros(probabilitygrid.shape)
    
                
    chaparral, lake, denseforest, canyon, pre_heating, ignition, combustion, extinction = neighbourcounts

    # unpack the state arrays
    NW, N, NE, W, E, SW, S, SE = neighbourstates
    '''
    water = (terraingrid == 1)    
    grid[water] = 1

    chaparral = (terraingrid == 0)
    grid[chaparral] 

    forest = (terraingrid == 2) & (decaygrid == 0)
    grid[forest] = 2

    cannyon = (terraingrid == 3) & (decaygrid == 0)
    grid[cannyon] = 3
    '''
    ignitable = ((terraingrid==0) | (terraingrid==2) | (terraingrid==3))
    unburnt_cells = ((grid == 0) | (grid == 2) | (grid == 3)) # cells currently in state 3
    
    
    #Number of neighbours burning
    at_least_1_neighbour = (N > 3) | (E > 3) | (S > 3) | (W > 3)
    at_least_3_neighbour = (neighbourcounts[6] >= 3) 
    #print("Neighbour counts: " , neighbourcounts[7])
    #probgrid1 = np.add(probabilitygrid, ((0.18)*neighbourcounts[4]))
    
    preheating_neighbours = np.add(probabilitygrid,  neighbourcounts[4])
    ignition_neighbours = np.add(preheating_neighbours,  2 * neighbourcounts[5])
    combustion_neighbours = np.add(ignition_neighbours,  3 * neighbourcounts[6])
    
    wind_direction = (S > 3)
    windgrid[wind_direction] += 1
    
    wind_direction = (SE > 3)
    windgrid[wind_direction] += 0.6
    
    wind_direction = (SW > 3)
    windgrid[wind_direction] += 0.6
    
    wind_direction = (NE > 3)
    windgrid[wind_direction] += 0.4
    
    wind_direction = (NW > 3)
    windgrid[wind_direction] += 0.4
    
    opposite_direction = (N > 3)
    windgrid[opposite_direction] -= 2.5
    
    if(wind_applied == False):
        for x in range(grid.shape[0]):
            for y in range(grid.shape[0]):
                windgrid[x][y] = 1
    
    probgrid2 = np.add(probabilitygrid, randomgrid)
    random_and_wind = np.multiply(probgrid2, windgrid)
    
    #probabilitygrid[forest] += 0.3
    #probabilitygrid[chaparral] +=0.8
    #probabilitygrid[cannyon] +=0.1
    '''
    n = (S>3)
    nw = (SE>3)
    ne = (SW>3)
    w = (E>3)
    e = (W>3)
    se = (NW>3)
    sw = (NE>3)
    s = (N>3)

    probabilitygrid[n] += 0.8 
    probabilitygrid[nw] += 0.5 
    probabilitygrid[ne] += 0.5 
    probabilitygrid[w] += 0.3 
    probabilitygrid[e] += 0.3 
    probabilitygrid[se] += 0.2 
    probabilitygrid[sw] += 0.2 
    probabilitygrid[s] += 0.1 

    probabilitygrid[water] = 0
    '''
    ignitable_terrain = (terraingrid != 1)
    ignited_chap = (((decaygrid == 0) & (random_and_wind > 0.35) & at_least_1_neighbour & ignitable_terrain)) | ((decaygrid == 0) & (combustion_neighbours >= 7) & ignitable_terrain)
    #ignited_forest = (((decaygrid == 0) & (probgrid2 > 0.7) & at_least_3_neighbour & ignitable_terrain ))
    grid[ignited_chap] = 4
    #grid[ignited_forest] = 4

    #burning = (decaygrid >=1)

    #burning2 = burning & direction
    




    #in_state_0 = (grid == 0) & (grid == 2) & (grid == 3) # cells currently in state 3
    '''
    above_threshold = (randomgrid > 0.35)
    all_sides_above_1 = (N > 3) | (E > 3) | (S > 3) | (W > 3) # side states > 3
    to_one = all_sides_above_1 & ignited
    grid[to_one] = 4

    #two_sides_above_1 = ((N == 4) | (S == 4)) & ((E == 4) | (W == 4))
    #to_one_again = in_state_0 & two_sides_above_1 & above_threshold
    #grid[to_one_again] = 4

    has_three_neighbours = (neighbourcounts[6]) >= 3
    engulfed = unburnt_cells & has_three_neighbours
    grid[engulfed] = 4
    '''
    

    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born
    #birth = (pre_heating >= 1) & (grid == 0)
    # if 2 or 3 live neighbours and is alive -> survives
    #survive = (pre_heating >= 1) & (grid == 1)
    # Set all cells to 0 (dead)
    #grid[:, :] = 0
    # Set cells to 1 where either cell is born or survives
    #grid[birth] = 1
   

    cells4 = (grid == 4)
    cells5 = (grid == 5)
    cells6 = (grid == 6)
    cells7 = (grid == 7)

    decaygrid[cells4] += 1
    decaygrid[cells5] += 1
    decaygrid[cells6] += 1
    decaygrid[cells7] += 1

    decay_to_one = (decaygrid == 4) 
    grid[decay_to_one] = 4
    
    #
    
    chaparral_ignition = ((decaygrid == 5) & (terraingrid == 0))
    grid[chaparral_ignition] = 5
    
    forest_ignition = (decaygrid == 5) & (terraingrid == 2)
    grid[forest_ignition] = 5
    
    canyon_ignition = (decaygrid == 5) & (terraingrid == 3)
    grid[canyon_ignition] = 5
    
    
    chaparral_combustion = (decaygrid > 6) & (terraingrid == 0)
    grid[chaparral_combustion] = 6
    
    forest_combustion = (decaygrid > 6) & (terraingrid == 2)
    grid[forest_combustion] = 6
    
    canyon_combustion = (decaygrid == 6) & (terraingrid == 3)
    grid[canyon_combustion] = 6
    
    
    chaparral_extinction = (decaygrid > 20) & (terraingrid == 0)
    grid[chaparral_extinction] = 7
    
    forest_extinction = (decaygrid > 80) & (terraingrid == 2)
    grid[forest_extinction] = 7
    
    canyon_extinction = (decaygrid > 8) & (terraingrid == 3)
    grid[canyon_extinction] = 7
    
    #
    
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire"
    config.dimensions = 2
    config.states = (CHAPARRAL, LAKE, CANYON, DENSEFOREST, PRE_HEATING, IGNITION, COMBUSTION, EXTINCTION)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.9, 0.9, 0), (0.1, 0.5, 1), (0.1, 0.3, 0.1), (0.4, 0.4, 0.4), (1, 0.5, 0), (1, 0.2, 0.2), (0.7, 0, 0), (0,0,0)]
    config.num_generations = 400
    config.grid_dims = (200,200)
    config.wrap = False
    config.initial_grid = initilise_grid(config.grid_dims)


    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config

# Initilise grid to represent terrain values
def initilise_grid(grid_size):
    #Initilise grid to be all 0's (Chaparral)
    init_grid = np.zeros(grid_size)
    
    # Set water cells
    for y in range(40, 61):
       for x in range (20, 61):
          init_grid[y][x] = 1

    # Set forest cells
    for y in range(120, 161):
        for x in range (60, 101):
           init_grid[y][x] = 2
    # Set canyon cells
    for y in range(20, 141):
        for x in range (128, 141):
           init_grid[y][x] = 3
           
    init_grid[199][0] = 4
    
    if testing_water_prevention:
        for y in range(water_y_values[0], water_y_values[1]):
            for x in range(water_x_values[0], water_x_values[1]):
                init_grid[y][x] = 1

    return init_grid

def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Initilise decay grid
    decaygrid = np.zeros(config.grid_dims)
    
    # Initilise wind grid
    windgrid = np.zeros(config.grid_dims)

    #Random Grid
    randomgrid = np.zeros(config.grid_dims)
    for x in range(randomgrid.shape[0]):
        for y in range(randomgrid.shape[0]):
            randomgrid[x][y] = random.random()

    probabilitygrid = np.zeros(config.grid_dims)
            
    #Terrain Grid
    terraingrid = np.zeros(config.grid_dims)
    
    for y in range(40, 61):
       for x in range (20, 61):
          terraingrid[y][x] = 1

   # gollum lives in this forest
    for y in range(120, 161):
        for x in range (60, 101):
           terraingrid[y][x] = 2

    for y in range(20, 141):
        for x in range (128, 141):
           terraingrid[y][x] = 3

    # Create grid object
    grid = Grid2D(config, (transition_func, decaygrid, randomgrid, terraingrid, probabilitygrid, windgrid))
    #grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
