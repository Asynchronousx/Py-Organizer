import os
from pathlib import Path
from pprint import pprint
from collections import defaultdict

## function to retrieve file extension and filename
def get_files(data):   
    print("Retrieving files...")

    ## Scan the entire directory for files inside the directory itself
    for file in os.listdir():
        ## splitext return a tuple composed by the root (i.e: filename without extensione) and the extension itself
        ## (i.e: .txt, .png etc). This will be useful to throw into the dictionary extension as keys and file names as values.
        fname , ext = os.path.splitext(file)
        ## using the definition of the defaultdict, we're assigning to a specified key (given by the extension) the filename retrieved.
        ## since we used lists as default object factory, for that given key a list of filename exists. So we must append the name to it.
        ## Note: if the key do not exists, defaultdict for definition will create a new pair key:list with the new extension found.
        data[ext].append(fname)

    ## checking files into that directory (uncomment)
    ## pprint(data)

## function to organize retrieved data into the appropriate folders
def organize(data):
    print("Creating folders...")

    ## for each file into the file dictionary
    for k, v in data.items():
       
        ## getting the current cwd
        curpath = os.getcwd()

        ## Since we could have the "empty name folder ''", we must assure that we rename that extension with "Other".
        extfolder = "Other" if k=='' else k[1:].capitalize()

        ## This if checks if a found extension folder already exists in the current analyzed folder 
        ## How? isdir check that the extension folder, obtained through joining toghether curpath and the extfolder using Path.joinpath()
        ## (to create a correct reference to the OS Path we're on) exists. If exists, that skip the folder creation process and move
        ## forward to move the files into that folder.
        if not (os.path.isdir(Path(curpath).joinpath(extfolder))):
            os.mkdir(extfolder)

        ## for each file of the retrieved list at the current key, move the file to the appropriate folder (based on the Key value).
        for file in v:
            ## checking that the file isn't a directory
            if not os.path.isdir(Path(curpath).joinpath(file+k)):
                ## os.rename takes in input the absolute path of the file we need to move as first argument, and the absolute path of the new
                ## directory we want to move that file in. We're using concatenation with "+" to improve complexity.
                os.rename(Path(curpath).joinpath(file+k), Path(curpath).joinpath(extfolder).joinpath(file+k))

## print video intro and take folder path     
def intro():
    ascii_art = """
     _____            ____                              _
    |  __ \          / __ \                            (_)
    | |__) | _   _  | |  | | _ __   __ _   __ _  _ __   _  ____  ___  _ __
    |  ___/ | | | | | |  | || '__| / _` | / _` || '_ \ | ||_  / / _ \| '__|
    | |     | |_| | | |__| || |   | (_| || (_| || | | || | / / |  __/| |
    |_|      \__, |  \____/ |_|    \__, | \__,_||_| |_||_|/___| \___||_|
              __/ |                 __/ |
             |___/                 |___/
    """
    print(ascii_art)
    print("Insert path or Drop&Drag a folder to a specify where to organize files, leave blank if desired is <CURRENT FOLDER>")
    print("Desired Path: ", end='')

    ## getting user folder input
    folder_path = input()

    ## check if folder path: exit otherwise
    if folder_path: 
        try:
            os.chdir(folder_path)
        except Exception:
            print("Make sure to insert a correct path and try again.")
            exit(0)
    



## entry point
if __name__ == '__main__':
    ## Using defaultdict to get rid of KeyError. This will allow us to, whenever a new 
    ## key extension is found, to initialize a new key with a default object factory of type list.
    ## this will create, for any new given key, a new generic list (which will contain the string filenames).
    fdata = defaultdict(list)

    ## doing things
    intro()
    get_files(fdata)
    organize(fdata)

    # done
    print("Work Done!")
