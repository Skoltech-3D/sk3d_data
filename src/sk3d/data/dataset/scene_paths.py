class ScenePaths:
    def __init__(self, scene_name, *, addons_dir=None, data_dir=None, raw_dir=None):
        self.scene_name = scene_name
        self.addons_dir = addons_dir
        self.data_dir = data_dir
        self.raw_dir = raw_dir

    # Structured light
    # ----------------
    def sl_full(self):
        return f'{self.data_dir}/{self.scene_name}/stl/reconstruction/cleaned.ply'

    def sl_part(self, scan_i, var='ref'):
        if var == 'ref':    return f'{self.data_dir}/{self.scene_name}/stl/partial/aligned/{scan_i:04}.ply'
        elif var == 'val':  return f'{self.data_dir}/{self.scene_name}/stl/validation/aligned/{scan_i:04}.ply'

    def sl_occ(self):
        return f'{self.data_dir}/{self.scene_name}/stl/occluded_space.ply'

    # Images
    # ------
    def img(self, cam, mode, pos_i, light=None, var='undist'):
        if var == 'raw':  base_dir = self.raw_dir
        else:             base_dir = self.data_dir
        base_dir = f'{base_dir}/{self.scene_name}/{cam}/{mode}'
        if var == 'raw':       base_dir = f'{base_dir}/raw'
        elif var == 'undist':  base_dir = f'{base_dir}/undistorted'

        if light is not None:  base_dir = f'{base_dir}/{light}'

        if cam.startswith('phone') and (mode == 'rgb'):  ext = 'jpg'
        else:                                            ext = 'png'

        return f'{base_dir}/{pos_i:04}.{ext}'

    # Calibration
    # -----------
    def cam_poses(self, cam, mode):
        return f'{self.data_dir}/{self.scene_name}/{cam}/{mode}/images.txt'

    def cam_model(self, cam, mode, var='pinhole'):
        if var == 'pinhole':    return f'{self.data_dir}/calibration/{cam}/{mode}/cameras.txt'
        elif var == 'generic':  return f'{self.data_dir}/calibration/{cam}/{mode}/intrinsics.yaml'

    def undist_model(self, cam, mode):
        return f'{self.data_dir}/calibration/{cam}/{mode}/undistortion.pt'

    # Addons
    # ------
    def mvsnet_cam(self, cam, mode, pos_i):
        return f'{self.addons_dir}/{self.scene_name}/{cam}/{mode}/mvsnet_input/{pos_i:08}_cam.txt'

    def mvsnet_pair(self, cam, mode):
        return f'{self.addons_dir}/{self.scene_name}/{cam}/{mode}/mvsnet_input/pair.txt'

    def idr_cams(self, cam, mode):
        return f'{self.addons_dir}/{self.scene_name}/{cam}/{mode}/idr_input/cameras.npz'

    def proj_depth(self, src, svar, dst, dvar, pos_i):
        base_dir = f'{self.addons_dir}/{self.scene_name}/proj_depth/{src}.{svar}@{dst}.{dvar}'
        return f'{base_dir}/{pos_i:04}.png'
