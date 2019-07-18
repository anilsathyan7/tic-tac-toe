import pygame
import numpy as np 
import time
import sys
import random

pygame.mixer.init() 
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((610, 610))
surface.fill((255, 255, 255))
done = False
color = (0, 0, 0)
width, height = 200, 200
thickness = 10
sound = None

font_size=40


font2 = pygame.font.SysFont('comicsansms', 80)
one_won = font2.render('Player one won !!!', True, (0, 0, 0))
two_won = font2.render('Player two won !!!', True, (0, 0, 0))
match_drawn = font2.render('Match drawn !!!', True, (0, 0, 0))



# Image Library
_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get('images/'+path)
        if image == None:
                image = pygame.image.load('images/'+path)
                _image_library[path] = image
        return image

# Sound Library
_sound_library = {}
def play_sound(path):
  global _sound_library, sound
  sound = _sound_library.get('audios/'+path)
  if sound == None:
    
    sound = pygame.mixer.Sound('audios/'+path)
    _sound_library[path] = sound  
  sound.play()


# Splash screen
play_sound('splash_intro.wav')


while font_size<90:

 font = pygame.font.Font('fonts/crackman.ttf', font_size)
 text = font.render('Tic Tac Toe', True, (0, 0, 0))
 surface.blit(text, (305 - text.get_width() // 2, 305 - text.get_height() // 2))
 pygame.display.update()
 pygame.time.wait(100)
 font_size=font_size+5
 if font_size==90:
         pygame.time.wait(1500)
 surface.fill(pygame.Color("white"),(10,10,590,590))

#Draw grid 
grid = []

def draw_grid():
    global grid
    
    pygame.draw.rect(surface, (0,0,0), pygame.Rect(0, 0, 610, 610), 15)    
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(5, 5, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(205, 5, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(405, 5, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(5, 205, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(205, 205, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(405, 205, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(5, 405, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(205, 405, width, height), thickness))
    grid.append(pygame.draw.rect(surface, color, pygame.Rect(405, 405, width, height), thickness))

# Draw grid and borders
pygame.draw.rect(surface, (0,0,0), pygame.Rect(0, 0, 610, 610), 15)
draw_grid()

#Store states
entries= np.array([None]*9)

# Player turn
Turn = True

def reset():

  global grid, entries, Turn, surface, done, font2
  
  grid = []
  surface.fill((255, 255, 255))
  
  entries = np.array([None]*9)
  Turn = True
  done= False
  pos=35

  font3 = pygame.font.Font('fonts/gomarice_no_continue.ttf', 70)
  font4 = pygame.font.SysFont('timesnewroman', 30)
  colors = [(148,0,211), (75,0,130), (0,0,255), (0,255,0), (255,255,0), (255,127,0), (255,0,0)]
  col = random.choice(colors)
  COLORCYCLE = pygame.USEREVENT + 1
  pygame.time.set_timer(COLORCYCLE, 500)

  ANIMATECYCLE = pygame.USEREVENT + 2
  pygame.time.set_timer(ANIMATECYCLE, 30)
  
  replay = font3.render('PLAY AGAIN ?', True, col)
  yes_no = font4.render('YES [Y]  NO [N]', True, (0,0,0))

  
  play_sound('replay.wav')
  check=False
  while not check:
    for event in pygame.event.get():
        
        if(event.type == COLORCYCLE):
           # change color
           col1 = random.choice(colors)
           replay = font3.render('PLAY AGAIN?', True, col1)
           
        if(event.type == ANIMATECYCLE):
                if pos < 305:
                   pos = pos + 5

        surface.fill((255, 255, 255))
        pygame.draw.rect(surface, (0,0,0), pygame.Rect(0, 0, 610, 610), 15)
        surface.blit(replay, (305 - replay.get_width() // 2, pos - replay.get_height() // 2))
        surface.blit(yes_no, (305 - yes_no.get_width() // 2, (690 - pos) - replay.get_height() // 2))
        pygame.display.update()
       
               
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                check=True
                surface.fill((255, 255, 255))
                sound.stop()
                play_sound('re_enter.wav')
                draw_grid()
                return 0                
            elif event.key == pygame.K_n:
                check=True
  # Exit game
  sound.stop()
  pygame.display.update()
  s = pygame.Surface((610,610))
  s.fill((0,0,0))
  count=0
  play_sound('exit.wav')
  while count<150:

    s.set_alpha(count)                         
    surface.blit(s, (0,0))
    pygame.display.update()
    pygame.time.wait(10)
    count=count+2

  pygame.quit()
  sys.exit()             
  

def finish():
   global surface
   surface.fill((255, 255, 255))

def put_xy(value, img_pos, grid_pos):
  if value == 0 :
    play_sound('circle.wav')
    surface.blit(get_image('o.png'), img_pos)
    entries[grid_pos]=0
  else:
    play_sound('cross.wav') 
    surface.blit(get_image('x.png'), img_pos)
    entries[grid_pos]=1

def check_win():
    global surface, one_won, two_won, match_drawn
    mat = np.reshape(entries,(3,3))
    
    
    for i in range(0,3):
      if (mat[i][0] == mat [i][1] == mat [i][2]):
         if mat[i][0] == 0:
            pygame.draw.line(surface, (0,0,0), grid[i*3].midleft, grid[(i*3) + 2].midright, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player one won !!!"
            surface.fill((255, 255, 255))
            surface.blit(one_won, (305 - one_won.get_width() // 2, 305 - one_won.get_height() // 2))
            return 1
         elif mat[i][0] == 1:
            pygame.draw.line(surface, (0,0,0), grid[i*3].midleft, grid[(i*3) + 2].midright, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player two won !!!"
            surface.fill((255, 255, 255))
            surface.blit(two_won, (305 - two_won.get_width() // 2, 305 - two_won.get_height() // 2))
            return 1

    for j in range(0,3):
      if (mat[0][j] == mat [1][j] == mat [2][j]):
         if mat[0][j] == 0:
            pygame.draw.line(surface, (0,0,0), grid[j].midtop, grid[(j + 6)].midbottom, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player one won !!!"
            surface.fill((255, 255, 255))
            surface.blit(one_won, (305 - one_won.get_width() // 2, 305 - one_won.get_height() // 2))
            return 1
         elif mat[0][j] == 1:
            pygame.draw.line(surface, (0,0,0), grid[j].midtop, grid[(j + 6)].midbottom, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player two won !!!"
            surface.fill((255, 255, 255))
            surface.blit(two_won, (305 - two_won.get_width() // 2, 305 - two_won.get_height() // 2))
            return 1
    
    if(mat[0][0] == mat[1][1] == mat[2][2]):
         if mat[0][0] == 0:
            pygame.draw.line(surface, (0,0,0), grid[0].topleft, grid[8].bottomright, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player one won !!!"
            surface.fill((255, 255, 255))
            surface.blit(one_won, (305 - one_won.get_width() // 2, 305 - one_won.get_height() // 2))
            return 1
            
         elif mat[0][0] == 1:
            pygame.draw.line(surface, (0,0,0), grid[0].topleft, grid[8].bottomright, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player two won !!!"
            surface.fill((255, 255, 255))
            surface.blit(two_won, (305 - two_won.get_width() // 2, 305 - two_won.get_height() // 2))
            return 1
    
    if(mat[0][2] == mat[1][1] == mat[2][0]):
         if mat[0][2] == 0:
            pygame.draw.line(surface, (0,0,0), grid[2].topright, grid[6].bottomleft, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player one won !!!"
            surface.fill((255, 255, 255))
            surface.blit(one_won, (305 - one_won.get_width() // 2, 305 - one_won.get_height() // 2))
            return 1
         elif mat[0][2] == 1:
            pygame.draw.line(surface, (0,0,0), grid[2].topright, grid[6].bottomleft, 20)
            pygame.display.update()
            pygame.time.wait(1000)
            print "Player two won !!!"
            surface.fill((255, 255, 255))
            surface.blit(two_won, (305 - two_won.get_width() // 2, 305 - two_won.get_height() // 2))
            return 1
    if (not any( x is None for x in entries)):
            pygame.display.update()
            pygame.time.wait(1000)
            print "Match drawn !!!"
            surface.fill((255, 255, 255))
            surface.blit(match_drawn, (305 - match_drawn.get_width() // 2, 305 - match_drawn.get_height() // 2))
            return 2 
    return 0



while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect in grid:
                       if rect.collidepoint(event.pos) and entries[grid.index(rect)] == None :
                          if Turn:
                             put_xy(0,(rect.x + 25, rect.y + 25), grid.index(rect))   
                          else:
                             put_xy(1,(rect.x + 25, rect.y + 25), grid.index(rect))  
                          Turn = not Turn
                    status=check_win()
                    if(status!=0):
                       pygame.draw.rect(surface, (0,0,0), pygame.Rect(0, 0, 610, 610), 15)
                       pygame.display.update()
                       pygame.event.clear()
                       if status == 1:
                          play_sound('win.wav')
                       else:
                          play_sound('draw.wav')
                       pygame.time.wait(3000)
                       done = True
                       
                       reset()
                       
                          
                
        pygame.display.flip()
        clock.tick(60)
