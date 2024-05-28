import numpy as np


def open_rtv(fname):
    """
    the function read the binary file of the fast-frame xrapid camera
    :param fname: file name
    :return:
    numpy array (4,1024,1360)
    4 frames
    """
    file = open(fname, 'rb')
    n = 1024 * 1360
    file_array = np.fromfile(file, dtype='uint16', offset=0x2000, count=n * 4).reshape((4, 1024, 1360))
    ar_right = np.copy(file_array[1::2, :, :1360 // 2])
    ar_left = np.copy(file_array[1::2, :, 1360 // 2:])
    file_array[1::2, :, :1360 // 2] = ar_left
    file_array[1::2, :, 1360 // 2:] = ar_right

    image_array = np.copy(file_array)
    image_array = np.nan_to_num(image_array)
    file.close()
    return image_array
