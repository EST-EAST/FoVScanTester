# -*- coding: utf-8 -*-
"""
Scan execution configuration file example.
Copy it as scanconfig.py and taylor it to your needs.
"""

# ### Simulator connection
cte_use_motorsim = True            # Enables the simulator mode

cte_test_protocol = False   # Enables the engineering mode to only test the protocol

if (cte_test_protocol):
    cte_enable_motors_first = False     # Sends a command to enable the motors before performing the scan
    cte_disable_motors_first = True     # Sends a command to disable the motors before performing the scan
    cte_reset_motors_first = True       # Sends a command to the motors (home and center operation) before performing the scan
    cte_home_motors_first = False      	# Sends a command to the motors (home operation) before performing the scan
    cte_command_np_flags = True         # Enables the sending of NP commands to the motors
    cte_wait_for_p = False              # Waits for P answers from the motors
    cte_sim_disable_untimely_resp = True    # Disables the untimely response of P
else:
    cte_enable_motors_first = False     # Sends a command to enable the motors before performing the scan
    cte_disable_motors_first = False    # Sends a command to disable the motors before performing the scan
    cte_reset_motors_first = False      # Sends a command to the motors (home and center operation) before performing the scan
    cte_home_motors_first = True      	# Sends a command to the motors (home operation) before performing the scan
    cte_command_np_flags = True         # Enables the sending of NP commands to the motors
    cte_wait_for_p = True               # Waits for P answers from the motors
    cte_sim_disable_untimely_resp = False   # Disables the untimely response of P


# ### Hardware device configuration
cte_proto_rev = 2  # Prototype revision.

# ### Timing configuration
cte_stabilization_time = 2.000  # Stabilization time that actuates when no picture is taken.
cte_step_delay_time = 0.000 	# Pause time between steps
cte_step_wait_for_key = False   # Pause until a key is received

# ### Reporting configuration
cte_export_ods = False      # Creates a report in ODS format (for Linux platforms)
cte_export_openpyxl = False  # Creates a report in XLSX format (for Windows platforms)
cte_upload_web = False      # [DOESN'T WORK] Uploads the results to the Scan Configuration web.


# ### Algorithm source web
# cte_web_root = "http://fijar.ll.iac.es/fovscan"   # Scan Configuration web to retrieve algorithms from.
cte_web_root = "http://fovscan.gatatac.org"       # Scan Configuration web to retrieve algorithms from.
# cte_web_root = "http://localhost:3000"              # Scan Configuration web to retrieve algorithms from.
# ### Motors Connection configuration
cte_use_socket = True   # If True it uses a XPort TCP socket to communicate with motors, serial link otherwise

if not (cte_use_socket):
    # Serial connection configuration
    import os

    if (os.name == 'nt'):
        cte_serial_port = 'COM4:'   # Serial link port for windows machines
    else:
        cte_serial_port = '/dev/ttyUSB0'   # Serial link port for Linux machines
    if (cte_use_motorsim):
        if (os.name == 'nt'):
            # In case of using the simulator, the loopback serial link port for Windows machines
            cte_serial_port_loopback = 'COM5:'
        else:
            # In case of using the simulator, the loopback serial link port for Linux machines
            cte_serial_port_loopback = '/dev/ttyUSB1'

else:
    # TCP connection configuration
    import socket

    cte_socket_port = 10001     # TCP port for the connection
    if not (cte_use_motorsim):
        cte_socket_ip = "192.168.90.105"    # IP for TCP connection
    else:
        cte_socket_ip = socket.gethostname()    # If using simulator, IP for the simulator machine


# ### Motor configuration
cte_motor_x = 1     # Index of the X motor in the motor list
cte_motor_y = 2     # Index of the y motor in the motor list
cte_motor_comp = 3  # Index of the Comp motor in the motor list
cte_motor_x_xport = 22  # XPort Index of the X motor in the motor list
cte_motor_y_xport = 23  # XPort Index of the Y motor in the motor list
cte_motor_comp_xport = 24 # XPort Index of the Comp motor in the motor list
cte_use_motor_x = True      # Enables the X motor
cte_use_motor_y = True      # Enables the Y motor
cte_use_motor_comp = True   # Enables the Comp motor

# If 0, then the motor that is expected to take longer is asked to provide a 'p', while others use polling strategy
# If 1, then the X motor is asked to provide a 'p', while others use polling strategy
# If 2, then the Y motor is asked to provide a 'p', while others use polling strategy
# If >=3, then the Comp motor is asked to provide a 'p', while others use polling strategy
cte_force_wait_for_motor = 0

cte_force_wait_bit_x = False        # Force waiting position attained bit on motor x
cte_force_wait_bit_y = False        # Force waiting position attained bit on motor y
cte_force_wait_bit_comp = False     # Force waiting position attained bit on motor z

# Answer mode of the controller
cte_mode_answ = 1

# ### App configuration
cte_verbose = False         # Activates verbose mode of the App
cte_fileprefix = "frame"    # Prefix for the camera files

# ### Camera configuration
cte_use_cvcam = False       # Activates the use of an OpenCV managed video camera

if cte_use_cvcam:
    cte_camsource = 0       # Camera ID for OpenCV handler.
    cte_framePath = "./00_acquired/"    # Path for OpenCV acquired images

cte_use_photocam = False    # Activates the use of PhotoCam managed photo cameras

if cte_use_photocam:
    # cte_cameractrl_path = "C:\\Program Files (x86)\\digiCamControl\\"
    cte_cameractrl_path = ""    # Path for CameraControl comamnd binary files
    cte_cameractrl_command = "CameraControlCmd.exe"     # Name of the CameraControl binary file
    cte_cameractrl_capturecmd = "/capture"              # Command for capture a picture
    cte_cameractrl_filenamecmd = "/filename"            # Command for setting the filename
    cte_cameractrl_filename_root = "FoV"                # Filename name root for storing the images.

cte_use_gphoto2 = False     # Activates the use of GPhoto2 managed photo cameras

if cte_use_gphoto2:
    cte_gphoto2_framePath = "./00_acquired/"            # Path for GPhoto2 acquired images
    cte_gphoto2_filename_root = "FoV"                   # Filename name root for storing the images.

cte_second_picture = False  # Enables taking a secondary picture before leaving current position.

if cte_second_picture:
    cte_stabilization_time_pic2 = 4.000  # Stabilization time for pic 2


cte_command_gcs_dcp = True
if cte_command_gcs_dcp:
    cte_command_gcs_scale = 10000000
    cte_command_gcs = True
    cte_command_gcs_tcp = False
else:
    cte_command_gcs_tcp = False     # Enables commanding the system through GCS system
    if cte_command_gcs_tcp:
        cte_command_gcs = True
        cte_command_gcs_tcp_ip = socket.gethostname() # localhost
        cte_command_gcs_tcp_port = 2001 # DCP
        cte_command_gcs_tcp_scale = 10000000

