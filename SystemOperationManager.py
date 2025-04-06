from pathlib import Path,WindowsPath,PurePath
import os,sys,time,string,webbrowser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

DIRECTORY_PATH="C:/Users/"+os.getlogin()+"/Desktop/videogames"

class DirectoryManager():
    def __init__(self,directory_name:str):
        self.DIRNAME=directory_name
        self.executable_files=[]
        self.get_updated_game_list()
    def return_directories(self):
        dirs=[]
        for tuple in self.executable_files:
            dirs.append(tuple[1])
        return dirs
    def return_executable_files(self):
        executables=[]
        for tuple in self.executable_files:
            executables.append(tuple[0])
        return executables
    def return_executable_file_names(self):
        names=[]
        for tuple in self.executable_files:
            names.append(tuple[0].name.removesuffix('.exe'))
        return names
    def get_updated_game_list(self):
        self.executable_files.clear()
        subdirs=list(Path(self.DIRNAME).iterdir())
        for dir in subdirs:
            dir_path=Path(dir)
            if dir_path.is_dir():
                files=list(Path(dir).iterdir())
                for file in files:
                    if file.suffix=='.exe' and not 'UnityCrashHandler' in file.name:
                        self.executable_files.append([file,dir])
    def open_file_from_id(self,ID:int):
        if len(self.executable_files)>ID>=0:
            os.startfile(self.return_executable_files()[ID])
    def delete_dir_from_id(self,ID:int):
        if len(self.executable_files)>ID>=0:
            dir_to_delete=self.return_directories()[ID]
            for dir,subdirs,files in os.walk(dir_to_delete):
                for file in files:
                    os.remove(os.path.join(dir,file))
                    print('deleted file: ',os.path.join(dir,file))
            for dir,subdirs,files in os.walk(dir_to_delete,topdown=False):
                for subdir in subdirs:
                    os.rmdir(os.path.join(dir,subdir))
            os.rmdir(dir_to_delete)
            self.get_updated_game_list()
    def add_dir_to_path(self):
        self.get_updated_game_list()

def shutdown():
    os.system('shutdown /p /f')

def get_files_dir():
    script_path = __file__ if '__file__' in globals() else sys.argv[0]
    return os.path.dirname(os.path.realpath(script_path))

movie_page_link='https://streamingcommunity.paris'
opt=Options()
opt.add_argument(argument='--headless=new')

def open_movie_from_title(title:str):
    try:
        driver=webdriver.Chrome(options=opt)
        driver.get(movie_page_link)

        driver.find_element(By.CLASS_NAME,"search-button").click()
        search_bar=driver.find_element(By.XPATH,'//input[@type="text" @class="form-control"]')
        search_bar.send_keys(title)
        time.sleep(3)

        results=driver.find_elements(By.CLASS_NAME,'slider-item')
        first_result=results[0].find_element(By.XPATH,'.//*').get_attribute('href')
        movie_num_code=first_result[first_result.rfind('/')+1:first_result.find('-')]
        driver.quit()

        webbrowser.open(movie_page_link+'/watch/'+movie_num_code)
    except:
        pass