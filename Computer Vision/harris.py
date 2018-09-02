import os 
from scipy.ndimage import filters
from PIL import Image

import numpy as np
from matplotlib import pyplot as plt

import datetime

def compute_harris_response(im, sigma=1):
    """compute the harris corner detector response function for 
    each pixel"""
    start = datetime.datetime.now()
    #derivatives
    imx = np.zeros(im.shape)
    # gaussian filter args: 
    #   input - an array, 
    #   [standard deviation], 
    #   [order], on each axis 
    #   output
    filters.gaussian_filter(im, (sigma, sigma), (0,1),  imx)
    imy = np.zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (1,0), imy)
    #harris matrix components
    Wxx = filters.gaussian_filter(imx*imx, sigma)
    Wxy = filters.gaussian_filter(imx*imy, sigma)
    Wyy = filters.gaussian_filter(imy*imy, sigma)
    delta = datetime.datetime.now()
    
    
    #determinant and trace to approx
    #[[x, y]  * [[x, y] = [[xx, xy]
    # [x, y]]   [x, y]]    [xy, yy]]
    # Det = xx*yy - xy*xy
    # Trace = xx + yy
    Wdet = Wxx*Wyy - Wxy**2
    Wtr = Wxx + Wyy
    
    # added these two lines to account for NaN
    res = Wdet / Wtr
    res[np.isnan(res)] = 0

    return res

def get_harris_points(harrisim, min_dist=10, threshold= 0.1):
    """ Return corners from a Harris response image
    min_dist is the minimum number of pixels separating
    corners and image boundary. """

    #find the top corner candidates above a corner threshold
    corner_threshold = harrisim.max() * threshold
    harrisim_t = (harrisim > corner_threshold) * 1

    #get coords of candidates 
    coords = np.array(harrisim_t.nonzero()).T

    #candidate_values
    candidate_values = [harrisim[c[0], c[1]] for c in coords]

    #sort candidates
    index = np.argsort(candidate_values)
    
    #store allowed point locations in array
    allowed_locations = np.zeros(harrisim.shape)
    allowed_locations[min_dist:-min_dist, min_dist: -min_dist] = 1

    #select the best points taking min distance into account 
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i,0], coords[i,1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0

    return filtered_coords

def plot_harris_points(image, filtered_coords):
    from matplotlib import pyplot as plt
    plt.figure()
    plt.gray()
    plt.imshow(image)
    plt.plot([p[1] for p in filtered_coords], 
        [p[0] for p in filtered_coords], '*')
    plt.axis('off')
    plt.show()


def get_descriptors(image, filtered_coords, wid=5):
    """for each point, return pixel value around the point using a 
    neighbourhood of 2 * width + 1( assume points are extracted 
    with a min_distance > wid)"""
    desc = []
    for coords in filtered_coords:
        patch = image[coords[0]-wid: coords[0] + wid + 1, 
                    coords[1] - wid: coords[1]+wid+1].flatten()
        desc.append(patch)

    return desc


def match(desc1, desc2, threshold=0.5):
    """for each corner point descriptor in the first image
    select its match from the second image using normalized cross
    correlation"""
    n = len(desc1[0])
    
    #pairwise distances
    d = -np.ones((len(desc1), len(desc2)))
    for i in range(len(desc1)):
        for j in range(len(desc2)):
            d1 = (desc1[i] - np.mean(desc1[i])) / np.std(desc1[i])
            d2 = (desc2[j] - np.mean(desc2[j])) / np.std(desc2[j])
            ncc_value = np.sum(d1*d2) / (n-1)
            if ncc_value > threshold:
                d[i,j] = ncc_value

    ndx = np.argsort(-d)
    matchscores = ndx[:,0]

    return matchscores

def match_twosided(desc1, desc2, threshold=0.5):
    """two sided symmetric version of match()."""

    matches_12 = match(desc1, desc2, threshold)
    matches_21 = match(desc2, desc1, threshold)

    ndx_12 = np.where(matches_12 >= 0)[0]

    for n in ndx_12:
        if matches_21[matches_12[n]] != n:
            matches_12[n] = -1

    return matches_12

def appendimages(im1, im2):
    """return a new image that appends the two images side by side."""
    #select the image with the fewest rows and fill in the empty rows

    rows1 = im1.shape[0]
    rows2= im2.shape[0]

    if rows1 < rows2:
        im1 = np.concatenate((im1, np.zeros((rows2-rows1, im1.shape[1]))), axis=0)
    elif rows1 > rows2:
        im2 = np.concatenate((im2, np.zeros((rows1-rows2, im2.shape[1]))), axis=0)

    return np.concatenate((im1, im2), axis=1)

def plot_matches(im1, im2, locs1, locs2, matchscores, show_below=False):
    """show a figure with lines joining the accepted matches
    Input
    =====
    im1, im2 - image arrays 
    locs1, locs2 -feature locations 
    matchscores - an output from match
    show_below - if images are to be shown below matches
    """

    im3 = appendimages(im1, im2)
    if show_below:
        im3 = np.vstack((im3, im3))

    plt.imshow(im3)
    cols1 = im1.shape[1]

    for i, m in enumerate(matchscores):
        if m > 0:
            plt.plot([locs1[i][1], locs2[m][1]+cols1],[locs1[i][0], locs2[m][0]], 'c*-')
    plt.axis('off')


if __name__ == "__main__":
    import sys
    print "testing application"
    simple_img = np.zeros((128,128))
    simple_img[32:96,32:96] = 255
    #im1 = simple_img
    #im2 = np.copy(im1)
    im1 = np.array(Image.open(sys.argv[1]).convert('L'))
    im2 = np.copy(im1)
    
    
    filtered1 = get_harris_points(compute_harris_response(im1, 1), 10)
    filtered2 = get_harris_points(compute_harris_response(im2, 1), 10)
    d1 = get_descriptors(im1, filtered1)
    d2 = get_descriptors(im2, filtered2)
    
    matches = match_twosided(d1, d2)
    plt.figure()
    plt.gray()
    plot_matches(im1, im2, filtered1, filtered2, matches)
    plt.show()