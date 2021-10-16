
from PIL import Image
import random
IMAGE_NAME = "roadster.jpg"
img = Image.open(IMAGE_NAME)

# img = Image.open(f)  # You can also use this on a local file; just put the local filename in quotes in place of f.
# img.show()  # Send the image to your OS to be displayed as a temporary file
print(img.size)  # A tuple.  Note: width first THEN height.  PIL goes [x, y] with y counting from the top of the frame.
width = img.size[0]
height = img.size[1]

print("width: " + str(width))
print("height: " + str(height))

#
# Ok, so let’s say we want to represent an image using a small number of colors.
#If we restrict R, G, and B to three values each – 0, 127, or 255 – then that makes 3 * 3 * 3 = 27 colors.
#If we restrict R, G, and B to two values each – only min or max, 0 or 255 – then that makes 2 * 2 * 2 = 8 colors.
#First, let’s code up these two possibilities.

# •	27-color naïve quantization: Take each pixel in turn.  For R, G, and B individually,
# if the value is less than         255 // 3, make it 0.  If it’s greater than 255 * 2 // 3, make it 255.  Otherwise, make it 127.
# •	8-color naïve quantization: Take each pixel in turn.
# For R, G, and B individually, if the value is less than 128, make it 0.  If it’s greater or equal, make it 255.


pix = img.load()  # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.

# # 8-color naive quantization
# for x in range(width):
#     for y in range(height):
#         R,G,B = pix[x,y]
#         new_pixel = [R,G,B]
#         for i in range(len(new_pixel)):
#             if new_pixel[i] < 128: new_pixel[i] = 0
#             else: new_pixel[i] = 255
#             print(new_pixel)
#         pix[x,y] = tuple(new_pixel)


# # 27-color naive quantization
# for x in range(width):
#     for y in range(height):
#         R,G,B = pix[x,y]
#         new_pixel = [R,G,B]
#         for i in range(len(new_pixel)):
#             if new_pixel[i] < 255//3: new_pixel[i] = 0
#             elif new_pixel[i] < 255 * 2 // 3: new_pixel[i] = 255
#             else: new_pixel[i] = 127
#             # print(new_pixel)
#         pix[x,y] = tuple(new_pixel)

#
# 1)	Specify a value of K.
# 2)	Choose K random elements of the set.  (In our case, the specific RGB color values at K random pixels from the image.)  Call these the means, though we haven’t averaged anything yet.
# 3)	Loop over every single pixel and assign it to the mean that is closest (has the smallest squared error, as explained above).
# 4)	Take each group of pixels generated in step 3 and find the actual mean of those pixels (so, the individually averaged RGB values of all pixels in that group).
# 5)	Repeat steps 3 and 4.  As you do so, the values of the means will change, which will cause pixels to move between groups.  Keep repeating until this becomes stable; that is, until no pixel changes group.  (This means you’ll need to keep track of the groups and how many pixels move in or out during each round.)
# 6)	When the process resolves, you’ve now found the K specific means that minimized the squared error!  The algorithm isn’t guaranteed to converge to optimality, but in practice it is quite robust.



def calculate_distance(pixel1, pixel2):
    return (pixel1[0]-pixel2[0])**2 + (pixel1[1]-pixel2[1])**2 + (pixel1[2]-pixel2[2])**2


def calculate_means(dictionary):
    new_means = []
    for key in dictionary.keys():
        array = dictionary[key]
        R_sum, G_sum, B_sum = 0, 0, 0
        for coordinate in array:
            elem = pix[coordinate[0], coordinate[1]]
            R_sum += elem[0]
            G_sum += elem[1]
            B_sum += elem[2]
        new_means.append((R_sum/len(array), G_sum/len(array), B_sum/len(array)))
    return new_means

K = 27


arr = []
for x in range(width):
    for y in range(height):
        arr.append((x,y))

means = random.sample(arr, K)
for i in range(len(means)):
    means[i] = pix[means[i][0], means[i][1]]

done = False
old_set = None
i = 0
while not done:
    print("Gen " + str(i))
    i+=1
    d = {}
    for key in means:
        d[key] = set()
    for x in range((width)):
        for y in range((height)):
            distance_array = [calculate_distance(pix[x,y], mean) for mean in means]
            d[means[distance_array.index(min(distance_array))]].add((x,y))

    new_set = []
    for key in d: new_set.append(d[key])
    if new_set == old_set: done = True
    else:
        old_set = new_set
        means = calculate_means(d)


for key in d:
    int_key = (int(key[0]), int(key[1]), int(key[2]))
    for coordinate in d[key]:
        print(coordinate)
        pix[int(coordinate[0]), int(coordinate[1])] = int_key


# for key in d.keys():
#     print(key, len(d[key]))

# print(means)





# print(pix)
# pix[2,5] = (255, 255, 255)  # Set the pixel to white.  Note this is called on “pix”, but it modifies “img”.
img.show()  # Now, you should see a single white pixel near the upper left corner
img.save("my_image.png")  # Save the resulting image.  Alter your filename as necessary.
