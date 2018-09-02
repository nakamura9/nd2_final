import os
from PIL import Image
from numpy import *
import numpy
from pylab import *
from scipy.ndimage import filters
from scipy.ndimage import measurements, morphology
import math
from pca import pca

def img_compress(img):
    """
    Image processing technique to reduce dimensionality in an image
    Reduce the resolution in an image using pixel deletion of every second row and column
    """
    img = numpy.delete(img, (list(range(0, img.shape[1], 2))), axis=1)
    return numpy.delete(img, (list(range(0, img.shape[0], 2))), axis=0)

def get_imlist(path):
    """ Returns a list of filenames for
    all jpg images in a directory. """

    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".jpg")]


def create_greyscale_image(img):
    """create a greyscale image flattened as a one dimensional array"""
    return img.convert("L")
    

def invert_greyscale_image(img):
    """inverts a greyscale image"""
    if isinstance(img, Image.Image):
        img = array(img)
    img = 255 - img
    return Image.fromarray(img)


def im_array_resize(im, size):
    """Take an image array and resize the array via a PIL image resize"""
    pil_im = Image.fromarray(uint8(im))

    return array(pil_im.resize(size))


def histeq(im, bins=256):
    """
    Histogram equalization of a greyscale image
    ***Enhances quite nicely***
    """

    imhist, bins = histogram(im.flatten(), bins=bins, normed=True)
    cdf = imhist.cumsum() #cumulative distribution function
    cdf = 255 * cdf/ cdf[-1] #normalize

    #linear interpolation used to find new pixel values

    im2 = interp(im.flatten(), bins[:-1], cdf)

    return im2.reshape(im.shape), cdf


def compute_average(imlist):
    """Compute the average of a list of images."""
    averageim = array(Image.open(imlist[0]), "f")

    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print imname + " ...skipped"
        averageim /= len(averageim)

    return array(averageim, "uint8")


def gaussian(img, sd):
    """
    Takes an image array(greyscale) and returns a 
    gaussian filtered array with the given standard deviation
    """
    return filters.gaussian_filter(img, sd)


def color_gaussian(img, sd):
    """
    takes a color image and returns an array of all channels filtered thriugh the gausssian function
    """
    res = img
    for i in range(3):
        res[:,:, i] = gaussian(img[:,:,i], sd)

    return uint8(res)


def im_derivative(im, filter):
    """
    Calculate the derivative of the image using approximations inspired by the prewitt and sobel filters 
    """
    imx = zeros(im.shape) #makes an array full of zeros
    filter(im, 1, imx)

    imy= zeros(im.shape)
    filter(im, 0, imy)

    return array(sqrt(imx**2+ imy**2), "uint8")

def im_edge_direction(im, filter):
    """find the x and y derivatives and then use trig to compute the directionof the edge"""
    imx = zeros(im.shape) #makes an array full of zeros
    filter(im, 1, imx)

    imy= zeros(im.shape)
    filter(im, 0, imy)

    imdir = zeros(im.shape)
    vert = math.pi / 2
    for index, value in ndenumerate(imdir):
            if imx[index] != 0:
                imdir[index] = math.atan2(imy[index],imx[index])
            elif imx[index] == 0 and imy[index] != 0:
                imdir[index] = vert #vertical line
            else:
                imdir[index] = 0
    return imdir

def outlines(img, filter, long_only=True):
    """creates a mapping of gradients to points and assumes that points with the same gradient are part of the same line"""

    res = im_derivative(img, filter)
    objs = {}
    for index, value in ndenumerate(res):
        if value in objs:
            objs[value].append(index)
        else:
            objs[value] = [index]

    if long_only:
        long = {}
        for obj in objs:

            if len(objs[obj]) > 20 and obj != 0:
                long[obj] = objs[obj]
        return long
    else:
        return objs

def gaussian_derivative(im, sd):
    """
    Calculate the derivative using gaussian and a standard deviation
    """
    imx = zeros(im.shape) #makes an array full of zeros
    filters.gaussian_filter(im, (sd, sd), (0,1), imx)

    imy= zeros(im.shape)
    filters.gaussian_filter(im, (sd, sd), (1,0), imy)
    
    #returns the gradient calculated as an overall magnitude
    return array(sqrt(imx**2+ imy**2), "uint8")


def binary_threshold(im, thresh = 128):
    """Converts a greyscale image into a binary one by thresholding at the value of 128"""
    return 1 * (im < thresh) #) for values less than 128 and 1 otherwise

def denoiser(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
    """
    An implementation of the Rudin-Osher-Fatemi(ROF) image demoising model
    using the numerical procedure presented in eq(11) A.Chambolle (2005)

    Input: noisy imput greyscale image, initial guess for U weight of the TV(total variation)-regularizing term, step_lenght, tolerance for stop criterion
    """

    m,n = im.shape

    #var init
    U = U_init
    Px = im #x component of the dual field
    Py = im #y component of the dual field
    error = 1

    i =0
    while (error > tolerance):
        U_old = U

        #gradient of the primal variable
        GradUx = roll(U, -1, axis=1)-U #X component of U's gradient
        GradUy = roll(U, -1, axis=0)-U #Y component of U's gradient

        #Update the dual variable
        PxNew = Px + (tau/tv_weight)*GradUx
        PyNew = Py + (tau/tv_weight)*GradUy

        NormNew = maximum(1, sqrt(PxNew**2+PyNew**2))

        Px = PxNew/NormNew #Update of x-component(dual)
        Py = PyNew/NormNew #Update of y-component(dual)

        #Update the primal variable
        RxPx = roll(Px, 1, axis=1) #right x-translation of the x component
        RyPy = roll(Py, 1, axis=0) #right y-translation of the y-component

        DivP = (Px-RxPx)+(Py-RyPy) #divergence of the dual field
        U = im +tv_weight*DivP

        #update of error
        i += 1
        print("Iterated %d times, with an error of: %f " % (i, error))
        error = linalg.norm(U-U_old)/sqrt(n-m)

    return U, im-U

def add_noise(im, intensity=30):
    """
    Takes an image and randomly adds noise to it synthetically
    """
    return im + intensity * numpy.random.standard_normal(im.shape)

def grey_unsharp(img):
    """
    Increase the sharpness of an image by subtracting its gaus from the 
    original
    """
    return img - gaussian(img, 5)

def color_unsharp(img):
    """
    Increase the sharpness of an image by subtracting its gaus from the 
    original. For color images the process is performed on each channel in turn
    """
    gaus = numpy.copy(img)
    #select the right combination of channels for the desired results
    gaus[:,:, 2] = gaussian(img[:,:,2], 5)
    gaus[:,:, 1] = gaussian(img[:,:,1], 5)
    gaus[:,:, 0] = gaussian(img[:,:,0], 5)
    return imarray - gaus
    
def image_quotient(img, sig):
    """
    The quotient of the image and its gaussian 
    """
    return img / (img * gaussian(img, sig))

def find_objects(img):
    """
    Uses the label function of the measurement module to find the objects 
    in a binary thresholded image
    """
    deriv = im_derivative(img, filters.sobel)
    thresh = binary_threshold(deriv)
    return measurements.label(thresh)



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise Exception("The argument must be a filename")

    img = Image.open(sys.argv[1])
    imarray = array(img)
    grey_imarray =array(create_greyscale_image(img))
    simple_img = numpy.zeros((128,128))
    simple_img[32:96,32:96] = 255
    
    """Image.fromarray(simple_img).show()
    
    directed = im_edge_direction(simple_img, filters.sobel)
    for index, val in ndenumerate(directed):
        if val != 0: print index, ": ", val
    """

    """
    #Image inversion
    create_greyscale_image(img).show()

    invert_greyscale_image(create_greyscale_image(img)).show()
    """
    
    """
    #Image resize
    smaller_img = im_array_resize(imarray, (640, 640))
    print "height: ", len(smaller_img), "\nwidth: ", len(smaller_img[0])
    """

    """
    #Image histogram
    figure()
    hist(array(create_greyscale_image(img)).flatten(), 128)
    show()
    """
    
    """
    #Histogram equalization   
    hist_data = histeq(grey_imarray)
    
    figure()
    hist(hist_data[0].flatten(), 256)
    show()

    Image.fromarray(hist_data[0]).show()
    """


    """
    #Gaussian tests
    import time
    for i in range(5):
        pic =Image.fromarray(gaussian(grey_imarray, i))
        pic.show()
        time.sleep(2)
        pic.close()
   """ 

    """
    #Color gaussian
    Image.fromarray(color_gaussian(imarray, 5)).show()
    """

    """
    #Image derivatives
    Image.fromarray(im_derivative(grey_imarray, filters.prewitt)).show()
    """

    """
    #Gaussian Image derivatives
    Image.fromarray(gaussian_derivative(grey_imarray, 1)).show()
    """

    """
    #Object identification
    labels, objs = measurements.label(binary_threshold(grey_imarray))
    print labels
    """

    """
    #Image denoising
    noisy_image_array = add_noise(grey_imarray)
    Image.fromarray(noisy_image_array).show()

    Image.fromarray(denoiser(grey_imarray, grey_imarray, tolerance=5)[0]).show()

    """
    """
    #Exercise 1: gaussian contours
    figure()
    gray()
    contour(Image.fromarray(gaussian(grey_imarray,2)), origin='image')
    show()
    """

    """
    #Exercise 2: unsharp masking
    Image.fromarray(grey_unsharp(grey_imarray)).show()
    
    #color unsharp
    Image.fromarray(color_unsharp(imarray)).show()
    """

    """
    #Exercise 3: image quotient
    Image.fromarray(image_quotient(grey_imarray, 5)).show()
    """
    
    """
    #Exercise 4: Edge detection using gradients
    bandw, points = get_outlines(simple_img)
    
    Image.fromarray(bandw).show()
    """

    """
    #image compression
    Image.fromarray(img_compress(grey_imarray)).show()
    """

    #print len(outlines(grey_imarray, filters.sobel))

    #plots the principle components for the first seven modes with the 
    # the most variation.    
    imlist = get_imlist("image_data/a_selected_thumbs")
    im = array(Image.open(imlist[0]))
    m,n = im.shape[0:2]
    imnbr = len(imlist)

    immatrix = array([array(Image.open(im)).flatten() for im in imlist], 'f')

    V,S,immean = pca(immatrix)

    figure()
    gray()
    subplot(2, 4, 1)
    imshow(immean.reshape(m,n))
    for i in range(7):
        subplot(2,4,i+2)
        imshow(V[i].reshape(m,n))

    show()

    import pickle
    f = open('font_pca_modes.pkl', 'wb')
    pickle.dump(immean, f)
    pickle.dump(V, f)
    f.close()