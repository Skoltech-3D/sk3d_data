# Skoltech3D
This repository describes the structure and format of the Skoltech3D dataset and provides utilities for working with the data.

> **Multi-sensor large-scale dataset for multi-view 3D reconstruction**  
  Oleg Voynov, Gleb Bobrovskikh, Pavel Karpyshev, Saveliy Galochkin, Andrei-Timotei Ardelean, Arseniy Bozhenko, Ekaterina Karmanova, Pavel Kopanev, Yaroslav Labutin-Rymsho, Ruslan Rakhimov, Aleksandr Safin, Valerii Serpiva, Alexey Artemov, Evgeny Burnaev, Dzmitry Tsetserukou, Denis Zorin  
  *CVPR 2023*  
  **[Project page](https://skoltech3d.appliedai.tech/)&nbsp;|
    [Paper (6 MB)](https://skoltech3d.appliedai.tech/data/skoltech3d.pdf)&nbsp;|
    [Supplementary text (2 MB)](https://skoltech3d.appliedai.tech/data/skoltech3d_supp.pdf)&nbsp;|
    [Supplementary results (101 MB)](https://skoltech3d.appliedai.tech/data/skoltech3d_supp_results.pdf)&nbsp;|
    [arXiv](https://arxiv.org/abs/2203.06111)**



## Table of contents
- [Overview](#overview)
- [Structured-light data](#structured-light-data)
- [Image data](#image-data)
- [Calibration](#calibration)
- [Addons](#addons)
  - [Alternative calibration formats](#alternative-calibration-formats)
  - [Structured-light depth maps](#structured-light-depth-maps)
  - [Other reprojected depth maps](#other-reprojected-depth-maps)
- [ScenePaths](#scenepaths)
- [Download](#download)
- [Evaluation](#evaluation)
- [Changelog](#changelog)



## Overview
The dataset consists of 107 scenes scanned with 
- RangeVision Spectrum structured-light scanner,
- 2x The Imaging Source DFK 33UX250 industrial RGB cameras,
- 2x Huawei Mate 30 Pro phones with time-of-flight depth sensors,
- Intel RealSense D435 stereo RGB-D camera,
- and Microsoft Kinect v2 ToF RGB-D camera.

Previews of the scenes are available in the [supplementary results](https://skoltech3d.appliedai.tech/data/skoltech3d_supp_results.pdf)
for the paper, and the list of scene names can be found at [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1).

The data for each scene consists of
- a highly accurate reference structured-light scan in the form of mesh and depth maps,
- RGB and infra-red images and lower-quality depth maps from the cameras, captured from 100 points of view, under 14 lighting conditions,
- intrinsic camera parameters and camera positions,
- and additional data, such as occluding surface, as described further.

A detailed overview of the provided data is available in the
["Skoltech3D data"](https://docs.google.com/spreadsheets/d/1yWBtM93OdQHrsSKVG9Jp9t1Bz9FIOfJhDPLDPkcTXxo)
spreadsheet and is explained below.



## Structured-light data
The structured-light (SL) data for each scene consists of
- the reference merged and cleaned full structured-light scan,
- 27 raw partial scans,
- 5 validation partial scans, if the temporary coating was used for the scene,
- and the occluding surface, described in paragraph
  ["Rendering SL scans. Occluding surface"](https://skoltech3d.appliedai.tech/data/skoltech3d.pdf#%5B%7B%22num%22%3A14%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C49.112%2C721%2Cnull%5D)
  in the paper.

The paths to the files are
```
Data              | Path
------------------|-----
Full scan         | dataset/{scene}/stl/reconstruction/cleaned.ply
Partial scans     | dataset/{scene}/stl/partial/aligned/{scan_i:04}.ply
Validation scans  | dataset/{scene}/stl/validation/aligned/{val_scan_i:04}.ply
Occluding surface | dataset/{scene}/stl/occluded_space.ply
```
where
- `scene` is the name of the scene from [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1),
- `scan_i` is the id of the partial scan from `0..26`,
- and `val_scan_i` is the id of the validation partial scan from `0..4`.

The structured-light data is stored as triangle meshes in binary PLY format, which can be opened in [MeshLab](https://www.meshlab.net),
or loaded using [Open3D](http://www.open3d.org/docs/0.17.0/python_api/open3d.io.read_triangle_mesh.html#open3d.io.read_triangle_mesh).



## Image data
The image data for each scene consists of the images captured from 100 viewpoints with
the right and left The Imaging Source (TIS) cameras,
the right and left phone cameras,
and the RealSense and Kinect cameras.

The paths to the files are
```
Data                                     | Path
---------------------------------------- |-----
Undistorted images, lighting-dependent   | dataset/{scene}/{cam}/{mode}/undistorted/{light}/{pos_i:04}.{ext}
Undistorted images, lighting-independent | dataset/{scene}/{cam}/{mode}/undistorted/{pos_i:04}.{ext}
Raw images, lighting-dependent           | raw/{scene}/{cam}/{mode}/raw/{light}/{pos_i:04}.{ext}
Raw images, lighting-independent         | raw/{scene}/{cam}/{mode}/raw/{pos_i:04}.png
```
where
- `scene` is the name of the scene from [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1),
- `cam` is the name of the camera from `tis_right`, `tis_left`, `kinect_v2`, `real_sense`, `phone_right`, and `phone_left`,
- `mode` is the name of the modality from `rgb`, `depth`, `ir`, and `ir_right`,
- `light` is the name of the lighting condition, as explained below,
- `pos_i` is the id of the viewpoint from `0..99`,
- and `ext` is `png`, except for the RGB images from `phone_right` and `phone_left`, for which it is `jpg`.

We captured RGB images with all the devices,
depth images with the two phones, the Kinect, and the RealSense,
and infra-red (IR) images with the two phones, the Kinect, and the left and right IR sensors of the RealSense.

We captured RGB images with all devices, and all modalities with the RealSense,
under 12 lighting conditions, denoted in [`params.py:1`](/src/sk3d/data/dataset/params.py#L1) as `{lighting_condition}@best`.
For two of the lighting conditions, denoted as `ambient_low@fast` and `flash@fast`,
we additionally captured the images with camera settings corresponding to a high level of noise,
as explained in paragraph
["Sensor exposure/gain selection"](https://skoltech3d.appliedai.tech/data/skoltech3d.pdf#%5B%7B%22num%22%3A12%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C49.112%2C721%2Cnull%5D)
in the paper.
For the Kinect, since controlling the camera settings was not possible,
the two additional lighting conditions are not available,
and the available lighting conditions are labeled without the suffix `best` of `fast`,
as in [`params.py:6`](/src/sk3d/data/dataset/params.py#L6).

The time-of-flight depth sensors of the Kinect and the phones are unaffected by the lighting conditions,
so we captured the depth and IR images for these cameras once per viewpoint.

For each image, we provide an undistorted version and the raw unprocessed version.

The images are stored as either regular PNG with lossless compression,
or lossy JPEG in case of RGB images from the phones,
or PNG with each RGBA pixel representing a little-endian 32-bit floating point value.
Please refer to [`imgio.py:5`](/src/sk3d/data/io/imgio.py#L5) for more details on the format of the images,
and to [`load_imgs.ipynb`](/examples/load_imgs.ipynb) for a code example for loading the images.



## Calibration
The calibration data consists of
- camera poses in the global space of the SL data for each scene, after the refinement described in paragraph
  ["Refinement of camera poses"](https://skoltech3d.appliedai.tech/data/skoltech3d.pdf#%5B%7B%22num%22%3A234%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C49.112%2C721%2Cnull%5D)
  in the paper,
- pinhole camera models, corresponding to the undistorted images,
- central generic camera models, corresponding to the raw images,
- and depth undistortion models, described in paragraph
  ["Refinement of depth camera calibration"](https://skoltech3d.appliedai.tech/data/skoltech3d.pdf#%5B%7B%22num%22%3A234%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C49.112%2C721%2Cnull%5D)
  in the paper.

The paths to the files are
```
Data                       | Path
-------------------------- |-----
Camera poses               | dataset/{scene}/{cam}/{mode}/images.txt
Pinhole camera models      | dataset/calibration/{cam}/{mode}/cameras.txt
Central generic cam models | dataset/calibration/{cam}/{mode}/intrinsics.yaml
Depth undistortion models  | dataset/calibration/{cam}/{mode}/undistortion.pt
```
where
- `scene` is the name of the scene from [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1),
- `cam` is the name of the camera from `tis_right`, `tis_left`, `kinect_v2`, `real_sense`, `phone_right`, and `phone_left`,
- and `mode` is the name of the modality from `rgb`, `ir`, and `ir_right`.

The camera parameters of the `ir` sensors correspond to both the IR and the depth images.

The camera poses and the pinhole camera models are stored in the [COLMAP text format](https://colmap.github.io/format.html#text-format).
The central generic camera models are stored in the format of
[Thomas Schöps' camera calibration toolbox](https://github.com/puzzlepaint/camera_calibration#how-to-use-generic-camera-models-in-your-application).



## Addons
### Alternative calibration formats
For the undistorted RGB images from `tis_right` camera,
we provide the camera parameters in two additional formats:
- in [MVSNet format](https://github.com/YoYo000/MVSNet#file-formats),
- and in [IDR format](https://github.com/lioryariv/idr/blob/main/DATA_CONVENTION.md),
  commonly used in works on NeRF-based 3D reconstruction.

The paths to the files are
```
Data                    | Path
----------------------- |-----
MVSNet                  |
  Camera parameters     | addons/{scene}/{cam}/{mode}/mvsnet_input/{pos_i:08}_cam.txt
  View selection scores | addons/{scene}/{cam}/{mode}/mvsnet_input/pair.txt
IDR                     | addons/{scene}/{cam}/{mode}/idr_input/cameras.npz
```
where
- `scene` is the name of the scene from [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1),
- `cam` is the name of the camera --- `tis_right`,
- `mode` is the name of the modality --- `rgb`,
- and `pos_i` is the id of the viewpoint from `0..99`.

In addition to the standard fields in the IDR `cameras.npz`,
we provide the field `cam_dict['roi_box_{pos_i}'] = left, right, top, bottom`,
which represents the bounding box of the object in the image in pixels
(precisely, the bounding box of the projection of the SL scan).

Also note that the MVSNet view selection scores in `pair.txt`,
and consequently the neighboring source views for multi-view stereo matching,
can be calculated in various ways.
We calculated the scores following the algorithm described in paragraph
["View Selection"](https://arxiv.org/pdf/1804.02505.pdf#subsection.1.4.1) in the MVSNet paper,
with the original parameters and using the vertices of the SL scan instead of the SfM reconstruction.



### Structured-light depth maps
In addition to the SL scans as triangle meshes, we provide the depth maps rendered from the scans at the image spaces of
the undistorted RGB images from both TIS cameras,
and the undistorted depth maps from each camera.

The paths to the files are
```
Data                      | Path
------------------------- |-----
Rendered w/o antialiasing | addons/{scene}/proj_depth/stl.clean_rec@{sensor}.undist/{pos_i:04}.png
        with antialiasing | addons/{scene}/proj_depth/stl.clean_rec.aa@{sensor}.undist/{pos_i:04}.png
```
where
- `scene` is the name of the scene from [`scenes.py:1`](/src/sk3d/data/dataset/scenes.py#L1),
- `sensor` is the name of the sensor from `tis_right`, `tis_left`,
  `kinect_v2_ir`, `real_sense_ir`, `phone_right_ir`, and `phone_left_ir`,
- and `pos_i` is the id of the viewpoint from `0..99`.

For each depth map we provide a version rendered without antialiasing in `stl.clean_rec@...`,
and a version rendered with antialiasing in `stl.clean_rec.aa@...`,
which may better correspond to low-quality sensor depth maps.

The images are stored as PNG files with each RGBA pixel representing a little-endian 32-bit floating point value.
Please refer to [`imgio.py:75`](/src/sk3d/data/io/imgio.py#L75) for more details on the format,
and to [`load_sl_depth.ipynb`](/examples/load_sl_depth.ipynb) for a code example for loading the depth maps.



### Other reprojected depth maps
![](https://img.shields.io/static/v1?label=&message=Coming%20soon&color=yellow)

You can also find code examples for rendering an SL scan to an arbitrary image space,
and for reprojecting a low-quality sensor depth map to an arbitrary image space
in [`render_sl_depth.ipynb`](/examples/render_sl_depth.ipynb) and [`reproject_depth.ipynb`](/examples/reproject_depth.ipynb)
respectively.



## ScenePaths
For convenience, we provide a python retriever of paths to the files from the dataset [`scene_paths.py:1`](/src/sk3d/data/dataset/scene_paths.py#L1).
Please refer to [`load_imgs.ipynb`](/examples/load_imgs.ipynb) or [`load_sl_depth.ipynb`](/examples/load_sl_depth.ipynb)
for some examples of its usage,
and to the column ["ScenePaths code"](https://docs.google.com/spreadsheets/d/1yWBtM93OdQHrsSKVG9Jp9t1Bz9FIOfJhDPLDPkcTXxo/edit#gid=0&range=H:H)
in the "Skoltech3D data" spreadsheet for the correspondence between the pieces of the dataset and the methods of this class.



## Download
You can download the dataset on the [skoltech3d.appliedai.tech/data](https://skoltech3d.appliedai.tech/data/) page.
The dataset is split into ZIP archives of sizes up to 25 GB based on the sensor, data modality, the scene, etc.
Please refer to the column ["Chunk file"](https://docs.google.com/spreadsheets/d/1yWBtM93OdQHrsSKVG9Jp9t1Bz9FIOfJhDPLDPkcTXxo/edit#gid=0&range=E:E)
in the "Skoltech3D data" spreadsheet for the correspondence between the pieces of the dataset and the names of the ZIP files.

![](https://img.shields.io/static/v1?label=&message=Coming%20soon&color=yellow)

For convenience, we provide a python downloader to download specific parts of the dataset. 



## Evaluation
![](https://img.shields.io/static/v1?label=&message=Coming%20soon&color=yellow)

To evaluate a 3D reconstruction method on Skoltech3D please follow the instructions on the [evaluation](/docs/evaluation.md) page.



## Changelog
#### 2023 Aug 16
- Initial release of the documentation.
