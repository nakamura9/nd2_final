'''
This system will take the interest points stored in the system and try and match them with snapshots taken by the camera.
each shot is processed with harris to find 10 interest points.
the process goes as follows.
the region we are not interested in is blanked out with zeros
in the interested region harris dectection is applied.
afterwards the data is matched between the two images. 
this script waits for the camera trigger.
The location of each matched interest point is matched with that of the reference.
the distance the detected image is from the reference is the distance that needs to be moved to correct the error.
the pixel distance is converted 
'''