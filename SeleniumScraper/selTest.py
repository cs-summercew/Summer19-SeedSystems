
# NOTE: Installation Instructions for Firefox
# Use "pip install selenium" to install selenium for python
# Go to https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/ to install the Selenium add-on for Firefox
# Go to https://github.com/mozilla/geckodriver/releases to install geckodriver
# Make sure to choose the geckodriver file that corresponds to your OS
# More helpful documentation info at https://selenium-python.readthedocs.io/getting-started.html

import time
#NOTE: We use sleep from the time library because the code often runs faster than pages can load.
#      We also added a few extra so that you can watch what is happening.
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import Select
except:
    print("please run 'pip install selenium' and try again")


def createdriver(url, path):
    "Creates the selenium driver object"
    opts = Options()
    # NOTE: Incognito mode may prevent the popup from appearing
    # opts.add_argument("—headless")     #Runs Firefox invisibly w/o a user interfaces
    # opts.add_argument("-incognito")     #Rusn Firefox in incognito mode
    driver = webdriver.Firefox(executable_path=path, options=opts)
    driver.get(url)
    return driver

def savepage(driver):
    "Saves the current html page as an html file"
    #TODO: Implement
    html = driver.page_source
    return html

def screenshot(driver):
    "Takes a screenshot of the current page and save it as a png"
    driver.save_screenshot("screenshot.png")
    return

def websearch(driver):
    "Conducts two websearchs using duckduckgo"
    search_form = driver.find_element_by_id('search_form_input_homepage')
    search_form.send_keys("I'm feeling famished. A churro sounds great!")
    time.sleep(2)
    search_form.clear() # Clears the searchbar of text
    search_form.send_keys("sdklfjgblsdkfjgblsdkjfgdfgadftgafdhdfhdfdag")
    search_form.submit() # Enters the current earch

    #BUG
    # # If a page or some elements of it load slowly, then you can wait for
    # # it to load with code like below
    # try:
    #     print('hi')
    #     # search_form = driver.find_element_by_id('search_form_input')
    #     # print(search_form)
    #     wait = WebDriverWait(driver, 3)
    #     element = wait.until(EC.visibility_of((By.ID, "'search_form_input'")))
    #     print('hi')
    #     print(element)
    #     #time.sleep(3)
    # except:
    #     print("Your Internet must suck! The webpage took too long to load.")
    
    time.sleep(2)
    search_form = driver.find_element_by_id('search_form_input')
    search_form.clear()
    search_form.send_keys("esoteric programming languages churro")
    search_form.submit()
    
    # Checks that we're on the second search, and have results
    time.sleep(0.1)
    assert "No results found" not in driver.page_source
    return

def closebrowser(driver):
    "Closes the browser"
    driver.close()  # Closes a single tab
    driver.quit()   # Closes all tabs
    return

def closepopup(driver):
    "Closes the duckduckgo add-on popup for FIREFOX"
    try: 
        # NOTE: You can find the xpath of an element by right-clikcing it in the browser
        #       and clicking inspect element. Right click on the respective html code, and
        #       you should see an option to copy the element's XPATH
        close_button = driver.find_element(By.XPATH, "/html/body/div/div[5]/a/span")

        # NOTE: ActionChains lets you automate low level interactions like mouse movements & button presses
        actions = ActionChains(driver)
        actions.move_to_element(close_button)
        actions.click(close_button)
        actions.perform()
    except:
        print("If the popup wasn't there, you probably didn't use firefox."+"\n"+
        "If the popup wasn't there, try without incognito mode or just comment out this function")
    return

def useform(driver):
    "Opens a feedback form for our search, and interacts with it"
    time.sleep(1.0)
    sendfeedback_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[4]/div[2]/div/div/a")
    actions = ActionChains(driver)
    actions.move_to_element(sendfeedback_button)
    actions.click(sendfeedback_button)
    actions.perform()

    good_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[4]/div[2]/div/div/div/a[1]")
    actions = ActionChains(driver)
    actions.move_to_element(good_button)
    actions.click(good_button)
    actions.perform()

    select = Select(driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/select"))
    select.select_by_index(13)
    textbox = driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/textarea")
    textbox.send_keys("I am testing the powers of automation with Selenium. Please ignore this feedback.")

    close_button1 = driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/a[1]")
    actions = ActionChains(driver)
    actions.move_to_element(close_button1)
    actions.click(close_button1)
    actions.perform()

    #BUG: The section of code below keeps throwing an error and I don't know why
    close_button2 = driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[2]/a")
    actions = ActionChains(driver)
    actions.move_to_element(close_button2)
    actions.click(close_button2)
    actions.perform()

    return
def main():
    """ run this file as a script """
    # # Prints all the links on the webpage below
    # driver.get('https://www.w3.org/')
    # for a in driver.find_elements_by_xpath('.//a'):
    #     print(a.get_attribute('href'))
    
    driver = createdriver('https://duckduckgo.com',
    '/Users/summer19/Documents/GitHub/Summer19-SeedSystems/SeleniumScraper/geckodriver')
    closepopup(driver)
    websearch(driver)
    useform(driver)
    #savepage(driver)
    #screenshot(driver)

    # link = driver.find_element_by_link_text('Esoteric programming language - Esolang')
    # print(link.text)
    # print(link.get_attribute('href'))
    
    # Closes the open web browser
    time.sleep(2)
    #closebrowser(driver)



if __name__ == "__main__":
    main()