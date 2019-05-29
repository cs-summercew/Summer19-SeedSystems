
# BeautifulSoup documentation:
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
try: 
    from bs4 import BeautifulSoup
except:
    print("Please install the BeautifulSoup library and try again")
try:
    import requests
except:
    print("Please install the requests library and try again")
try:
    import os
except:
    print("Please install the os library and try again")
try:
    import shutil
except:
    print("Please install the shutil library and try again")

# If you get any of these except errors, 
# installing Anaconda should ensure that 
# you have all the proper libraries installed...
# https://www.anaconda.com/distribution/


# Global Variables
URL = "https://esolangs.org/wiki/Language_list"
baseURL = "https://esolangs.org"
newURL = "https://freedirectorysubmissionsites.com"


def setup():
    " Makes a folder to hold our html files, and return a path to that folder"
    original_dir = os.getcwd()
    dirContents = os.listdir(original_dir)
    path = os.path.join(original_dir, "Scraped_Files")
    if "Scraped_Files" in dirContents:
            shutil.rmtree(path) # Removes directories regardless of if they're empty
    os.mkdir(path)
    return path

def createfiles(listOflinks, path):
    "Creates file directory"
    for link in listOflinks:
        # Make the paths for each file
        name = link.get('href')
        print(name)
        file_name = name[6:]+".html"    #TODO: name[6:] will not work on more complex lists
        print("File name is",file_name)
        filePath = os.path.join(path, file_name)
        # Get the info that will be written to the files
        URLtoLoop = baseURL + name
        print(URLtoLoop)
        info = requests.get(URLtoLoop)
        finalInfo = info.text
        # Write the files
        with open(filePath, 'w') as f:
            f.write(finalInfo)
    return

def makesoup(Ourpath):
    "Creates a beautiful soup object that can be used to parse our webpage for links"
    result = requests.get(URL)
    pagesrc = result.text # Turns the html into a single string
    soup = BeautifulSoup(pagesrc,"lxml")
    return soup


def main():
    print("Start of main()\n")
  
    #print(LinkList[33]) #external resources link
    #Links to other lang pages start @35 (!!!)
    
    Ourpath = setup()
    soup = makesoup(Ourpath)
    
    LinkList = soup.findAll('a')
    LinkList_Subset=LinkList[35:40]
    createfiles(LinkList_Subset, Ourpath)
    

    print("End of main()\n")

if __name__ == "__main__":
    main()