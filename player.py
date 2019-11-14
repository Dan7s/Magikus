import pygame, math, random 
import utils
pygame.init()

#PLAYER----------------------------------------------------------------------------------------------------------------

class PlayerActive(pygame.sprite.Sprite):
	
		def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			
			self.player_state = "2"
			self.image = pygame.image.load("sprites/player_sprite" + str(self.player_state) +".png")
			self.rect = self.image.get_rect()
			
			self.rect.x = 400
			self.rect.y = 400
			self.speed = 10
			
			self.healthMax = 10
			self.health = self.healthMax
			self.mana = pygame.sprite.Group()
			self.manaMax = 40
			self.bullets = pygame.sprite.Group()
			self.exp = 0
			
			#simple skill list
			self.spellbinding = {
				'wave' : self.summon_wave,
				'wall' : self.summon_wall,
				'heal' : self.heal_spell,
			}
			
			self.isAlive = True
			
			
		def move(self, xdir, ydir):
			self.rect.x += xdir*self.speed
			self.rect.y += ydir*self.speed
			
			
		def rotating(self, cur):
			quater = [0, 0]
			if cur[0] < self.rect.x + (self.image.get_rect().width/2):
				quater[0] = -1
			else:
				quater[0] = 1
			if cur[1] < self.rect.y + (self.image.get_rect().height/2):
				quater[1] = -1
			else:
				quater[1] = 1
			
			if quater == [1, -1]:
				h = -(2*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				i = -(0.5*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				if cur[1] < h:
					self.player_state = "1"
				if cur[1] > h and cur[1] < i:
					self.player_state = "2"
				if cur[1] > i:
					self.player_state = "3"
						
			elif quater == [-1, -1]:
				f = -(-2*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				g = -(-0.5*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				if cur[1] < f:
					self.player_state = "1"
				if cur[1] > f and cur[1] < g:
					self.player_state = "8"
				if cur[1] > g:
					self.player_state = "7"
					
			elif quater == [-1, 1]:
				h = -(2*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				i = -(0.5*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				if cur[1] < i:
					self.player_state = "7"
				if cur[1] > i and cur[1] < h:
					self.player_state = "6"
				if cur[1] > h:
					self.player_state = "5"
				
			elif quater == [1, 1]:
				f = -(-2*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				g = -(-0.5*(cur[0] - (self.rect.x + (self.image.get_rect().width/2))) - (self.rect.y + (self.image.get_rect().height/2)))
				if cur[1] < g:
					self.player_state = "3"
				if cur[1] > g and cur[1] < f:
					self.player_state = "4"
				if cur[1] > f:
					self.player_state = "5"
			
		def spawnMana(self):
			self.mana.add(Bullet())
			
		def moveMana(self):
			self.image = pygame.image.load("sprites/player_sprite" + str(self.player_state) +".png")
			for obj in self.mana:
				if obj.rect.x + obj.rect.width >= self.rect.width or obj.rect.x <= 0:
					obj.movex *= -1
					
				if obj.rect.y + obj.rect.height >= self.rect.height or obj.rect.y <= 0:
					obj.movey *= -1
				
				obj.rect.x += obj.movex
				obj.rect.y += obj.movey

				self.image.blit(obj.image, obj.rect)
		
		def shoot(self, target):
			if utils.cd.get('shoot') <= 0 and self.mana:
				utils.cd['shoot'] = utils.cdMax.get('shoot')
				bullet = self.mana.sprites()[0]
				self.mana.remove(bullet)
				
				bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.height/2
				bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.width/2
				
				bullet.basic_shoot(target)
				self.bullets.add(bullet)

		def summon_wave(self, target):
			if len(self.mana) >= utils.cost.get('wave') and utils.cd.get('wave') <= 0:
				utils.cd['wave'] = utils.cdMax.get('wave')
				for x in range(0, utils.cost.get('wave')):
					bullet = self.mana.sprites()[0]
					self.mana.remove(bullet)
					
					bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.height/2
					bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.width/2
					
					bullet.wave(target)
					self.bullets.add(bullet)

		def summon_wall(self, target):
			if len(self.mana) >= utils.cost.get('wall') and utils.cd.get('wall') <= 0:
				utils.cd['wall'] = utils.cdMax.get('wall')
				if self.player_state == "2":
					target_mod_x = 30
					target_mod_y = 30
					target = target[0] - 60, target[1] - 60
				elif self.player_state == "4":
					target_mod_x = -30
					target_mod_y = 30
					target = target[0] + 60, target[1] - 60
				elif self.player_state == "6":
					target_mod_x = -30
					target_mod_y = -30
					target = target[0] + 60, target[1] + 60
				elif self.player_state == "8":
					target_mod_x = 30
					target_mod_y = -30
					target = target[0] - 60, target[1] + 60
				elif self.player_state == "1" or self.player_state == "5":
					target_mod_x = 40
					target_mod_y = 1
					target = target[0] - 80, target[1] - 0
				elif self.player_state == "3" or self.player_state == "7":
					target_mod_x = 1
					target_mod_y = 40
					target = target[0], target[1] - 80
				for x in range(0, utils.cost.get('wall')):
					bullet = self.mana.sprites()[0]
					self.mana.remove(bullet)

					bullet.rect.x = self.rect.x + self.rect.width/2 - bullet.rect.height/2
					bullet.rect.y = self.rect.y + self.rect.height/2 - bullet.rect.width/2
					
					bullet.wall(target)
					self.bullets.add(bullet)
					
					target = target[0] + target_mod_x, target[1] + target_mod_y
					
					
		def heal_spell(self, target):
			if len(self.mana) >= utils.cost.get('heal') and self.health < self.healthMax and utils.cd.get('heal') <= 0:
				utils.cd['heal'] = utils.cdMax.get('heal')
				bullet = self.mana.sprites()[0:utils.cost.get('heal')]
				self.mana.remove(bullet)
				self.health += 1
				
		def takeDemage(self):
			self.health -= 1
			
			if self.health == 0:
				self.destroy()
				
		def destroy(self):
			self.isAlive = False
			
		def addExp(self, value):
			self.exp += value
				
		def update(self, cur, activeMap, mapWidth, mapHeight):
			if self.isAlive:
				for cd in utils.cd:
					utils.cd[cd] -= 1
				
				self.rotating(cur)
				activeMap.blit(self.image, self.rect)
				
				for obj in self.bullets:
					obj.update(mapWidth, mapHeight)
					activeMap.blit(obj.image, obj.rect)
					
				self.bullets.update(mapWidth, mapHeight)
				self.bullets.draw(activeMap)
			
#ATAKS------------------------------------------------------------------------------------------------------------------

class Bullet(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load("sprites/mana.png")
		self.rect = self.image.get_rect()
		
		self.rect.x = random.randint(5, 55)
		self.rect.y = random.randint(5, 55)
		
		self.movex = random.choice([-1, 1])
		self.movey = random.choice([-1, 1])
		self.speed = 12.0
	
	def basic_shoot(self, target):
		xdiff = target[0] - self.rect.x - self.rect.width/2
		ydiff = target[1] - self.rect.y - self.rect.height/2
		magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
		numFrames = int(magnitude / self.speed) + 1
		self.movex = xdiff/numFrames
		self.movey = ydiff/numFrames
		travelx = self.movex * numFrames
		travely = self.movey * numFrames
		self.rect.x += xdiff - travelx
		self.rect.y += ydiff - travely

	def wave(self, target):
		travel_end_x = target[0] + random.randint(-100, 100)
		travel_end_y = target[1] + random.randint(-100, 100)
		xdiff = travel_end_x - self.rect.x - self.rect.width/2
		ydiff = travel_end_y - self.rect.y - self.rect.height/2
		magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
		numFrames = int(magnitude / self.speed) + 1
		self.movex = xdiff/numFrames
		self.movey = ydiff/numFrames
		travelx = self.movex * numFrames
		travely = self.movey * numFrames
		self.rect.x += xdiff - travelx
		self.rect.y += ydiff - travely

	def wall(self, target):
		xdiff = target[0] - self.rect.x - self.rect.width/2
		ydiff = target[1] - self.rect.y - self.rect.height/2
		magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
		numFrames = int(magnitude / self.speed) + 1
		if xdiff <= target[0] and ydiff <= target[1]:
			self.movex = 0
			self.movey = 0
		else:
			self.movex = xdiff/numFrames
			self.movey = ydiff/numFrames
		travelx = self.movex * numFrames
		travely = self.movey * numFrames
		self.rect.x += xdiff - travelx
		self.rect.y += ydiff - travely
		
	def destroy(self):
		self.kill()
		
	def checkDist(self, mapWidth, mapHeight):
		if self.rect.x < -10 or self.rect.x > mapWidth:
			self.destroy()
		if self.rect.y < -10 or self.rect.y > mapHeight:
			self.destroy()
		
	def update(self, mapWidth, mapHeight):
		self.checkDist(mapWidth, mapHeight)
		self.rect.x += self.movex
		self.rect.y += self.movey
