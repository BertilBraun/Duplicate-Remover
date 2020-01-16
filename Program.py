import os
import cv2
import glob
import tqdm
import datetime
import numpy as np
from PIL import Image
from multiprocessing import Pool, cpu_count

def load(path):

    try:
        image = Image.open(path)
        image = image.resize((500, 500))

        return image

    except Exception as ex:
        print(ex)
        return None

def mse(imageA, imageB):

    err = np.sum((np.asarray(imageA).astype("float") - np.asarray(imageB).astype("float")) ** 2)
    err /= float(imageA.size[0] * imageA.size[1])
    
    return err

def get_all_files_in_folder(folder, extention):

    return glob.glob(folder + "/*" + extention)
   
def delete(data):
    
    i = data[0]
    files = data[1]    
    f1 = files[i]
    imageA = load(f1)
    
    if imageA == None:
        print("Image coudnt be loaded " + f1)
        return
    
    for j in range(i + 1, len(files) - 1):
        
        f2 = files[j]
        imageB = load(f2)

        if imageB == None:
            print("Image coudnt be loaded " + f2)
            continue
    
        if mse(imageA, imageB) < 500:     
            print("del file : " + f2)
            os.remove(f2)
            
    print(str(i) + " compelte " + datetime.datetime.now().strftime("%H:%M:%S"))
    
def delete_files(files):

    p = Pool(cpu_count())
    
    p.map(delete, ([i, files] for i in range(len(files))))
    
def clean_folder(folder, extention = '.jpg'):

    files = get_all_files_in_folder(folder, extention)
    
    print("\ncleaning Folder \"" + folder + "\" with " + str(len(files)) + " Files\n")

    delete_files(files)
    
def clean_sub_folders(folder):
    dirs = [os.path.join(folder, o) for o in os.listdir(folder) if os.path.isdir(os.path.join(folder,o))]

    for f in dirs:
        clean_sub_folders(f)
        clean_folder(f)
    
if __name__ == '__main__': 
    d = 'C:/Users/Braun/Desktop/Pictures'
    
    clean_sub_folders(d)
    clean_folder(d)