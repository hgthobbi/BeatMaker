#beat maker application, code from https://www.youtube.com/watch?v=F3J3PZj0zi0

#pygame libarary contains mixer and timing components to ensure the app has proper time quantizing
import pygame
from pygame import mixer
pygame.init()

#controlling height and width of screen, hard coded for now, look into dimensions based on sytem display
WIDTH = 1400
HEIGHT = 800

#import colors used for the app
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

#initialize the base display screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font('freesansbold.ttf', 32)

#timer 
fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
# -1 is used to show not active, 1 is used to show active
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

# load in sounds
clap = mixer.Sound('sounds/clap.wav')
crash = mixer.Sound('sounds/crash.wav')
hi_hat = mixer.Sound('sounds/hi hat.WAV')
kick = mixer.Sound('sounds/kick.WAV')
snare = mixer.Sound('sounds/snare.WAV')
tom = mixer.Sound('sounds/tom.WAV')

def play_notes():
	for i in range(len(clicked)):
		if clicked[i][active_beat] == 1:
			if i == 0: 
				hi_hat.play()
			if i == 1: 
				snare.play()
			if i == 2: 
				kick.play()
			if i == 3: 
				crash.play()
			if i == 4: 
				clap.play()
			if i == 5: 
				tom.play()					

#this method will draw out the grid layout for the layout
def draw_grid(clicks, beat):
	instrument_menu = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT - 195], 5)
	control_menu = pygame.draw.rect(screen, grey, [0, HEIGHT - 200, WIDTH, 200], 5)
	
	colors = [grey, white, grey]
	hi_hat_text = label_font.render('Hi Hat', True, white)
	screen.blit(hi_hat_text, (50, 30))
	snare_text = label_font.render('Snare', True, white)
	screen.blit(snare_text, (50, 130))
	kick_text = label_font.render('Kick', True, white)
	screen.blit(kick_text, (60, 230))
	crash_text = label_font.render('Crash', True, white)
	screen.blit(crash_text, (50, 330))
	clap_text = label_font.render('Clap', True, white)
	screen.blit(clap_text, (60, 430))
	floor_text = label_font.render('Floor Tom', True, white)
	screen.blit(floor_text, (25, 530))
	for i in range(instruments):
		pygame.draw.line(screen, grey, (0, (i*100) + 100), (200, (i*100) + 100), 3)
	

	for i in range(beats):
		for j in range(instruments):
			if clicks[j][i] == -1:
				color = grey
			else:
				color = green
			# // is floor divide
			rect = pygame.draw.rect(screen, color, [i * ((WIDTH-200) // beats) + 200, (j * 100) + 5, ((WIDTH-200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)
			pygame.draw.rect(screen, gold, [i * ((WIDTH-200) // beats) + 200, (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)
			pygame.draw.rect(screen, black, [i * ((WIDTH-200) // beats) + 200, (j * 100), ((WIDTH-200) // beats), ((HEIGHT - 200) // instruments)], 2, 5)
			boxes.append((rect, (i, j)))

		active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
	return boxes


#main game loop
run = True
while run:
	timer.tick(fps)
	screen.fill(black)
	boxes = draw_grid(clicked, active_beat)
	if beat_changed:
		play_notes()
		beat_changed = False

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in range(len(boxes)):
				if boxes[i][0].collidepoint(event.pos):
					coords = boxes[i][1]
					clicked[coords[1]][coords[0]] *= -1

	beat_length = 3600 // bpm

	if playing: 
		if active_length < beat_length:
			active_length += 1
		else:
			active_length = 0
			if active_beat < beats - 1:
				active_beat += 1
				beat_changed = True 
			else:
				active_beat = 0
				beat_changed = True

	pygame.display.flip()
pygame.quit()

