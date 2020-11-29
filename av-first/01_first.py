import av

container = av.open("target_1280.mp4")

for frame in container.decode(video=0):
  frame.to_image().save('frame-%04d.jpg' % frame.index)
