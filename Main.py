import pygame, random, math
from player import PlayerActive
import enemies_file
import utils
from utils import HudBars, SpellIcon, TextButton, SwitchButton, DragIcon, SlotImage
from map_file import mainMap
pygame.init()

class GAME():
	def __init__(self):
		#base_settings
		self.displayMode = 0
		self.resolutionMode = 1
		self.diplayModeSwitchText = ""
		self.resolutionSwitchText = ""
		self.gw = pygame.display.set_mode(self.setDisplayResolution(), self.setDisplayMode())
		self.map = mainMap()
		pygame.display.set_caption("Magikus - alpha 0.8.8")
		self.clock = pygame.time.Clock()
		#class_shourtcuts
		self.group_all_enemies = enemies_file.enemies_group_class.group_enemies
		self.group_all_spawners = enemies_file.spawners_group_class.group_spawners
		self.enemy_slime = enemies_file.Enemy_Slime
		self.player = PlayerActive()
		#settings
		self.actualDifficulty = 1
		self.spawnManaDelay = 0
		self.spawnManaDelayMax = 13
		self.FPS = 30
		#player_stats
		self.player.rect.x = self.gw.get_rect().centerx - self.player.rect.w/2
		self.player.rect.y = self.gw.get_rect().centery - self.player.rect.h/2
		self.player_mana_rest = False
		self.player_moving = False

	#hud_text
	def DisplayText(self, message, x, y, size, color):
		font = pygame.font.Font(None, size)
		text = font.render(message, 1, (color))
		self.gw.blit(text, (x, y))
		
	#seting display mode
	def setDisplayMode(self):
		if self.displayMode == 0:
			self.diplayModeSwitchText = "windowed"
			return 0
		elif self.displayMode == 1:
			self.diplayModeSwitchText = "noframe"
			return pygame.NOFRAME
		elif self.displayMode == 2:
			self.diplayModeSwitchText = "fullscreen"
			return pygame.FULLSCREEN
	
	#setting resolution
	def setDisplayResolution(self):
		text = str(utils.resolutions[self.resolutionMode])
		text = text.replace(")", "")
		text = text.replace("(", "")
		text = text.replace(",", " x")
		self.resolutionSwitchText = text
		return utils.resolutions[self.resolutionMode]

	#start_screen
	def menu(self):
		menu = True
		self.gw.fill(utils.black)
		#Text and Buttons
		self.DisplayText('made by Dan7s', self.gw.get_rect().left + 10, self.gw.get_rect().top + 10, 25, utils.white)
		self.DisplayText('beta 0.8.8', self.gw.get_rect().right - 90, self.gw.get_rect().top + 10, 25, utils.white)
		self.DisplayText('Magikus', self.gw.get_rect().centerx - 160, self.gw.get_rect().centery - 205, 120, utils.red)
		self.DisplayText('Magikus', self.gw.get_rect().centerx - 165, self.gw.get_rect().centery - 195, 120, utils.blue)
		start_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery - 50), (200, 50), utils.blue, "Start Game")
		load_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 30), (200, 50), utils.blue, "Load Game")
		options_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 110), (200, 50), utils.blue, "Options")
		exit_button = TextButton((self.gw.get_rect().centerx - 100 , self.gw.get_rect().centery + 190), (200, 50), utils.blue, "Exit Game")
		while menu:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				
			#Buttons
			if start_button.isClicked():
				self.map.generateMap(self.actualDifficulty)
				self.playGame()
			if options_button.isClicked():
				self.options("inMenu")
			if load_button.isClicked():
				pass
			if exit_button.isClicked():
				pygame.quit()
				quit()
				
			#Updates
			pygame.display.update()
			start_button.update(self.gw)
			load_button.update(self.gw)
			options_button.update(self.gw)
			exit_button.update(self.gw)
			self.clock.tick(self.FPS)

	#gameover
	def gameover(self):
		gameover = True
		self.gw.fill(utils.black)
		gained_exp_text = pygame.font.Font(None, 25).render("Gained experience points: " + str(self.player.exp), 1, utils.yellow)
		gained_exp_rect = gained_exp_text.get_rect()
		#Text and Buttons
		self.DisplayText("YOU DIED", self.gw.get_rect().centerx - 130, self.gw.get_rect().centery - 125, 82, utils.red)
		self.DisplayText("Gained experience points: " + str(self.player.exp), self.gw.get_rect().centerx - gained_exp_rect.w/2, self.gw.get_rect().centery - 65, 25, utils.yellow)
		restart_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery - 25), (200, 50), utils.blue, "Restart")
		load_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 50), (200, 50), utils.blue, "Load Game")
		exit_button = TextButton((self.gw.get_rect().centerx - 100 , self.gw.get_rect().centery + 125), (200, 50), utils.blue, "Exit Game")

		#Gameover loop
		while gameover:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

			#Buttons
			if restart_button.isClicked():
				self.restartGame()
			if load_button.isClicked():
				pass
			if exit_button.isClicked():
				pygame.quit()
				quit()

			#Updates
			restart_button.update(self.gw)
			load_button.update(self.gw)
			exit_button.update(self.gw)
			pygame.display.update()
			
			self.clock.tick(self.FPS)

	#restart game
	def restartGame(self):
		self.gw.fill(utils.black)
		for enemy in self.group_all_enemies:
			enemy.destroy()
		for spawner in self.group_all_spawners:
			spawner.destroy()
		self.player.health = self.player.healthMax
		self.player.bullets.empty()
		self.player.exp = 0
		self.player.mana.empty()
		self.player.rect.x = self.gw.get_rect().centerx - self.player.rect.w/2
		self.player.rect.y = self.gw.get_rect().centery - self.player.rect.h/2
		self.player.isAlive = True
		self.map.generateMap(self.actualDifficulty)
		self.playGame()
		
	#skill options (slots etc.)
	def skillsOptions(self):
		skillsOptions = True
		icon_options_group = []
		slot_active_group = []
		slot_disable_group = []
		counter = 1
		self.gw.fill(utils.black)
		
		#text and buttons
		back_button = TextButton((self.gw.get_rect().centerx - 350, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Back")
		defaults_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Reset")
		set_button = TextButton((self.gw.get_rect().centerx + 150, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Set")
	
		#active bar slots
		for slot in utils.skillSlot:
			slot = SlotImage("sprites/icons/slot_1.png", (self.gw.get_rect().left + (self.gw.get_rect().width/(len(utils.skillSlot)+1)*counter)-30, self.gw.get_rect().centery -100))
			slot.spell_inside = utils.skillSlot.get(counter)
			slot_active_group.insert(counter-1, slot)
			counter += 1
		
		#unactive slots
		counter = 1
		for spell in self.player.spells:
			slot = SlotImage("sprites/icons/slot_2.png",  (self.gw.get_rect().left + (self.gw.get_rect().width/(len(self.player.spells)+1)*counter)-30, self.gw.get_rect().centery + 80))
			slot.spell_inside = spell
			slot_disable_group.insert(counter-1, slot)
			counter += 1
		
		#skill icons
		counter = 1
		for spell in self.player.spells:
			for slot in slot_disable_group:
				if slot.spell_inside == spell:
					icon_x, icon_y = slot.rect.x+10, slot.rect.y+10
					break
			for slot in slot_active_group:
				if slot.spell_inside == spell:
					icon_x, icon_y = slot.rect.x+10, slot.rect.y+10
					break
			icon = DragIcon(spell, "sprites/icons/" + spell + "_icon.png", (icon_x, icon_y))
			icon_options_group.insert(counter-1, icon)
			counter += 1
			
		#skill options loop
		while skillsOptions:
			self.gw.fill(utils.black)
			self.DisplayText('Skills', self.gw.get_rect().centerx - 80, self.gw.get_rect().centery - 280, 82, utils.red)
			
			for icon in icon_options_group:
				self.DisplayText(str(icon.spell_name), icon.rect.x, icon.rect.y + 60, 28, utils.white)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.pause()
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						for icon in icon_options_group:
							if icon.rect.collidepoint(event.pos):
								icon.draging = True
								icon.oldPos = (icon.rect.x, icon.rect.y)
								if icon.rect.collidelist(slot_active_group) >= 0:
									icon.oldSlot = icon.rect.collidelist(slot_active_group)
								else:
									icon.oldSlot = icon.rect.collidelist(slot_disable_group)
								mouse_x, mouse_y = event.pos
								offset_x = icon.rect.x - mouse_x
								offset_y = icon.rect.y - mouse_y
								
				elif event.type == pygame.MOUSEBUTTONUP:
					for icon in icon_options_group:
						if icon.draging:
							icon.draging = False
							if icon.rect.collidelist(slot_active_group) >= 0:
								utils.skillSlot[icon.oldSlot+1] = 0
								choosen_slot = slot_active_group[icon.rect.collidelist(slot_active_group)]
								icon.rect.x, icon.rect.y = choosen_slot.rect.x+10, choosen_slot.rect.y+10
								utils.skillSlot[icon.rect.collidelist(slot_active_group)+1] = icon.spell_name
							elif icon.rect.collidelist(slot_disable_group) >= 0:
								utils.skillSlot[icon.oldSlot+1] = 0
								choosen_slot = slot_disable_group[icon.rect.collidelist(slot_disable_group)]
								icon.rect.x, icon.rect.y = choosen_slot.rect.x+10, choosen_slot.rect.y+10
							else:
								icon.rect.x, icon.rect.y = icon.oldPos[0], icon.oldPos[1]
								
				elif event.type == pygame.MOUSEMOTION:
					for icon in icon_options_group:
						if icon.draging:
							mouse_x, mouse_y = event.pos
							icon.rect.x = mouse_x + offset_x
							icon.rect.y = mouse_y + offset_y
								
			#buttons
			if back_button.isClicked():
				self.pause()
			if defaults_button.isClicked():
				pass
			if set_button.isClicked():
				pass
				
			#Updates
			back_button.update(self.gw)
			defaults_button.update(self.gw)
			set_button.update(self.gw)
			for slot in slot_active_group:
				slot.update(self.gw)
			for slot in slot_disable_group:
				slot.update(self.gw)
			for icon in icon_options_group:
				icon.update(self.gw)
			pygame.display.update()
			self.clock.tick(self.FPS)
	
	#options
	def options(self, options_type):
		options = True
		self.gw.fill(utils.black)
		#text and Buttons
		self.DisplayText('Options', self.gw.get_rect().centerx - 110, self.gw.get_rect().centery - 280, 82, utils.red)
		difficulty_switch = SwitchButton((self.gw.get_rect().centerx - 210, self.gw.get_rect().centery - 180), (420, 50), utils.blue, "Difficulty: " + str(utils.difficulty[self.actualDifficulty]))
		display_mode_switch = SwitchButton((self.gw.get_rect().centerx - 210, self.gw.get_rect().centery - 100), (420, 50), utils.blue, "Display: " + self.diplayModeSwitchText)
		resolution_mode_switch = SwitchButton((self.gw.get_rect().centerx - 210, self.gw.get_rect().centery - 20), (420, 50), utils.blue, "Resolution: " + self.resolutionSwitchText)
		back_button = TextButton((self.gw.get_rect().centerx - 350, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Back")
		defaults_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Reset")
		set_button = TextButton((self.gw.get_rect().centerx + 150, self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Set")
		
		#options loop
		while options:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					if options_type == "inGame":
						self.pause()
					elif options_type == "inMenu":
						self.menu()
					
			#Buttons
			if difficulty_switch.isClicked():
				if self.actualDifficulty < len(utils.difficulty)-1:
					self.actualDifficulty += 1
				else:
					self.actualDifficulty = 0
				if options_type == "inGame":
					self.map.generateSpawners(self.actualDifficulty)
			if display_mode_switch.isClicked():
				if self.displayMode < 2:
					self.displayMode += 1
				else:
					self.displayMode = 0
				self.setDisplayMode()
			if resolution_mode_switch.isClicked():
				if self.resolutionMode < len(utils.resolutions)-1:
					self.resolutionMode += 1
				else:
					self.resolutionMode = 0
				self.setDisplayResolution()
			if back_button.isClicked():
				if options_type == "inGame":
					self.pause()
				elif options_type == "inMenu":
					self.menu()
			if defaults_button.isClicked():
				self.actualDifficulty = 1
				self.displayMode = 0
				self.resolutionMode = 1
				self.setDisplayResolution()
				self.setDisplayMode()
				self.options(options_type)
			if set_button.isClicked():
				pygame.display.set_mode(self.setDisplayResolution(), self.setDisplayMode())
				self.options(options_type)
			
			#Updates
			difficulty_switch.update(self.gw, "Difficulty: " + str(utils.difficulty[self.actualDifficulty]))
			display_mode_switch.update(self.gw, "Display: " + self.diplayModeSwitchText)
			resolution_mode_switch.update(self.gw, "Resolution: " + self.resolutionSwitchText)
			back_button.update(self.gw)
			defaults_button.update(self.gw)
			set_button.update(self.gw)
			pygame.display.update()
			self.clock.tick(self.FPS)
		
	#pause
	def pause(self):
		pause = True
		self.gw.fill(utils.black)
		#Text and Buttons
		self.DisplayText('Game Paused', self.gw.get_rect().centerx - 200, self.gw.get_rect().centery - 280, 82, utils.red)
		resume_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery - 180), (200, 50), utils.blue, "Resume")
		restart_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery - 100), (200, 50), utils.blue, "Restart")
		skill_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery - 20), (200, 50), utils.blue, "Skills")
		load_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 60), (200, 50), utils.blue, "Load Game")
		options_button = TextButton((self.gw.get_rect().centerx - 100, self.gw.get_rect().centery + 140), (200, 50), utils.blue, "Options")
		exit_button = TextButton((self.gw.get_rect().centerx - 100 , self.gw.get_rect().centery + 220), (200, 50), utils.blue, "Exit Game")

		#Pause Loop
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pause = False
					self.playGame()

			#Buttons
			if resume_button.isClicked():
				pause = False
				self.playGame()
			if restart_button.isClicked():
				self.restartGame()
			if skill_button.isClicked():
				self.skillsOptions()
			if load_button.isClicked():
				pass
			if options_button.isClicked():
				self.options("inGame")
			if exit_button.isClicked():
				pygame.quit()
				quit()

			#Updates
			resume_button.update(self.gw)
			restart_button.update(self.gw)
			skill_button.update(self.gw)
			load_button.update(self.gw)
			options_button.update(self.gw)
			exit_button.update(self.gw)
			pygame.display.update()
			self.clock.tick(self.FPS)

	#game
	def playGame(self):
		Game_Running = True
		#hud preapare
		hud_bars = HudBars()
		icon_group = []
		
		#skills
		for slot in utils.skillSlot:
			if utils.skillSlot.get(slot) != 0:
				icon = SpellIcon("sprites/icons/" + str(utils.skillSlot.get(slot)) + "_icon.png", self.gw, utils.cdMax.get(utils.skillSlot.get(slot)), utils.cost.get(utils.skillSlot.get(slot)), slot)
				icon_group.insert(slot, icon)
			
		#game loop
		while Game_Running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					self.pause()

			#Player_controll
			activeKey = pygame.key.get_pressed()
			cur = pygame.mouse.get_pos()
			cur = (cur[0] - self.map.offsetX, cur[1] - self.map.offsetY)
			mouse = pygame.mouse.get_pressed()

			if activeKey[pygame.K_d] or activeKey[pygame.K_a] or activeKey[pygame.K_w] or activeKey[pygame.K_s]:
				self.player_moving = True
				self.spawnManaDelayMax = 15
			else:
				self.player_moving = False
				self.spawnManaDelayMax = 40

			if activeKey[pygame.K_d]:
				self.player.move(1, 0)

			if activeKey[pygame.K_a]:
				self.player.move(-1, 0)

			if activeKey[pygame.K_w]:
				self.player.move(0, -1)

			if activeKey[pygame.K_s]:
				self.player.move(0, 1)

			if activeKey[pygame.K_1]:
				self.player.spells.get(utils.skillSlot.get(1))(cur)
				
			if activeKey[pygame.K_2]:
				self.player.spells.get(utils.skillSlot.get(2))(cur)
			
			if activeKey[pygame.K_3]:
				self.player.spells.get(utils.skillSlot.get(3))(cur)
				
			if activeKey[pygame.K_4]:
				self.player.spells.get(utils.skillSlot.get(4))(cur)
				
			if activeKey[pygame.K_5]:
				self.player.spells.get(utils.skillSlot.get(5))(cur)

			if activeKey[pygame.K_6]:
				self.player.spells.get(utils.skillSlot.get(6))(cur)
				
			if activeKey[pygame.K_7]:
				self.player.spells.get(utils.skillSlot.get(7))(cur)
				
			if activeKey[pygame.K_8]:
				self.player.spells.get(utils.skillSlot.get(8))(cur)
				
			if activeKey[pygame.K_9]:
				self.player.spells.get(utils.skillSlot.get(9))(cur)
		

			#window_fill
			self.gw.fill(utils.black)
			self.map.reloadMap()


			#player_shooting_and_mana_recorvering
			if mouse[0]:
				self.player.shoot(cur)
				
			if len(self.player.mana) < self.player.manaMax:
				self.spawnManaDelay -= 1
				if self.spawnManaDelay <= 0:
					self.player.spawnMana()
					self.spawnManaDelay = self.spawnManaDelayMax

			self.player.moveMana()


			#collisions
			PlayerCollisions = pygame.sprite.spritecollide(self.player, self.group_all_enemies, False)
			for enemy in PlayerCollisions:
				self.player.takeDemage()
				enemy.destroy()

			BulletCollisions = pygame.sprite.groupcollide(self.group_all_enemies, self.player.bullets, False, True)
			for enemy in BulletCollisions:
				if enemy.takeDemage() == True:
					self.player.addExp(1*self.actualDifficulty)
			
			#game_over
			print(self.clock, len(self.group_all_spawners), len(self.group_all_enemies), end='\r')
			if self.player.health <= 0:
				self.gameover()
			
			#updates
			self.group_all_spawners.update(self.actualDifficulty)
			self.group_all_spawners.draw(self.map.activeMap)
			self.player.update(cur, self.map.activeMap, self.map.mapWidth, self.map.mapHeight)
			self.group_all_enemies.update(self.player)
			self.group_all_enemies.draw(self.map.activeMap)
			
			
			#hud_and_map
			self.map.update(self.gw, self.player.rect)
			for icon in icon_group:
				icon.update(self.gw, utils.cd.get(utils.skillSlot.get(icon.skillNum)), len(self.player.mana))
			hud_bars.update(self.gw, self.player.health, self.player.healthMax, len(self.player.mana), self.player.manaMax, self.player.exp)
			
			
			#end
			pygame.display.update()
			self.clock.tick(self.FPS)
			
		pygame.quit()
		quit()

#starting
GAME().menu()
