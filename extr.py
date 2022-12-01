#How to operate - write 'python embed.py' into the shell. To decrypt, write 'python extract.py'

from PIL import Image
import random


def modify_pixel(pixel, plane, bit, modifier):
	m = modifier * (2**(7 - bit))
	r = pixel[0] + m if plane == 0 else pixel[0]
	g = pixel[1] + m if plane == 1 else pixel[1]
	b = pixel[2] + m if plane == 2 else pixel[2]
	return (r, g, b)


key = 123
colourPlane = 0  # 0 is red, 1 is green, 2 is blue
significantBit = 7  # 7 is the least significant bit, 0 is the most
coverImage = "img/scifi.bmp"
secret = str(input('What do you want to send? : '))

image = Image.open(coverImage)
dimensions = image.size  # dimensions[0] is width, dimensions[1] is height
pixels = image.load(
)  # pixels[0,0] returns a list of the (R,G,B)-values of the pixel at position (0,0) (top left origin)

shuffledIndices = list(
    range(0, dimensions[0] * dimensions[1])
)  # generates a list of the numbers from 0 to the number of pixels in the cover-image
random.seed(key)
random.shuffle(
    shuffledIndices)  # re-orders the list using the key to seed the randomness

# Convert the secret into ASCII bits
# Prepend the length of the secret to it to aid extraction
sbits = "".join(format(ord(char), "b").zfill(7) for char in secret)
lbits = format(len(secret), "b").zfill(14)
bits = lbits + sbits

# Embed the secret bits into the re-ordered pixels in the chosen colour plane
for i in range(len(bits)):
	x = shuffledIndices[i] % dimensions[0]
	y = int(shuffledIndices[i] / dimensions[0])
	p = format(pixels[x, y][colourPlane], "b").zfill(8)

	# If the existing value is 0, only change it if the secret bit is 1
	if p[significantBit] == "0":
		if bits[i] == "1":
			pixels[x, y] = modify_pixel(pixels[x, y], colourPlane,
			                            significantBit, 1)
	# If the existing value is 1, only change it if the secret bit is 0
	else:
		if bits[i] == "0":
			pixels[x, y] = modify_pixel(pixels[x, y], colourPlane,
			                            significantBit, -1)

# Output the stego-image
image.save("stego-image.bmp")
