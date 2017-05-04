# Calibration file for repeatability tests

repeat_zero_pos = -0.01020
repeat_delta = 0.000015
repeat_tare_pos = repeat_zero_pos + repeat_delta
repeat_privilege_up = True
if repeat_privilege_up:
    repeat_prefix_pos = repeat_zero_pos
else:
    repeat_prefix_pos = repeat_tare_pos + repeat_delta

print("Calculated prefix position: " + str(repeat_prefix_pos))
