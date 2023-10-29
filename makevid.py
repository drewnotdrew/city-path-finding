from PIL import Image

gif = []
for i in range(0, 204):
    gif.append(Image.open(f"out/routes{i}.jpg"))

gif[0].save("anim.gif", save_all=True, append_images=gif[1:], optimize=False, duration=100)