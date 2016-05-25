import subprocess

import gphoto2 as gp

def capture(downloadPath, resultFile, showImage):
    context = gp.gp_context_new()
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera, context))
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE, context))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = downloadPath+"/"+resultFile
    print('Copying image to', target)
    camera_file = gp.check_result(gp.gp_camera_file_get(            
        camera, file_path.folder, file_path.name,
        gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(camera_file, target))
    if (showImage):
        subprocess.call(['xdg-open', target])
    gp.check_result(gp.gp_camera_exit(camera, context))
    return True
