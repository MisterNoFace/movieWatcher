import pygame,random
pygame.init()
pygame.joystick.init()
pygame.font.init()
pygame.mouse.set_visible(False)
import os,webbrowser,threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

W,H=800,450
display=pygame.display.set_mode((W,H),pygame.SCALED+pygame.FULLSCREEN)
clock = pygame.time.Clock()
movie_title=''
selected_menu_option=0
particles=[]
is_searching=False

opt=Options()
opt.add_argument(argument='--headless=new')

def open_from_streamingCommunity(title:str):
    global movie_title,is_searching
    driver=webdriver.Chrome(options=opt)
    try:
        movie_page_link='https://streamingcommunity.to'
        driver.get(movie_page_link)
        #driver.find_element(By.ID,"details-button").click()
        #driver.find_element(By.ID,"proceed-link").click()
        driver.find_element(By.CLASS_NAME,"search-button").click()
        driver.find_element(By.XPATH,'//input[@type="text" @class="form-control"]').send_keys(title) #search bar
        driver.implicitly_wait(1)

        results=driver.find_elements(By.CLASS_NAME,'slider-item')
        first_result=results[0].find_element(By.XPATH,'.//*').get_attribute('href')
        movie_num_code=first_result[first_result.rfind('/')+1:first_result.find('-')]     
        if is_searching: webbrowser.open(movie_page_link+'/watch/'+movie_num_code)
        #return movie_page_link+'/watch/'+movie_num_code
    except:
        pass
    is_searching=False
    driver.quit()

"""def open_from_Xprime(title:str):
    global is_searching
    try:
        driver=webdriver.Chrome(options=opt)
        driver.get('https://xprime.tv')
        #driver.find_element(By.ID,"details-button").click()
        #driver.find_element(By.ID,"proceed-link").click()
        driver.find_element(By.CLASS_NAME,"search-button svelte-yrzwyi").click()
        driver.implicitly_wait(2)
        search_bar=driver.find_element(By.CLASS_NAME,'search-input svelte-yrzwyi visible').send_keys(title)


        driver.find_elements(By.CLASS_NAME,'result-item svelte-kdpa49')[0].click()
        driver.implicitly_wait(0.5)
        driver.find_element(By.CLASS_NAME,'play-button color-primary hasLabel hasIcon ltr-kjpk1q svelte-vuiiet').click()
        driver.implicitly_wait(0.5)
        
        webbrowser.open(driver.current_url)
        driver.quit()
        return driver.current_url

    except:
        return None
    is_searching=False"""

def open_from_Hexa():
    global movie_title,is_searching
    driver=webdriver.Chrome(options=opt)
    try:
        driver.get('https://hexa.watch/search')
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH,'//input[@type="text"]').send_keys(movie_title) #search bar

        link=driver.find_elements(By.XPATH,'//a[@class="block w-full h-full"]')[0].get_attribute('href')
        driver.get(link)
        driver.implicitly_wait(0.5)
        if is_searching: webbrowser.open(driver.current_url.replace('details','watch'))
        #return driver.current_url.replace('details','watch')
    except:
        pass
    is_searching=False
    driver.quit()

        

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
    try:
        font=pygame.font.Font('m3x6.ttf',size)
    except:
        font=pygame.font.Font(pygame.font.get_default_font(),size)
    img_text=font.render(text,False,color)
    return img_text


def main():
    global movie_title,selected_menu_option,is_searching
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
                    if movie_title!='' and not is_searching:
                        threading.Thread(target=open_from_streamingCommunity).start()
                        threading.Thread(target=open_from_Hexa).start()
                        is_searching=True
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                if event.key==pygame.K_F4:
                    os.system('shutdown /p /f')
                if event.key==pygame.K_BACKSPACE:
                    movie_title=movie_title[0:len(movie_title)-1]
                if event.key==pygame.K_TAB:
                    movie_title=''
            if event.type==pygame.TEXTINPUT:
                movie_title+=event.text

               
        t=get_text('DIGIT MOVIE or TV SERIES TITLE:',size=50)
        display.blit(t,(W/2-t.get_width()/2,150))
        t=get_text(movie_title,size=80)
        pygame.draw.rect(display,(255,255,255),[W/2-t.get_width()/2-10,200,t.get_width()+20,t.get_height()+10],width=5)
        display.blit(t,(W/2-t.get_width()/2,200))
        if is_searching:
            t=get_text('Searching...',size=80,color=(0,0,0))
            pygame.draw.rect(display,(255,255,255),[W/2-t.get_width()/2-10,H/2-t.get_height()/2,t.get_width(),t.get_height()],border_radius=10)
            display.blit(t,(W/2-t.get_width()/2,H/2-t.get_height()/2))
        pygame.display.update()
        clock.tick(60)
main()