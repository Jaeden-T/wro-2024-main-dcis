import cv2
import numpy as np
import math
import statistics

def detectPosition(image_files):
    def get_contours_center(contour):
        M = cv2.moments(contour)
        if M['m00'] == 0:
            return (0, 0)
        cx = int(M['m00'] / M['m10'])
        cy = int(M['m00'] / M['m01'])
        return (cx, cy)

    def classify_position(cx, image_width):
        if cx < image_width / 3:
            return "Left"
        elif cx > 2 * image_width / 3:
            return "Right"
        else:
            return "Center"

    prev_centers = []
    movement_data = []

    # Assuming all images have the same size, let's get the image width
    sample_image = cv2.imread(image_files[0])
    image_height, image_width, _ = sample_image.shape

    for img_file in image_files:
        img = cv2.imread(img_file)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        lower_green = np.array([40, 40, 40])
        upper_green = np.array([90, 255, 255])

        greenMask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Merge the Masks
        mask = cv2.bitwise_or(greenMask, mask)
        imgray = cv2.bitwise_or(img, img, mask=mask)

        # Perform edge detection using Canny algorithm
        edged = cv2.Canny(imgray, 30, 200)

        # Find contours in the image
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        current_centers = []
        for contour in contours:
            cx, cy = get_contours_center(contour)
            current_centers.append((cx, cy))

        if prev_centers:
            for prev_center, curr_center in zip(prev_centers, current_centers):
                movement_x = abs(curr_center[0] - prev_center[0])
                movement_y = abs(curr_center[1] - prev_center[1])
                total_movement = math.sqrt(movement_x**2 + movement_y**2)
                movement_data.append((total_movement, curr_center))

        prev_centers = current_centers

    # Find the contour that moved the most
    if movement_data:
        max_movement, max_center = max(movement_data, key=lambda x: x[0])
        position = classify_position(max_center[0], image_width)

        return [position, max_center]

    else:
        return 0
