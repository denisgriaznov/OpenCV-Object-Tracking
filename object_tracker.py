import argparse
import cv2

# Variable indicating that tracking is in progress
is_tracking = False
tracker = None
# Init tracker
def init_tracker(frame,bbox):
        global tracker
        tracker = None
        tracker = cv2.TrackerKCF_create()
        tracker.init(frame, bbox)
        global is_tracking
        is_tracking = True

# Tracking function
def tracking():

    # Get new box and tracking state from new frame
    ok, bbox = tracker.update(frame)

    if ok:
        # Recalculated rectangle and position
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        cv2.putText(frame, "POSITION : [{} {}]".format(str(int(p2[0]/2)) , str(int(p2[1]/2))), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
        cv2.putText(frame, "To change box press 'b'" , (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
    else :
        # If tracking fails
        global is_tracking
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        is_tracking = False



if __name__=="__main__":

    # Create parser of video path and initial box
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", default = 'cam', type=str, help="Path to video. Default is your camera capturing.")
    parser.add_argument("-b", "--box", default = 'select', type=str, help="Bounding box coordinates. In defult case you can select area after press key 'b'.")
    parser.add_argument("-f", "--frame", default = 0, type=int, help="Frame number for preselected box. In default case is first frame.")
    args = parser.parse_args()

    # Check arguments
    if args.video=='cam':
        video = cv2.VideoCapture(0)
    else:
        video = cv2.VideoCapture(args.video)



    # Check video flow
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    ok, frame = video.read()

    if not ok:
        print("Cannot read video file")
        sys.exit()

    if args.box=='select':
        bbox = (235, 100, 180, 180)
    else:
        bbox = tuple(int(x) for x in args.box.split(','))
        if not args.frame:
            init_tracker(frame,bbox)

    frame_number = 0
    # Frames flow loop
    while True:

        ok, frame = video.read()
        if not ok:
            break

        # If frame not default, chek frame numper
        frame_number = frame_number + 1
        if (args.box and args.frame and args.frame==frame_number):
            init_tracker(frame,bbox)

        key = cv2.waitKey(1) & 0xff
        if key == 27:
            break

        # Init new bbox
        if key == ord("b"):
            cv2.putText(frame, "Select bounding box and press Space", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            bbox = cv2.selectROI("Tracking", frame, fromCenter=False,showCrosshair=True)
            init_tracker(frame,bbox)

        if (is_tracking):
            tracking()
        else:
            cv2.putText(frame, "To select bounding box press 'b'", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        cv2.imshow("Tracking", frame)

    cv2.destroyAllWindows()
