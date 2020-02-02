import cv2
from scipy import ndimage
import math



cap = cv2.VideoCapture(0)

# Checking if camera can be accessed
if not cap.isOpened():
    raise IOError("Cannot open webcam")

#defining the crosshair
crosshair_length = 10
crosshair_thickness = 2
backgroud_subtractor = cv2.createBackgroundSubtractorMOG2()

# Details for saving the video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))


while True:
    # Reading a new frame
    read, frame = cap.read()
    # Flipping the image so that it looks like a mirror
    frame = cv2.flip(frame, 1)

    background_mask_frame = backgroud_subtractor.apply(frame)
    #cv2.fastNlMeansDenoising(background_mask_frame,7,21)
    # Calculating the center of were most changes have happened
    mass_center = ndimage.measurements.center_of_mass(background_mask_frame)
    # Drawing crosshair
    if not math.isnan(mass_center[1]) and not math.isnan(mass_center[1]):
        cv2.line(frame, (int(mass_center[1]), int(mass_center[0])- crosshair_length), (int(mass_center[1]), int(mass_center[0]) + crosshair_length),
             (0, 0, 255), crosshair_thickness)
        cv2.line(frame, (int(mass_center[1]) - crosshair_length, int(mass_center[0])), (int(mass_center[1]) + crosshair_length, int(mass_center[0])),
             (0, 0, 255), crosshair_thickness)
    # Showing video with crosshair
    cv2.namedWindow('Mask', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Mask', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video', frame)

    # Comment the following if you do not want to save a video file
    output_file.write(frame)
    cv2.imshow('Mask', background_mask_frame)

    # Stopp the loop if ESC key is detected
    input_key = cv2.waitKey(1)
    if input_key == 27: # = ESC
        break
# Cleaning up
cap.release()
cv2.destroyAllWindows()