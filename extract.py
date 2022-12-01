from PIL import Image
import random

# Set the configurations
key = 123
colourPlane = 0
significantBit  = 7
stegoImage = "stego-image.bmp"

# Read the stego-image data
image = Image.open(stegoImage)
dimensions = image.size
pixels = image.load()

# Replicate the pixel embedding order
shuffledIndices = list(range(0, dimensions[0] * dimensions[1]))
random.seed(key)
random.shuffle(shuffledIndices)

# Extract the embedded data by reversing the embedding process
extractedBits = []
for i in shuffledIndices:
	x = i % dimensions[0]
	y = int(i / dimensions[0])
	p = format(pixels[x, y][colourPlane], "b").zfill(8)
	extractedBits.append(p[significantBit])

# Determine the length of the secret
extractedLengthBits = extractedBits[:14]
extractedLength = 0
for i in range(len(extractedLengthBits)):
	extractedLength += int(extractedLengthBits[i]) * (2 ** (13 - i))

# Convert the ASCII bits to the secret
extractedSecretASCII = []
for i in range(0, extractedLength):
	a = 0
	for j in range(0, 7):
		a += int(extractedBits[14 + i * 7 + j]) * (2 ** (6 - j))
	extractedSecretASCII.append(chr(a))

print("".join(extractedSecretASCII))
