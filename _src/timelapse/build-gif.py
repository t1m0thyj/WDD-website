import io

# from apng import APNG, PNG
from PIL import Image

still_frames = [Image.open(f"image-{i}.png") for i in range(16)]
frames = []
durations = []
for i in range(len(still_frames)):
    frames.append(still_frames[i].convert("RGB"))
    durations.append(1500)
    for j in range(15):
        temp_frame = Image.blend(still_frames[i], still_frames[(i + 1) % len(still_frames)], (j + 1) / 15)
        frames.append(temp_frame.convert("RGB"))
        durations.append(500 // 15)

frames[0].save("WDD-timelapse.webp", format="WEBP", save_all=True, append_images=frames[1:], duration=durations, loop=0, quality=98, method=6)
# img = APNG()
# for i in range(len(frames)):
#     print(i)
#     bytes = io.BytesIO()
#     frames[i].save(bytes, format="PNG")
#     img.append(PNG.from_bytes(bytes.getvalue()), delay=durations[i])
# img.save("WDD-timelapse.apng")
