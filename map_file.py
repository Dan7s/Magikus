import pygame, utils, random, enemies_file
pygame.init()

#main_map
class mainMap():
	def __init__(self):
		self.mapimage = None
		self.chunkSize = 300
		self.activeMap = None
		self.offsetX = 0
		self.offsetY = 0
		self.scrollSpeed = 10
		
	#generating spawners
	def generateSpawners(self, actualDifficulty):
		for z in range(0, actualDifficulty*2):
			enemies_file.createSpawner(actualDifficulty, self.mapWidth, self.mapHeight)
		
	#generating map
	def generateMap(self, actualDifficulty):
		self.mapWidth =  7 * self.chunkSize
		self.mapHeight = 7 * self.chunkSize
		
		self.mapImage = pygame.Surface((self.mapWidth, self.mapHeight))
		self.mapImage.fill((90, 175, 82))
		
		grass_image_0 = pygame.image.load("sprites/map_0/grass_0.png")
		grass_image_1 = pygame.image.load("sprites/map_0/grass_1.png")
		grass_image_2 = pygame.image.load("sprites/map_0/grass_2.png")
		
		randChunkType = 0
		
		for x in range(0, 7):
			for y in range(0, 7):
				if randChunkType == 0:
					self.mapImage.blit(grass_image_0, (x*self.chunkSize, y*self.chunkSize))
				elif randChunkType == 1:
					self.mapImage.blit(grass_image_1, (x*self.chunkSize, y*self.chunkSize))
				else:
					self.mapImage.blit(grass_image_2, (x*self.chunkSize, y*self.chunkSize))
					
				randChunkType = random.choice([0, 0, 1, 1, 2])
				
		self.generateSpawners(actualDifficulty)
	
	#reloading map
	def reloadMap(self):
		self.activeMap = self.mapImage.copy()
	
	#update
	def update(self, gw, playerRect):
		gw_rect = gw.get_rect()
		
		#camera_moving
		if playerRect.centerx > gw_rect.centerx + 25 - self.offsetX:
			self.offsetX -= self.scrollSpeed
		elif playerRect.centerx < gw_rect.centerx - 25 - self.offsetX:
			self.offsetX += self.scrollSpeed
			
		if playerRect.centery > gw_rect.centery + 25 - self.offsetY:
			self.offsetY -= self.scrollSpeed
		elif playerRect.centery < gw_rect.centery - 25 - self.offsetY:
			self.offsetY += self.scrollSpeed
		
		#camera_stops_on_map_border
		if self.offsetX > 0:
			self.offsetX = 0
		elif self.offsetX < gw_rect.width - self.mapWidth:
			self.offsetX = gw_rect.width - self.mapWidth
		
		if self.offsetY > 0:
			self.offsetY = 0
		elif self.offsetY < gw_rect.height - self.mapHeight:
			self.offsetY = gw_rect.height - self.mapHeight
			
		if playerRect.left < 0:
			playerRect.left = 0
		elif playerRect.right > self.mapWidth:
			playerRect.right = self.mapWidth
			
		if playerRect.top < 0:
			playerRect.top = 0
		elif playerRect.bottom > self.mapHeight:
			playerRect.bottom = self.mapHeight
		
		gw.blit(self.activeMap, (self.offsetX, self.offsetY))
