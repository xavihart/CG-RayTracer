import cv2
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--path", default="./", type=str, help="the relative path for the image to be operated")
parser.add_argument("--frac", default=2, type=int, help="the fraction to be compressed")
args = parser.parse_args()
frac = args.frac
pth = args.path
root = "./"
photo_path = os.path.join(root, pth)
img = cv2.imread(photo_path)
img2 = cv2.resize(img, (img.shape[1] // frac, img.shape[0] // frac))
print(img2.shape)
cv2.imwrite("./trans.jpg", img2)

