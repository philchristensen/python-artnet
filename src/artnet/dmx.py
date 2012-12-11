# sketches about implementing a constant flow of DMXOut packets

import time

fps = 40.0

last_frame = None
frame_queue = []
running = True
while(running):
	now = time.time()
	send_next_frame() if frame_queue else send_last_frame()
	elapsed = time.time() - now
	frames, excess = divmod(elapsed, 1.0 / fps)
	while(frames):
		frame_queue.pop()
		frames -= 1
	
	time.sleep(excess)
	