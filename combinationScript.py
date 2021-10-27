# based on Jonas Wagner's script https://29a.ch/2009/5/14/concatenating-images-using-python
from PIL import Image
import sys

def change_size(height_old, height_new, width):
	percentage = float(height_new)/float(height_old)
	width = int(width * percentage)
	return width

if not len(sys.argv) > 3:
    raise SystemExit("Usage: %s src1 [src2] .. dest" % sys.argv[0])


images = list(map(Image.open, sys.argv[1:-1]))

mh = min(i.size[1] for i in images)

for value,i in enumerate(images, start = 0):
	if mh < i.size[1]:
		new_img = i.resize((change_size(i.size[1], mh, i.size[0]), mh), Image.ANTIALIAS)
		images[value] = new_img

w = sum(i.size[0] for i in images)

result = Image.new("RGBA", (w + (50* (len(images)-1)), mh))

x = 0
for i in images:
    result.paste(i, (x, 0))
    x += i.size[0] + 50

result.save(sys.argv[-1])
