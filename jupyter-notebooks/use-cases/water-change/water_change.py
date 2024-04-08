import numpy as np
import cv2 as cv
import imutils
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from bokeh.io import output_file, show
from bokeh.plotting import figure
import bokeh.plotting as bk


# Read image
a = cv.imread('20160707.tif')
hsv_a = cv.cvtColor(a, cv.COLOR_BGR2HSV)

b = cv.imread('20160722.tif')
hsv_b = cv.cvtColor(b, cv.COLOR_BGR2HSV)

#defining upper and lower bounds to find "blue" in img
low = np.array([55, 0, 0])
high = np.array([118, 255, 255])

#create threshold based upon upper and lower bounds
inner_a = cv.inRange(hsv_a, low, high)
inner_b = cv.inRange(hsv_b, low, high)

cv.imwrite('inner_a.png',inner_a)
cv.imwrite('inner_b.png',inner_b)

#used for eroding and dilating img
kernel = np.ones((5,5),np.uint8)

#erosion and dilation to eliminate noise
erosion_a = cv.erode(inner_a,kernel,iterations = 2)
erosion_b = cv.erode(inner_b,kernel,iterations = 2)

innerA = cv.dilate(erosion_a,kernel,iterations = 1)
innerB = cv.dilate(erosion_b,kernel,iterations = 1)

cv.imwrite('innerA.png',innerA)
cv.imwrite('innerB.png',innerB)
  
# compute the exact Euclidean distance from every binary
# pixel to the nearest zero pixel, then find peaks in this
# distance map
eucl_a = ndimage.distance_transform_edt(innerA)
eucl_b = ndimage.distance_transform_edt(innerB)

localMaxA = peak_local_max(eucl_a, indices=False, labels=innerA)
localMaxB = peak_local_max(eucl_b, indices=False, labels=innerB)


# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm
markers_a = ndimage.label(localMaxA, structure=np.ones((3, 3)))[0]
markers_b = ndimage.label(localMaxB, structure=np.ones((3, 3)))[0]

labels_a = watershed(-eucl_a, markers_a, mask=innerA)
labels_b = watershed(-eucl_b, markers_b, mask=innerB)

def get_area(labels, inner_mask, img):
    area = 0
    for label in np.unique(labels):

	# ignoring zero label bc it represents background/land
        if label== 0:
            continue

	# otherwise, allocate memory for the label region and draw
	# it on the mask
        mask = np.zeros(inner_mask.shape, dtype="uint8")
        mask[labels == label] = 255
    
	# detect contours in the mask and grab the largest one
        contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        #fill contour area with color <= idk if this is necessary
        cv.fillPoly(img, pts=contours, color=(0,255,255))

    #get area from contours
        a = cv.contourArea(contours[0])
        area+=a

    #saving image with contour filled in (optional visualization)
    cv.imwrite('mask.png', img)

    return area

#apply function to both images to get contour and area
area_a = get_area(labels_a, innerA, a)
area_b = get_area(labels_b, innerB, b)

#calculate water level difference
water_level_diff = area_b/float(area_a)

dates = ['2016-07-13', '2016-09-10']
pixels = [area_a, area_b]

plt = figure(x_range=dates, plot_height=275, title="Reservoir Pixels",
           toolbar_location=None, tools="")

plt.vbar(x=dates, top=pixels, width=0.3, fill_color="#cfe31e")

plt.xgrid.grid_line_color = None
plt.y_range.start = 0
plt.xaxis.axis_label = "Date"
plt.yaxis.axis_label = "Sum(Pixels)"

#saves as a html file
bk.save(plt)
show(plt)

if __name__ == "__main__":
    print(area_a)
    print(area_b)
    print(water_level_diff)
    print("Percent change {0}%".format(((area_b/float(area_a))-1)*100))