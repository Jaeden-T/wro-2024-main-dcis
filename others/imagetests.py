import cv2
import numpy as np
import math
import statistics

# Load the image
img = cv2.imread('main.png')


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lowwer_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

lower_green = np.array([40, 40, 40])
upper_green = np.array([90, 255, 255])

greenMask = cv2.inRange(hsv, lower_green, upper_green)
mask = cv2.inRange(hsv, lowwer_red, upper_red)


# #* Merge the Mask
mask = cv2.bitwise_or(greenMask, mask)

imgray = cv2.bitwise_or(img, img, mask=mask)
# imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# (thresh, im_bw) = cv2.threshold(imgray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


cv2.imshow("Bitwise Or", imgray)

# Perform edge  using Canny algorithm
edged = cv2.Canny(imgray, 30, 200)

# Find contours in the image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


newContours  = []
frameContoursY = []
frameContoursX = []
# for x in contours:
#     statistics.mean()

avgXContour = []
avgYContour =[]
if len(contours) > 0:
    # Draw contours on the original image
    for contour in contours:
        
        # Draw contours
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 3)

        # Get all points from the contour
        for point in contour:
            # Draw red dots on these corner poin
            # print(point)
            cv2.circle(img, (point[0][0], point[0][1]), 5, (0, 0, 255), -1)

        
        print(contour[0][0][1])
        
        for x in contour:
            tempX = []
            tempY = []
            if x[0][0] > 0:
                tempX.append(x[0][0])
            if x[0][1] > 0:
                tempY.append(x[0][1])
        avgXContour.append(statistics.mean(tempX))
        avgYContour.append(statistics.mean(tempY))
        
        
    # Display the output

        
        
    
    cv2.imshow('Edges', img)
    # cv2.imshow('Contours', img)
    
    # cv2.imshow("blured", imgray)
    
    print()
else:
    print("No contours found.")

print()

numOfContours = len(contours)

frameContoursX.append(avgXContour)
frameContoursY.append(avgYContour)
movement = 0
tempMovementY = []
for x in range(0,numOfContours):
    tempMovementY.append = []

tempMovementX = []
for x in range(0, numOfContours):
    tempMovementX.append = []


for x in range(0, numOfContours):
    for y in range(0, len(frameContoursY)):
        tempMovementY[x].append(abs(frameContoursY[1] - frameContoursY[y-1]))
        
    for b in range(0, len(frameContoursX)):
        tempMovementY[x].append(abs(frameContoursY[1] - frameContoursY[b-1]))
       
movementY= []
movementX = []
for x in range(0, numOfContours):
    # Avg Momenet of each:
    movementY.append(statistics.mean(tempMovementY[x]))
    movementX.append(statistics.mean(tempMovementX[x]))

    # Avg Momenet of each:
# Wait for a key press and then close all windows


print(avgXContour)
print(avgYContour)
cv2.waitKey(0)
cv2.destroyAllWindows()
