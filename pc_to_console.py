import SystemOperationManager as system
import pygame,time,random
pygame.init()
pygame.joystick.init()

game_list=system.DirectoryManager(system.DIRECTORY_PATH)

W,H=800,450
display=pygame.display.set_mode((W,H),pygame.SCALED+pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

class Particle():
    def __init__(self,pos,force,duration):
        self.x=pos[0]
        self.y=pos[1]
        self.forcex=force[0]
        self.forcey=force[1]
        self.duration=random.randint(0,duration)        
    def update(self,color=(255,255,255),speed=1,alpha=50):
        self.x+=self.forcex
        self.y+=self.forcey
        self.duration-=speed*0.1
        #"light" effect
        radius=self.duration*2
        surface=pygame.Surface((radius*2,radius*2))
        surface.set_colorkey((0,0,0))
        surface.set_alpha(alpha)
        pygame.draw.circle(surface,color,(radius,radius),radius)
        display.blit(surface,(self.x-radius,self.y-radius))#,special_flags=BLEND_RGB_ADD)
        #draw particle
        pygame.draw.circle(display,color,(self.x,self.y),int(self.duration))
    def ended(self):
        if self.duration<=0: return True
        else: return False

def get_text(text,color=(255,255,255),size=32):
    font=pygame.font.Font(system.get_files_dir()+'/m3x6.ttf',size)
    img_text=font.render(text,False,color)
    return img_text


movie_title=''
selected_menu_option=0
particles=[]
game_list_surface=pygame.Surface((500,200))
game_list_surface.set_colorkey((0,0,0))
while True:
    display.fill((0,0,0))
    particles.append(Particle((0,random.randint(0,H)),(1,random.uniform(-1,1)),10))
    particles.append(Particle((W,random.randint(0,H)),(-1,random.uniform(-1,1)),10))
    particles.append(Particle((random.randint(0,W),0),(random.uniform(-1,1),1),10))
    particles.append(Particle((random.randint(0,W),H),(random.uniform(-1,1),-1),10))
    for particle in particles:
        particle.update(color=(200,200,200),speed=0.5)
        if particle.ended():
            particles.remove(particle)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()            

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_DOWN:
                selected_menu_option+=1
            if event.key==pygame.K_UP:
                selected_menu_option-=1
            if event.key==pygame.K_RETURN:
                pygame.draw.rect(display,(255,255,255),[0,H/2-50,W,100])
                display.blit(get_text('LOADING...',color=(0,0,0),size=64),(100,H/2-30))
                pygame.display.update()
                if movie_title!='':
                    system.open_movie_from_title(movie_title)
                else:
                    game_list.open_file_from_id(selected_menu_option)
                time.sleep(7)
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
            if event.key==pygame.K_F4:
                system.shutdown()
            if event.key==pygame.K_BACKSPACE:
                movie_title=movie_title[0:len(movie_title)-1]
            if event.key==pygame.K_TAB:
                movie_title=''
        if event.type==pygame.TEXTINPUT:
            movie_title+=event.text

    
    if int(selected_menu_option)>=len(game_list.return_executable_file_names()):
        selected_menu_option=0
    elif int(selected_menu_option)<0:
        selected_menu_option=len(game_list.return_executable_file_names())-1


    display.blit(get_text('SELECT VIDEOGAME:'),(480,100))
    game_list_surface.fill((0,0,0,0))
    for index,name in enumerate(game_list.return_executable_file_names()):
        text=get_text(str(index+1)+' - '+name)
        pos=[0,text.get_height()*index]
        if index==int(selected_menu_option):
            pos[0]=30
        if selected_menu_option>=5:
            pos[1]=text.get_height()*index-(selected_menu_option-5)*text.get_height()
        game_list_surface.blit(text,pos)
    display.blit(game_list_surface,(480,150))
        
    display.blit(get_text('DIGIT MOVIE TITLE:'),(100,100))
    r=get_text(movie_title,size=40)
    pygame.draw.rect(display,(255,255,255),[100,150,r.get_width()+20,r.get_height()],5)
    display.blit(r,(110,150))
    
    pygame.display.update()
    clock.tick(60)