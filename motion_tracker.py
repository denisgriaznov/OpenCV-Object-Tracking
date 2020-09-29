import argparse
import cv2

DELAY = 20

def grayscale(frame):
    # Converting color image to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Converting gray scale image to GaussianBlur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return gray

# Finding and drawing contours
def drawContours(background, frame, threshold, area):

    gray = grayscale(frame)
    # Calculation difference between init background and frame
    diff_frame = cv2.absdiff(background, gray)

    # Setup threshold
    thresh_frame = cv2.threshold(diff_frame,threshold, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # Finding contour of moving object
    cnts,_ = cv2.findContours(thresh_frame.copy(),
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print("moving objects: {}".format(len(cnts)))
    for contour in cnts:
        if cv2.contourArea(contour) < area:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

if __name__=="__main__":

    # Create parser of video path
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", default = 'cam', type=str, help="Path to video. Default is your camera capturing.")
    args = parser.parse_args()

    # Check arguments
    if args.video=='cam':
        video = cv2.VideoCapture(0)

    else:
        video = cv2.VideoCapture(args.video)

    ok, frame = video.read()
    # Initializing background as first frame
    background = grayscale(frame)
    background_list = list(background for i in range(DELAY))


    while True:

        ok, frame = video.read()
        drawContours(background, frame, 40, 800)
        cv2.imshow("Color Frame", frame)


        background = background_list[DELAY - 1]

        # Update list of background
        background_list.pop(0)
        background_list.append(grayscale(frame))

        key = cv2.waitKey(1)
        if key == 27:
            break

    video.release()
    cv2.destroyAllWindows()
