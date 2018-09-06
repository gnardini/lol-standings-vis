import cv2
import numpy as np

# Copied from https://stackoverflow.com/questions/3803888/opencv-how-to-load-png-images-with-4-channels
def read_transparent_png(filename):
    image_4channel = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    alpha_channel = image_4channel[:,:,3]
    rgb_channels = image_4channel[:,:,:3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white
    return final_image.astype(np.uint8)

def create_base_img(height, width, rows, icon_size, space_between):
    img = np.ones((height,width,3), np.uint8) * 255
    chart_base = height - 40
    for i in range(rows):
        y = chart_base - 35 - (icon_size + space_between) * i
        cv2.line(img,(100,y),(width,y),(128,128,128),2)
    cv2.line(img,(100,chart_base),(width,chart_base),(0,0,0),2)
    cv2.line(img,(100,chart_base),(100,40),(0,0,0),2)
    return img
