import undetected_chromedriver as uc
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import os
import sys
options = uc.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument("--ignore-certificate-errors")
options.add_argument("--window-size=1920,1080")
os.system('clear')
print('You can press ctrl+c at any time to exit the script')
try:
    file_name = input('Enter HTML file name: ')
    username = input('Enter your gmail username: ') 
    password = input('Enter your gmail password: ') 
    number_of_random_posts = input('Enter number of posts you want: ')
    while number_of_random_posts.isnumeric() != True or int(number_of_random_posts)<=0:
        number_of_random_posts = input('Please enter a positive whole number: ')
    number_of_random_posts = int(number_of_random_posts)    
    minimum_number_of_likes = input('Enter minimun number of likes: ')
    while minimum_number_of_likes.isnumeric() != True or int(minimum_number_of_likes)<=0: 
        minimum_number_of_likes = input('Please enter a positive whole number: ')
    minimum_number_of_likes = int(minimum_number_of_likes)
except KeyboardInterrupt:
    print('')
    print('Exited...')
    sys.exit(1)    
    



driver = uc.Chrome(options=options)
os.system('clear')
print('Script is starting please wait')
posts_data=[]
all_links=[]
def main():
    config('https://www.pinterest.com/')
    signIn()
    
    getData()
    suppress_exception_in_del(uc)
    
   
def config(url):
    driver.get(url)
    driver.implicitly_wait(5)
    driver.maximize_window()
    
def signIn():
    print('Logging you in')
    
    original_window = driver.current_window_handle
    driver.find_element(By.CSS_SELECTOR,('div[data-test-id="simple-login-button"] button')).click()
    
    
    
    iframe = driver.find_element(By.CSS_SELECTOR,('iframe[id*="gsi"]'))
    
    driver.switch_to.frame(iframe)
    
    span =driver.find_elements(By.TAG_NAME,('span'))[0]
   
    while len(driver.window_handles) == 1:
        try:
            span.click()
        except:
            time.sleep(2)
            driver.execute_script("document.querySelectorAll('span')[0].click()")    
    driver.switch_to.default_content()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    driver.find_element(By.ID,('identifierId')).send_keys(username)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR,('div[id="identifierNext"] button')).click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,('input[name="Passwd"]')).send_keys(password)
    time.sleep(4)
    driver.find_element(By.CSS_SELECTOR,('div[id="passwordNext"] button')).click()
    time.sleep(4)
    driver.switch_to.window(original_window)   
    
    
    
def getData():
    print('Gathering posts to search')
    k = 0
    while len(posts_data)<number_of_random_posts:
        links=[]
        while len(links) < 50:
            i=1 
            if i%50==0:
                driver.refresh()
                
            anchors= driver.find_elements(By.CSS_SELECTOR,('div[role="list"] > div a'))
            for a in anchors:
                try:                  
                    link = a.get_attribute('href') 
                    if link not in all_links and '/pin/' in link:
                        links.append(link)
                        all_links.append(link)
                        if len(links) == 50:
                            break
                except (StaleElementReferenceException ,WebDriverException) :
                    1
                
            driver.execute_script('window.scrollBy({top:window.innerHeight,left:0,behavior:"smooth"})')
            i+=1
        
        
                    
        file= open('test.txt','w')
        for l in all_links:
            file.write(l+'\n')
        file.close()
                

        
        for link in links:
            
            driver.get(link)
            
            likes_amount = ''
            possible_likes_amounts = driver.find_elements(By.CSS_SELECTOR,('div[class="tBJ dyH iFc sAJ O2T zDA IZT H2s"]'))
            if possible_likes_amounts:
                for pla in possible_likes_amounts:
                    try:
                        text = pla.text
                    except StaleElementReferenceException:
                        possible_likes_amounts = driver.find_elements(By.CSS_SELECTOR,('div[class="tBJ dyH iFc sAJ O2T zDA IZT H2s"]'))
                        if possible_likes_amounts:
                            for pla in possible_likes_amounts:
                                try:
                                    text = pla.text
                                except StaleElementReferenceException:
                                    text = '0'
                        else:
                            text = '0'                               
                    if '.' in text:
                        number= text.replace('k','00').replace('.','')
                    elif 'k' in text:
                        number =  text.replace('k','000')
                    else:
                        number = text     
                    if number.isnumeric() ==True:
                        likes_amount = number
                    else:
                        likes_amount = 0
            else:
                likes_amount = 0                
                  
            if int(likes_amount) > minimum_number_of_likes:
                image = driver.find_elements(By.CSS_SELECTOR,('img'))[1].get_attribute('src')
                video = driver.find_elements(By.CSS_SELECTOR,('div[aria-label="Pause or play video"]'))
                if video:
                    image = ''
                posts_data.append({'Link':link,'Image':image,'Likes':likes_amount})
                createHTML()
                if len(posts_data) == number_of_random_posts:
                    os.system('clear')
                    print(f'Searched {k+1} products')
                    print(f'Gathered {len(posts_data)} posts from {number_of_random_posts} posts')
                    sys.exit(1)
            os.system('clear')    
            k+=1
            if k == 1:
                print(f'Searched {k} post')
            else:   
                print(f'Searched {k} posts')
            if len(posts_data)== 1 or len(posts_data) == 0:                
                print(f'Gathered {len(posts_data)} post from {number_of_random_posts} posts')
            else:
                print(f'Gathered {len(posts_data)} posts from {number_of_random_posts} posts')
            print('Press ctrl+c to exit, gathered posts won\'t be lost')    


        driver.get('https://www.pinterest.com/')                 
def createHTML():  
    file=open(f'{file_name}.html','w',encoding="utf-8")
    template_head=f'''<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{file_name}</title>
                        <link href="style.css" rel="stylesheet">
                    </head>
                    <body>
                    <table data-table-theme="dark zebra">
                    <thead>
                        <tr>                                                                        
                        <th scope="col">Image</th>                        
                        <th scope="col">Likes</th>
                        </tr>
                    </thead>
                    <tbody>'''
    
    file.write(template_head)
    for post in posts_data:
        post_info = f'''<tr>
                            <td><a href="{post['Link']}" target="_blank"><img src="{post['Image']}"></a></th>                           
                                                      
                            <td>{post['Likes']}</td>
                        </tr>'''
               
        file.write(post_info)
           
    template_body='''        </tbody>
                        </table>
                        <script src="sorting.js"></script>  
                    </body>
                    </html>'''
    file.write(template_body)
    file.close()

def suppress_exception_in_del(uc):
    old_del = uc.Chrome.__del__

    def new_del(self) -> None:
        try:
            old_del(self)
        except:
            pass
    
    setattr(uc.Chrome, '__del__', new_del)

suppress_exception_in_del(uc)



try:
    main()
except KeyboardInterrupt:
    print('')
    print('Exited...')
    sys.exit(1)    