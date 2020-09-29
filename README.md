# OpenCV-Object-Tracking
Scripts for object tracking and motion detection using Python and OpenCV

## Object Tracker

Object tracker based on OpenCV KCF tracker. The program can capture video from a source or from a webcam.
Script parameters:

#### -v 

is your video path. In default case run your webcam.

#### -b 

is your preset bounding box. Four integers separated by comma: 

(x-coordinate of top left corner),(y-coordinate of top left corner),(width),(height)

In default case you can pick area by mouse.

#### -f 

is frame number for start tracking if -b is predetermined. In default case is 0.

Example:

```
python object_tracker.py -v videos/fruit.mp4 -b 235, 100, 180, 180 -f 10
```

  
