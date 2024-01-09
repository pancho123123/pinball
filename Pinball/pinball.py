import pygame, random
from random import randint
from pathlib import Path

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (0,0,255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball")
clock = pygame.time.Clock()
current_path = Path.cwd()
file_path = current_path / 'highscore.txt'

def draw_text1(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_text2(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/player2.png").convert()
		#self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.centery = 590
		self.speed_x = 0
		self.score = 0

	def update(self):
		self.speed_x = 0
		self.speed_y = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speed_x = -7
		if keystate[pygame.K_d]:
			self.speed_x = 7
		self.rect.x += self.speed_x
		
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/Ball1.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH // 5
		self.rect.y = HEIGHT // 2
		self.speedy = 4
		self.speedx = 4
		
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		
		if self.rect.left < 0 or self.rect.right > WIDTH:
		
			self.speedx = -self.speedx
		if self.rect.top < 0:
			self.speedy = -self.speedy

class Block1(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/block1.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.x_list = [100,200, 300, 400, 500, 600, 700]
		self.rect.x = random.choice(self.x_list)
		self.y_list = [100, 200, 300, 400]
		self.rect.y = random.choice(self.y_list)
		
	def update(self):
		pass

class Block2(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/block2.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.x_list = [100,200, 300, 400, 500, 600, 700]
		self.rect.x = random.choice(self.x_list)
		self.y_list = [100, 200, 300, 400]
		self.rect.y = random.choice(self.y_list)
		
	def update(self):
		pass
		
class Block3(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("img/block3.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.x_list = [100,200, 300, 400, 500, 600, 700]
		self.rect.x = random.choice(self.x_list)
		self.y_list = [100, 200, 300, 400]
		self.rect.y = random.choice(self.y_list)

	def update(self):
		pass
			
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def show_go_screen():
	
	screen.fill(BLACK)
	draw_text1(screen, "Pinball", 65, WIDTH // 2, HEIGHT // 4)
	draw_text1(screen, "-", 20, WIDTH // 2, HEIGHT // 2)
	draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 3/4)
	draw_text1(screen, "Created by: Francisco Carvajal", 10,  60, 625)
	
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

def get_high_score():
	with open(file_path,'r') as file:
		return file.read()

def show_game_over_screen():
	screen.fill(BLACK)
	if highest_score <= player.score:
		draw_text1(screen, "¡high score!", 60, WIDTH  // 2, HEIGHT * 1/4)
		draw_text1(screen, "score: "+str(player.score), 30, WIDTH // 2, HEIGHT // 2)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 4/5)
	else:
		draw_text1(screen, "score: "+str(player.score), 60, WIDTH // 2, HEIGHT * 1/3)
		draw_text1(screen, "Press Q", 20, WIDTH // 2, HEIGHT * 2/3)

	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					waiting = False

####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
	file = "img/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

### high score

try:
	highest_score = int(get_high_score())
except:
	highest_score = 0

# Cargar sonidos
explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
persiana_sound = pygame.mixer.Sound("sound/persiana.wav")

game_over = False
running = True
start = True
while running:
	screen.fill(BLACK)
	if game_over:

		show_game_over_screen()

		game_over = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		block1_list = pygame.sprite.Group()
		block2_list = pygame.sprite.Group()
		block3_list = pygame.sprite.Group()
		bar_list = pygame.sprite.Group() 
		
		player = Player()
		ball = Ball()
		all_sprites.add(player, ball)
		bar_list.add(player)

		for i in range(5):
			block1 = Block1()
			block2 = Block2()
			block3 = Block3()
				
			all_sprites.add(block1, block2, block3)
			block1_list.add(block1)
			block2_list.add(block2)
			block3_list.add(block3)
		
		
		player.score = 0

	if start:

		show_go_screen()

		start = False
		screen.fill(BLACK)
		all_sprites = pygame.sprite.Group()
		block1_list = pygame.sprite.Group()
		block2_list = pygame.sprite.Group()
		block3_list = pygame.sprite.Group()
		bar_list = pygame.sprite.Group() 
		
		player = Player()
		ball = Ball()
		all_sprites.add(player, ball)
		bar_list.add(player)
		
		for i in range(4):
			block1 = Block1()
			block2 = Block2()
			block3 = Block3()
				
			all_sprites.add(block1, block2, block3)
			block1_list.add(block1)
			block2_list.add(block2)
			block3_list.add(block3)
			
		
		player.score = 0
		


	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

		

	
	all_sprites.update()

	# limite barra gas
	if ball.rect.bottom > 600:
		game_over = True


	if len(block1_list) == 0 and len(block2_list) == 0 and len(block3_list) == 0:
		persiana_sound.play()
		for i in range(4):
			block1 = Block1()
			block2 = Block2()
			block3 = Block3()
				
			all_sprites.add(block1, block2, block3)
			block1_list.add(block1)
			block2_list.add(block2)
			block3_list.add(block3)
	
	# Checar colisiones - ball - block1
	hits = pygame.sprite.spritecollide(ball, block1_list, True)
	for hit in hits:
		player.score += 20
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
	
	# Checar colisiones - jugador - block2
	hits = pygame.sprite.spritecollide(ball, block2_list, True)
	for hit in hits:
		player.score += 50
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
			
	# Checar colisiones - ball - block3
	hits = pygame.sprite.spritecollide(ball, block3_list, True)
	for hit in hits:
		player.score += 80
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)

	# Checar colisiones - ball - bar
	hits = pygame.sprite.spritecollide(ball, bar_list, False)
	for hit in hits:
		ball.speedy = -ball.speedy
		
	all_sprites.draw(screen)

	#Marcador
	
	draw_text1(screen, str(player.score), 25, WIDTH // 2, 10)
	
	pygame.display.flip()