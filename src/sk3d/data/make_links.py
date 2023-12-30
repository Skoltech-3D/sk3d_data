#!/usr/bin/env python3
from argparse import ArgumentParser

from sk3d.data.dataset import scene_name_by_id


def main():
    description = 'Makes list of links to download parts of Skoltech3D dataset.'
    parser = ArgumentParser(description=description)
    parser.add_argument('--conf', type=str, required=True,
                        help='Path to the config file.')
    parser.add_argument('--server', type=str, choices=server2path.keys(),
                        default='storage.yandexcloud.net',
                        help='Server to download the data from. YandexCloud (the default) is recommended for the best download speed.')
    args = parser.parse_args()
    links = make_links(args.conf, args.server)
    for link in links:
        print(link)


def make_links(conf, server='storage.yandexcloud.net'):
    r"""Makes list of links to download parts of Skoltech3D dataset.

    Parameters
    ----------
    conf : str
        Path to the config file.
    server : {'storage.yandexcloud.net', 'skoltech3d.appliedai.tech'}
        Server to download the data from. YandexCloud (the default) is recommended for the best download speed.

    Returns
    -------
    links : list of str
    """
    lines = open(conf).readlines()
    all_scenes = set(scene_name_by_id.values())
    scenes = []

    'Collect filenames'
    filenames = []
    for line in lines:
        if line.startswith('#'):
            continue
        if line.startswith('scenes = '):
            'Get scene list'
            for scene in line[len('scenes = '):].split():
                if scene == 'all':
                    scenes = sorted(all_scenes)
                    break
                if scene not in all_scenes:
                    raise ValueError(f'Unknown scene name "{scene}"')
                scenes.append(scene)
            continue

        words = line.split()
        try:
            filename = next(w for w in words if w.endswith('.zip'))
        except StopIteration:
            continue
        if '{scene}' in filename:
            filenames.extend(filename.format(scene=scene) for scene in scenes)
        else:
            filenames.append(filename)

    'Make links'
    try:
        path_dir = server2path[server]
    except KeyError:
        raise ValueError(f'Unknown server "{server}"')
    links = [f'{path_dir}/{filename}' for filename in filenames]
    return links


server2path = {
    'storage.yandexcloud.net': 'https://storage.yandexcloud.net/skoltech3d',
    'skoltech3d.appliedai.tech': 'https://skoltech3d.appliedai.tech/data',
}


if __name__ == '__main__':
    main()
