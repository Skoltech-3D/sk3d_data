from PIL import Image
import numpy as np


def read(file, cam, mode, var='undist'):
    r"""Reads an image from Skoltech3D dataset.

    Parameters
    ----------
    file : str
        Path to the image file.
    cam : {'tis_right', 'tis_left', 'kinect_v2', 'real_sense', 'phone_right', 'phone_left'}
        Camera name.
    mode : {'rgb', 'ir', 'ir_right', 'depth'}
        Modality.
    var : {'undist', 'raw'}
        Image variant.
    Returns
    -------
    img : np.ndarray
        mode  | cam                | var    | shape           | dtype
        ----- | ------------------ | ------ | --------------- | -----
        rgb   | tis_{right,left}   | undist | [1952, 2368, 3] | uint8
              |                    | raw    | [2048, 2448, 3] |
              | kinect_v2          | undist | [1040, 1872, 3] |
              |                    | raw    | [1080, 1920, 3] |
              | real_sense         | undist | [1024, 1872, 3] |
              |                    | raw    | [1080, 1920, 3] |
              | phone_{right,left} | undist | [5280, 7104, 3] |
              |                    | raw    | [5472, 7296, 3] |
        ir    | kinect_v2          | undist |  [400,  496]    | float32 in [0, 65535] range
              |                    | raw    |  [424,  512]    |
              | real_sense         | undist |  [688, 1248]    | uint8
              |                    | raw    |  [720, 1280]    |
              | phone_{right,left} | undist |  [160,  208]    | uint32 in [0, 65535] range
              |                    | raw    |  [180,  240]    |
        depth | kinect_v2          | undist |  [400,  496]    | float32 in meters, with unknown depth denoted with NaN
              |                    | raw    |  [424,  512]    |         in mm,                                with 0
              | real_sense         | undist |  [688, 1248]    | float32 in meters,                            with NaN
              |                    | raw    |  [720, 1280]    | uint32 in mm,                                 with 0
              | phone_{right,left} | undist |  [160,  208]    | float32 in meters,                            with NaN
              |                    | raw    |  [180,  240]    | uint32 in mm,                                 with arbitrary value below 100

        For all cameras, a depth value represents the distance from the surface to the image plane
        (in contrast to the distance to the camera origin).
    """
    if (mode == 'rgb' or
        mode in {'ir', 'ir_right'}                 and cam in {'real_sense', 'phone_right', 'phone_left'} or
        mode == 'depth'            and var =='raw' and cam in {'real_sense', 'phone_right', 'phone_left'}):
        return read_img(file)
    elif (mode == 'depth' or
          mode == 'ir' and cam == 'kinect_v2'):
        return read_f32(file)
    else:
        raise ValueError(f'Invalid parameters {cam} {mode} {var}')


def read_img(file):
    r"""Reads an RGB, IR, or depth image from PNG or JPEG.

    Parameters
    ----------
    file : str
        Path to the image file.

    Returns
    -------
    img : np.ndarray
        of shape [width, height], or [width, height, 3], or [width, height, 4] and dtype uint8,
        or of shape [width, height] and dtype int32 (converted from uint16).
    """
    return np.asarray(Image.open(file))


def read_f32(file):
    r"""Reads a float32 image packed into RGBA.

    Parameters
    ----------
    file : str
        Path to the image file.

    Returns
    -------
    img : np.ndarray
        of shape [height, width] and dtype float32,
    """
    img = np.asarray(Image.open(file))
    img = unpack_float32(img)
    return img


def unpack_float32(ar8):
    r"""Unpacks an array of little-endian byte quadruplets back to the array of float32 values.

    Parameters
    ----------
    ar8 : np.ndarray
        of shape [**, 4].

    Returns
    -------
    ar : np.ndarray
        of shape [**]
    """
    return ar8.ravel().view('<f4').reshape(ar8.shape[:-1])
