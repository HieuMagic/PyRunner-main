import pygame
from sys import exit
from random import randint, choice

class MiniPlayer(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

class Game():
	def display_score(self):
		self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
		self.score_surf = self.test_font.render(f'Score: {self.current_time}',False,(64,64,64))
		self.score_rect = self.score_surf.get_rect(center = (400,50))
		self.display.blit(self.score_surf,self.score_rect)
		return self.current_time

	def collision_sprite(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.obstacle_group,False):
			self.obstacle_group.empty()
			return False
		else: return True

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('Runner')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((800,400))
		self.display = pygame.Surface((800,400))
		self.test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
		self.game_active = False
		self.start_time = 0
		self.score = 0
		self.bg_music = pygame.mixer.Sound('audio/music.wav')
		self.bg_music.play(loops = -1)

		#Groups
		self.player = pygame.sprite.GroupSingle()
		self.player.add(MiniPlayer())

		self.obstacle_group = pygame.sprite.Group()

		self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
		self.ground_surface = pygame.image.load('graphics/ground.png').convert()

		# Intro screen
		self.player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
		self.player_stand = pygame.transform.rotozoom(self.player_stand,0,2)
		self.player_stand_rect = self.player_stand.get_rect(center = (400,200))

		self.game_name = self.test_font.render('Pixel Runner',False,(111,196,169))
		self.game_name_rect = self.game_name.get_rect(center = (400,80))

		self.game_message = self.test_font.render('Press space to run',False,(111,196,169))
		self.game_message_rect = self.game_message.get_rect(center = (400,330))

		# Timer 
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1500)

	def minigame(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

				if self.game_active:
					if event.type == self.obstacle_timer:
						self.obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
				
				else:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						self.game_active = True
						self.start_time = int(pygame.time.get_ticks() / 1000)


			if self.game_active:
				self.display.blit(self.sky_surface,(0,0))
				self.display.blit(self.ground_surface,(0,300))
				self.score = self.display_score()
				
				self.player.draw(self.display)
				self.player.update()

				self.obstacle_group.draw(self.display)
				self.obstacle_group.update()

				self.game_active = self.collision_sprite()
				
			else:
				self.display.fill((94,129,162))
				self.display.blit(self.player_stand,self.player_stand_rect)

				score_message = self.test_font.render(f'Your score: {self.score}',False,(111,196,169))
				score_message_rect = score_message.get_rect(center = (400,330))
				self.display.blit(self.game_name,self.game_name_rect)

				if self.score == 0: self.display.blit(self.game_message,self.game_message_rect)
				else: self.display.blit(score_message,score_message_rect)

			pygame.display.update()
			self.screen.blit(self.display,(0,0))
			self.clock.tick(60)
  
Game().minigame()