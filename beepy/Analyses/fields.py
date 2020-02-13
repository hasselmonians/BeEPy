import numpy as np
from astropy.convolution import Gaussian2DKernel, convolve


def ratemap(root, xe=None, ye=None, occ_thresh=0, smooth=2):
    """
    Calculates the 2-dimensional ratemap and returns

    :param root: session object
    :param xe:  X dimension bins (defaults to min:10:max)
    :param ye:  Y dimension bins (defaults to min:10:max)
    :param occ_thresh: Less than N samples --> NaN
    :param smooth: 2D gaussian convolution std
    :return:
        rm: ratemap
        occ: occupancy
        spks: number of spikes
    """
    if xe is None:
        xe = np.arange(np.nanmin(root.beh['x']),
                       np.nanmax(root.beh['x']),
                       10)

    if ye is None:
        ye = np.arange(np.nanmin(root.beh['y']),
                       np.nanmax(root.beh['y']),
                       10)

    occ, _, _ = np.histogram2d(root.beh['x'], root.beh['y'], bins=(xe, ye))
    unvisited = occ <= occ_thresh
    occ[unvisited] = np.nan
    spks, _, _ = np.histogram2d(root.spike['x'], root.spike['y'], bins=(xe, ye))
    spks[unvisited] = np.nan

    rm = np.divide(spks, occ)
    rm[unvisited] = np.nan

    # Begin smoothing
    if smooth > 0:
        kernel = Gaussian2DKernel(smooth, smooth)
        rm = convolve(rm, kernel)
        rm[unvisited] = np.nan

        occ = convolve(occ, kernel)
        occ[unvisited] = np.nan

        spks = convolve(spks, kernel)
        spks[unvisited] = np.nan

    return rm, occ, spks


def polar_ratemap(root, be=None):
    pass