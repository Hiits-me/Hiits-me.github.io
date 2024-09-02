import glob
import os
from PIL import Image

# designate a path
path = './*.png'
i = 1

files = glob.glob(path)

# rename all .png file
for file in files:
    os.rename(file, './img' + str(i) + '.png')
    i+=1

# concatenate all .png files into a .gif
pictures=[]
for j in range(i-1):
    picture = 'img' + str(j+1) + '.png'
    img = Image.open(picture)
    pictures.append(img)

# save a gif file with some settings
pictures[0].save('heatmap.gif', save_all=True, append_images=pictures[1:], optimize=False, duration=400, loop=0)