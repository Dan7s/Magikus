import pygame, random, math, enemies_file
pygame.init()

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightblue = (75, 147, 255)
purple = (119, 119, 238)
yellow = (230, 200, 0)
white = (255, 255, 255)
grey = (117, 117, 117)

resolutions = [
	(800, 600),
	(1000, 600),
	(1024, 768),
	(1280, 720),
	(1280, 768),
	(1280, 1024),
	(1366, 767),
	(1400, 1050),
	(1440, 900),
	(1680, 1050),
	(1600, 1200),
	(1920, 1080),
	(2048, 1080),
	(2048, 1536),
]

difficulty = {
	0 : "peacefull",
	1 : "easy",
	2 : "normal",
	3 : "hard",
	4 : "extreme",
}

#enemies spawn cd
spawnSlimeCDMax = 35

class HudBars():
	def __init__(self):
		self.barHeight = 20
		self.barWidth = 150
		self.healthBase = pygame.Surface((self.barWidth, self.barHeight))
		self.manaBase = pygame.Surface((self.barWidth, self.barHeight))
		self.expBase = pygame.Surface((self.barWidth, self.barHeight))
		
	def update(self, gw, health, healthMax, mana, manaMax, exp):
		healthText = pygame.font.Font(None, 25).render(str(health), 1, black)
		manaText = pygame.font.Font(None, 25).render(str(mana), 1, black)
		expText = pygame.font.Font(None, 25).render("Exp: ", 1, yellow)
		expValueText = pygame.font.Font(None, 25).render(str(exp), 1, yellow)
		
		healthBarWidth = int((health / healthMax) * self.barWidth)
		manaBarWidth = int((mana / manaMax) * self.barWidth)
		
		healthBar = pygame.Surface((healthBarWidth, self.barHeight))
		manaBar = pygame.Surface((manaBarWidth, self.barHeight))

		healthBar.fill(green)
		self.healthBase.fill(grey)
		self.healthBase.blit(healthBar, (0, 0))
		self.healthBase.blit(healthText, (healthBarWidth - healthText.get_rect().w - 3, self.barHeight/2 -  healthText.get_rect().h/2))
		
		manaBar.fill(lightblue)
		self.manaBase.fill(grey)
		self.manaBase.blit(manaBar, (0, 0))
		self.manaBase.blit(manaText, (manaBarWidth - manaText.get_rect().w - 3, self.barHeight/2 - manaText.get_rect().h/2))
		
		self.expBase.fill(grey)
		self.expBase.blit(expText, (5, self.barHeight/2 - expText.get_rect().h/2))
		self.expBase.blit(expValueText, ((self.barWidth/2 - expValueText.get_rect().w/2) + expText.get_rect().w/2, self.barHeight/2 - expText.get_rect().h/2))
		
		gw.blit(self.healthBase, (5, 5))
		gw.blit(self.manaBase, (5, 30))
		gw.blit(self.expBase, (5, 55))

class SpellIcon():
	def __init__(self, icon, pos, cd, manaCost, skillNum):
		self.icon = icon
		self.manaCost = manaCost
		self.cd = cd
		
		self.image = pygame.image.load(self.icon)
		self.rect = pos
		
		self.buttonText = pygame.font.Font(None, 20).render(str(skillNum), 1, white)
		
		self.manaCostText = pygame.font.Font(None, 20).render(str(self.manaCost), 1, blue)
		
		self.manaLack = pygame.font.Font(None, 90).render("x", 1, purple)
		self.manaLackRect = self.manaLack.get_rect()
	
	def draw(self, gw, playerMana):
		self.image = pygame.image.load(self.icon)
		if playerMana < self.manaCost:
			self.image.blit(self.manaLack,((self.image.get_rect().w/2 - self.manaLackRect.w/2), (self.image.get_rect().h/2 - self.manaLackRect.h/2)))
		elif self.cd <= 0:
			self.image.blit(self.buttonText, (0, 0))
			self.image.blit(self.manaCostText, (0, 27))
		elif self.cd > 0:
			self.cdText = pygame.font.Font(None, 50).render(str(self.cd), 1, red)
			self.cdTextRect = self.cdText.get_rect()
			self.image.blit(self.cdText,((self.image.get_rect().w/2 - self.cdTextRect.w/2), (self.image.get_rect().h/2 - self.cdTextRect.h/2)))
			
		gw.blit(self.image, self.rect)
	
	def update(self, gw, cd, playerMana):
		self.cd = cd
		self.draw(gw, playerMana)
		
class TextButton():
	def __init__(self, pos, size, color, text):
		self.rect = pygame.Rect(pos, size)
		self.hasClicked = False
		self.image = pygame.Surface(size)
		self.image.fill(color)
		self.color = color
		self.text = pygame.font.Font(None, size[1]).render(text, 1, red)
		self.textRect = self.text.get_rect()
		self.buttonCDmax = 2
		self.buttonCD = self.buttonCDmax
		
	def draw(self, gw):
		self.image.blit(self.text, ((self.rect.w - self.textRect.w)/2, (self.rect.h - self.textRect.h)/2))
		gw.blit(self.image, self.rect)
	
	def mouseover(self):
		cur = pygame.mouse.get_pos()
		if self.rect.left < cur[0] < self.rect.right and self.rect.top < cur[1] < self.rect.bottom:
			return True
		else:
			return False
		
	def isClicked(self):
		mouse = pygame.mouse.get_pressed()
		if self.mouseover():
			self.image.fill(purple)
			if mouse[0] == True and self.hasClicked == False and self.buttonCD <= 0:
				self.buttonCD = self.buttonCDmax
				self.hasClicked = True
				return True
			if mouse[0] == False and self.hasClicked == True:
				self.hasClicked = False
				return False
		else:
			self.image.fill(self.color)
		
	def update(self, gw):
		if self.buttonCD > 0:
			self.buttonCD -= 1
		self.draw(gw)
		
class SwitchButton():
	def __init__(self, pos, size, color, text):
		self.rect = pygame.Rect(pos, size)
		self.hasClicked = False
		self.image = pygame.Surface(size)
		self.image.fill(color)
		self.color = color
		self.size = size
		self.text = pygame.font.Font(None, size[1]).render(text, 1, red)
		self.textRect = self.text.get_rect()
		self.buttonCDmax = 2
		self.buttonCD = self.buttonCDmax
		
	def draw(self, gw):
		self.image.blit(self.text, ((self.rect.w - self.textRect.w)/2, (self.rect.h - self.textRect.h)/2))
		gw.blit(self.image, self.rect)
	
	def mouseover(self):
		cur = pygame.mouse.get_pos()
		if self.rect.left < cur[0] < self.rect.right and self.rect.top < cur[1] < self.rect.bottom:
			return True
		else:
			return False
		
	def isClicked(self):
		mouse = pygame.mouse.get_pressed()
		if self.mouseover():
			self.image.fill(purple)
			if mouse[0] == True and self.hasClicked == False and self.buttonCD <= 0:
				self.buttonCD = self.buttonCDmax
				self.hasClicked = True
				return True
			if mouse[0] == False and self.hasClicked == True:
				self.hasClicked = False
				return False
		else:
			self.image.fill(self.color)
		
	def update(self, gw, text):
		if self.buttonCD > 0:
			self.buttonCD -= 1
		self.text = pygame.font.Font(None, self.size[1]).render(text, 1, red)
		self.draw(gw)
