import cv2
import numpy as np
from matplotlib import pyplot as plt
from harris import appendimages

def process_file(filename):
    sift=cv2.SIFT()
    img= cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp = sift.detect(gray, None)
    img = cv2.drawKeypoints(gray, kp)
    cv2.imwrite("kp.jpg", img)
    return kp

def get_descriptors(filename):
    sift=cv2.SIFT()
    img= cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp, desc = sift.detectAndCompute(gray, None)
    
    return kp, desc

def match(desc1, desc2):
    """For each descriptor in the first image, select its match in the 
    second image. input: desc1(descriptors for the first image)
    desc2(descriptors for the second image)"""
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(desc1, desc2)
    return sorted(matches, key= lambda x:x.distance)

def drawMatches(img1, kp1, img2, kp2, matches):
    out = appendimages(img1, img2)
    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        x1, y1 = kp1[img1_idx].pt
        x2, y2 = kp2[img2_idx].pt
        cv2.circle(out, (int(x1), int(y1)), 4, (0,0,255), 1)
        cv2.circle(out, (int(x2) + img1.shape[1], int(y2)), 4, (0,0,255), 1)

        cv2.line(out, (int(x1), int(y1)), (int(x2)+ img1.shape[1], int(y2)), (0,0,255), 1)

    return out

def make_and_plot_matches(img1, img2):
    kp1, desc1 = get_descriptors(img1)
    kp2, desc2 = get_descriptors(img2)
    img1 = cv2.cvtColor(cv2.imread(img1), cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(cv2.imread(img2), cv2.COLOR_BGR2GRAY)
    matches = match(desc1, desc2)
    imgres = drawMatches(img1, kp1, img2, kp2, matches)
    plt.imshow(imgres), plt.show()
    

if __name__ == "__main__":
    make_and_plot_matches("gerald.jpg", "gerald.jpg")