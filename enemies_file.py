import pygame, random, math
import utils
pygame.init()

class enemies_group_class():
	group_enemies = pygame.sprite.Group()


class enemies_spawner(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.image= pygame.image.load("sprites/enemies_spawer_1.png")
		
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		
		self.maxHP = 3
		self.HP = self.maxHP
		self.spawnSpeed = 2
		
		self.enemyType = 0
		self.spawnSlimeCD = 0
		self.spawnSlimeCDMax = utils.spawnSlimeCDMax
	
	def spawnEnemy(self, type, actualDifficulty, spawnerRect):
		self.spawnSlimeCD -= 1
		if self.spawnCD <= 0:
			newEnemy = Enemy_Slime()
			newEnemy.maxHP *= actualDifficulty
			newEnemy.HP *= actualDifficulty
			enemies_group_class.group_enemies.add(newEnemy)
			
			#random spawn location code
			
			
#BASIC_SLIME------------------------------------------------------------------------------------------------------------

spawnSlimeCD = 0
spawnSlimeCDMax = utils.spawnSlimeCDMax

def spawnSlime(actualDifficulty, mapWidth, mapHeight):
	global spawnSlimeCD, spawnSlimeCDMax
	spawnSlimeCD -= 1
	if spawnSlimeCD <= 0:
		newEnemy = Enemy_Slime()
		newEnemy.maxHP *= actualDifficulty
		newEnemy.HP *= actualDifficulty
		enemies_group_class.group_enemies.add(newEnemy)

		spawnSide = random.choice([1, 2, 3, 4])
		
		if spawnSide == 1:
			newEnemy.rect.x = -10
			newEnemy.rect.y = -10
		elif spawnSide == 2:
			newEnemy.rect.x = mapWidth + 10
			newEnemy.rect.y = -10
		elif spawnSide == 3:
			newEnemy.rect.x = -10
			newEnemy.rect.y = mapHeight + 10
		else:
			newEnemy.rect.x = mapWidth + 10
			newEnemy.rect.y = mapHeight + 10
			
		spawnSlimeCD = spawnSlimeCDMax

class Enemy_Slime(pygame.sprite.Sprite):
	def __init__(self):
			pygame.sprite.Sprite.__init__(self)
			
			self.name = pygame.font.Font(None, 20).render("Slime", 1, utils.black)
			self.image = pygame.image.load("sprites/enemy_slime_1.png")
			
			self.rect = self.image.get_rect()
			self.rect.x = 1100
			self.rect.y = 0
			
			self.maxHP = 2.0
			self.HP = self.maxHP
			self.speed = random.choice([2, 2, 2, 2, 2, 2, 2, 3, 4])
			
			self.hbWidth = 45
			self.hbHeight = 5
			self.hbBase = pygame.Surface((self.hbWidth, self.hbHeight))
			
	def stalkPlayer(self, player):
		xdiff = (player.rect.x + player.rect.width/2) - self.rect.x + self.rect.width/2
		ydiff = (player.rect.y + player.rect.height/2) - self.rect.y + self.rect.height/2
		
		magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
		numFrames = int(magnitude / self.speed)
		
		movex = xdiff/numFrames
		movey = ydiff/numFrames
		
		self.rect.x += movex
		self.rect.y += movey
		
	def drawBarName(self):
		width = int((self.HP / self.maxHP) * self.hbWidth)
		nameRect = self.name.get_rect()
		
		hb = pygame.Surface((width, self.hbHeight))
		hb.fill(utils.green)
		
		self.hbBase.fill(utils.red)
		self.hbBase.blit(hb, (0, 0))
		
		self.image.blit(self.hbBase, (5, nameRect.h))
		
		self.image.blit(self.name, (self.image.get_rect().w/2 -  nameRect.w/2, 0))
		
	def takeDemage(self):
		self.HP -= 1
		if self.HP <= 0:
			self.destroy()
			return True
		
	def destroy(self):
		self.kill()
		
	def update(self, player):
		self.drawBarName()
		self.stalkPlayer(player)
