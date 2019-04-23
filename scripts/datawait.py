import time

# A simple function for waiting (and printing out how much time has elapsed)
def rest(seconds):
	for x in range(seconds):
		time.sleep(1)
		print(x + 1)
