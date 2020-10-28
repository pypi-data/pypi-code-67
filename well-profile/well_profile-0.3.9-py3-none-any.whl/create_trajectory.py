from .plot import plot_wellpath
from .load_trajectory import define_sections, calc_dls
from .equations import *
from numpy import arange, linspace, interp
import pandas as pd
from math import degrees


def get(mdt, cells_no=100, profile='V', build_angle=1, kop=0, eob=0, sod=0, eod=0, kop2=0, eob2=0, units='metric',
        set_start=None, change_azimuth=None, dls_resolution=30):
    """
    Generate a wellpath.
    :param mdt: target depth, m or ft
    :param cells_no: number of cells
    :param profile: 'V' for vertical, 'J' for J-type, 'S' for S-type, 'H1' for Horizontal single curve and 'H2' for
                                                                                            Horizontal double curve
    :param build_angle: building angle, °
    :param kop: kick-off point, m or ft
    :param eob: end of build, m or ft
    :param sod: start of drop, m or ft
    :param eod: end of drop, m or ft
    :param kop2: kick-off point 2, m or ft
    :param eob2: end of build 2, m or ft
    :param units: 'metric' or 'english'
    :param set_start: set initial point in m {'north': 0, 'east': 0, 'depth': 0}
    :param change_azimuth: add specific degrees to azimuth values along the entire well
    :param dls_resolution: base length to calculate dls
    :return: a wellpath object with 3D position
    """

    initial_point = {'north': 0, 'east': 0, 'depth': 0}

    if set_start is not None:
        for x in set_start:  # changing default values
            if x in initial_point:
                initial_point[x] = set_start[x]

    md = list(arange(0, mdt + 1, 1))    # Measured Depth from RKB, m
    depth_step = md[1]
    tvd = None
    inclination = None
    azimuth = None
    north = None
    east = None

    if profile == 'V':        # Vertical well
        tvd, north, east, inclination, azimuth = vertical_section(profile, md, kop, depth_step)

    if profile == 'J':        # J-type well
        tvd, north, east, inclination, azimuth = create_j_well(mdt, md, kop, eob, build_angle, depth_step)

    if profile == 'S':  # S-type well
        tvd, north, east, inclination, azimuth = create_s_well(mdt, md, kop, eob, sod, eod, build_angle, depth_step)

    if profile == 'H1':     # Horizontal single-curve well
        tvd, north, east, inclination, azimuth = create_h1_well(mdt, md, kop, eob, depth_step)

    if profile == 'H2':        # Horizontal double-curve well
        tvd, north, east, inclination, azimuth = create_h2_well(mdt, md, kop, eob, kop2, eob2, build_angle, depth_step)

    # Re-arranging
    md_new = list(linspace(0, mdt, num=cells_no))
    depth_step = md_new[1] - md_new[0]
    tvd_new = [interp(x, md, tvd) for x in md_new]
    north_new = [interp(x, md, north) for x in md_new]
    east_new = [interp(x, md, east) for x in md_new]
    inclination_new = [interp(x, md, inclination) for x in md_new]
    azimuth_new = [interp(x, md, azimuth) for x in md_new]
    if change_azimuth is not None:
        azimuth_new, north_new, east_new = mod_azimuth(change_azimuth, azimuth_new, north_new, east_new)

    # Defining type of section
    sections = define_sections(tvd_new, inclination_new)

    dogleg = [0]
    inc = inclination_new.copy()
    for x in range(1, len(md_new)):
        dogleg.append(calc_dogleg(inc[x - 1], inc[x], azimuth_new[x - 1], azimuth_new[x]))
    dogleg = [degrees(x) for x in dogleg]

    class WellDepths(object):
        def __init__(self):
            self.md = md_new
            self.tvd = [x + initial_point['depth'] for x in tvd_new]
            self.depth_step = depth_step
            self.cells_no = cells_no
            self.north = [x + initial_point['north'] for x in north_new]
            self.east = [x + initial_point['east'] for x in east_new]
            self.inclination = [round(i, 2) for i in inclination_new]
            self.dogleg = dogleg
            self.azimuth = azimuth_new
            self.dls = calc_dls(self.dogleg, self.md, resolution=dls_resolution)
            self.dls_resolution = dls_resolution
            self.sections = sections
            self.units = units

        def plot(self, add_well=None, names=None):
            fig = plot_wellpath(self, add_well, names)
            return fig

        def df(self):
            data_dict = {'md': self.md, 'tvd': self.tvd, 'inclination': self.inclination,
                         'azimuth': self.azimuth, 'north': self.north, 'east': self.east}
            dataframe = pd.DataFrame(data_dict)
            return dataframe

    return WellDepths()


def vertical_section(profile, md, kop, depth_step):
    if profile == 'V':
        tvd = md
    else:
        tvd = md[:round(kop / depth_step) + 1]  # True Vertical Depth from RKB, m

    north = [0] * len(tvd)  # x axis
    east = [0] * len(tvd)  # x axis
    inclination = [0] * len(tvd)
    azimuth = [0] * len(tvd)

    return tvd, north, east, inclination, azimuth


def create_s_well(mdt, md, kop, eob, sod, eod, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('S', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle) / round((eob - kop) / depth_step)
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        inclination.append(degrees(theta))
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))

    for x in range(round((sod - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1])
        azimuth.append(0)

    # Drop section
    s = depth_step
    cells_drop = round((eod - sod) / depth_step)
    theta_delta = radians(build_angle) / cells_drop
    theta = radians(build_angle)
    r = s / theta_delta
    z_checkpoint = tvd[-1]
    hz_checkpoint = north[-1]
    for x in range(cells_drop):
        z_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
        tvd.append(round(z_checkpoint + z_displacement, 2))

        hz_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
        north.append(round(hz_checkpoint + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1] - degrees(theta_delta))
        azimuth.append(0)

    # Vertical section
    for x in range(round((mdt - eod) / depth_step)):
        tvd.append(round(tvd[-1] + depth_step, 2))
        north.append(north[-1])  # x axis
        east.append(0)
        inclination.append(0)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_j_well(mdt, md, kop, eob, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('J', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle / round((eob - kop) / depth_step))
    theta = theta_delta
    r = s / theta

    z_vertical = tvd[-1]
    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        inclination.append(degrees(theta))

        z_displacement = (r * sin(theta))
        tvd.append(round(z_vertical + z_displacement, 2))

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))
    for x in range(round((mdt - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        inclination.append(inclination[-1])
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_h1_well(mdt, md, kop, eob, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('H1', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(90) / round((eob - kop) / depth_step)
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta += theta_delta
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        inclination.append(degrees(theta))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Horizontal section
    for x in range(round((mdt - eob) / depth_step)):
        tvd.append(tvd[-1])
        north.append(north[-1] + depth_step)
        east.append(0)
        inclination.append(90)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def create_h2_well(mdt, md, kop, eob, kop2, eob2, build_angle, depth_step):
    # Vertical section
    tvd, north, east, inclination, azimuth = vertical_section('H2', md, kop, depth_step)

    # Build section
    s = depth_step
    theta_delta = radians(build_angle / round((eob - kop) / depth_step))
    theta = theta_delta
    r = s / theta

    z_displacement = (r * sin(theta))
    tvd.append(round(tvd[-1] + z_displacement, 2))
    z_count = z_displacement

    hz_displacement = r * (1 - cos(theta))
    north.append(round(north[-1] + hz_displacement, 2))
    east.append(0)
    inclination.append(degrees(theta))
    azimuth.append(0)

    for x in range(round((eob - kop) / depth_step) - 1):
        theta = theta + theta_delta
        z_displacement = (r * sin(theta)) - z_count
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count += z_displacement

        hz_displacement = r * (1 - cos(theta)) - north[-1]
        inclination.append(degrees(theta))
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Tangent section
    z_displacement = (depth_step * cos(radians(build_angle)))
    hz_displacement = (depth_step * sin(radians(build_angle)))
    for x in range(round((kop2 - eob) / depth_step)):
        tvd.append(round(tvd[-1] + z_displacement, 2))
        inclination.append(inclination[-1])
        north.append(round(north[-1] + hz_displacement, 2))
        east.append(0)
        azimuth.append(0)

    # Build section 2
    s = depth_step
    build_angle = 90 - build_angle
    cells_drop = round((eob2 - kop2) / depth_step)
    theta_delta = radians(build_angle) / cells_drop
    theta = radians(build_angle)
    r = s / theta_delta
    z_checkpoint = tvd[-1]
    hz_checkpoint = north[-1]

    for x in range(cells_drop):
        hz_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
        north.append(round(hz_checkpoint + hz_displacement, 2))
        inclination.append(inclination[-1] + degrees(theta_delta))
        east.append(0)
        azimuth.append(0)

        z_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
        tvd.append(round(z_checkpoint + z_displacement, 2))

    # Horizontal section
    for x in range(round((mdt - eob2) / depth_step)):
        tvd.append(tvd[-1])
        north.append(north[-1] + depth_step)
        inclination.append(inclination[-1])
        east.append(0)
        azimuth.append(0)

    return tvd, north, east, inclination, azimuth


def mod_azimuth(change_azimuth, azimuth_new, north_new, east_new):
    for a in range(len(azimuth_new)):
        azimuth_new[a] += change_azimuth

        if change_azimuth <= 90:
            east_new[a] = north_new[a] * sin(radians(change_azimuth))
            north_new[a] *= cos(radians(change_azimuth))
        elif 90 < change_azimuth <= 180:
            angle = change_azimuth - 90
            east_new[a] = north_new[a] * round(cos(radians(angle)), 3)
            north_new[a] *= - sin(radians(angle))
        elif 180 < change_azimuth <= 270:
            angle = change_azimuth - 180
            east_new[a] = - north_new[a] * round(sin(radians(angle)), 3)
            north_new[a] *= - cos(radians(angle))
        else:
            angle = change_azimuth - 270
            east_new[a] = - north_new[a] * round(cos(radians(angle)), 3)
            north_new[a] *= sin(radians(angle))

    return azimuth_new, north_new, east_new
