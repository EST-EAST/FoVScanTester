# Tolerances for deciding if the movement has to be commanded or not.
# If the distance to be covered is less than this ones, the movement will be skipped
cte_tol_x = 10      # minimum distance in motor encoder to command a movement in X direction
cte_tol_y = 10      # minimum distance in motor encoder to command a movement in Y direction
cte_tol_comp = 10   # minimum distance in motor encoder to command a movement in compensation direction

# Time to wait between steps, apart from motors and camera ones
cte_waitTime = 1
cte_stepTime = cte_waitTime * 1000

########### WINDOW TO MOTORS DEFINITIONS ################

# Mx = x
cte_lsx_min = 0  # End of LS travel in lower units
cte_lsx_scale = -(1000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lsx_max = 26900  # End of LS travel in upper units
cte_lsx_zero = 13100  # LS units coincidence with 0 mm (center)

# My = y
cte_lsy_min = 0  # End of LS travel in lower units
cte_lsy_scale = (2000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lsy_max = 39401  # End of LS travel in upper units
cte_lsy_zero = 18400  # LS units coincidence with 0 mm (center)

# Mcomp = compensaTion
cte_lscomp_min = 0  # End of LS travel in lower units
cte_lscomp_scale = -(2000 * 1000)  # LS units / mm * 1000 mm / 1 m
cte_lscomp_max = 39800  # End of LS travel in upper units
cte_lscomp_zero = 18800  # LS units coincidence with 0 mm (center)

# Home speeds
cte_vhx = 100.0
cte_vhy = 100.0
cte_vhcomp = 100.0

# Index speeds
cte_vix = 30.0
cte_viy = 30.0
cte_vicomp = 30.0

# Movement speeds
cte_vx = 100.0
cte_vy = 50.0
cte_vcomp = 30.0

###################### COMPENSATION ALGORITHM PARAMETERS ######################
# Original function ---> lscomp = (x + y) / 2
# Tunable function ---> lscomp = ((cte_comp_factor_x * x) + (cte_comp_factor_x * y)) / cte_comp_divisor
cte_comp_factor_x = 1
cte_comp_factor_y = 1
cte_comp_divisor = 2
