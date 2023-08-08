import time
import tkinter as tk
from tkinter import filedialog, messagebox

import keyboard
import pyautogui
import win32api, win32con
Baits=['Baits/baitCuprumCoin.png', 'Baits/baitSilverCoin.png', 'Baits/baitWood.png']
Garbage=['Garbage/garbage2.png']
GarbagePlace=['E.png', 'SE.png', 'GarbagePlaces/N.png', 'GarbagePlaces/NE.png', 'GarbagePlaces/NW.png', 'GarbagePlaces/S.png', 'GarbagePlaces/W.png']


def click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def drag_and_drop(x_start, y_start, x_end, y_end):
    pyautogui.moveTo(x_start, y_start)
    pyautogui.mouseDown()
    pyautogui.moveTo(x_end, y_end, duration=1)
    pyautogui.mouseUp()
    #clickShort(x_end,y_end)

def ThrowFishingRod():
    #win32api.SetCursorPos((x,y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def clickShort(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def FindGarbagePlace():
    for place in GarbagePlace:
        garbPlace = pyautogui.locateOnScreen(place, confidence=0.8)
        if garbPlace != None:
            return garbPlace


def prepare():
    locationHook=None
    locationLine=None
    while locationLine==None and locationHook==None:
        locationHook = pyautogui.locateOnScreen('hook.png', confidence=0.8)
        locationLine = pyautogui.locateOnScreen('line.png', confidence=0.8)

        if locationHook!=None and locationLine!=None:
            pyautogui.rightClick(locationHook)
            pyautogui.rightClick(locationLine)
            print("Hook and line")

def ThrowGarbage():
    time.sleep(4)
    for image in Garbage:
        garb = pyautogui.locateOnScreen(image, confidence=0.8)
        if garb is not None:
            #garbPlace = FindGarbagePlace()
            #if garbPlace!=None:
            drag_and_drop(garb[0], garb[1], 1, 1)
            print("good")
            #destroy=pyautogui.locateOnScreen("destroy.png", confidence=0.8)
            #print("j")
            ClickYes = pyautogui.locateOnScreen("Yes2.png", confidence=0.8)
            while ClickYes==None:
                ClickYes = pyautogui.locateOnScreen("Yes2.png", confidence=0.8)
            click(ClickYes[0], ClickYes[1])
            time.sleep(0.9)
            clickShort(ClickYes[0], ClickYes[1])
            print("Very good")
def select_bait():
    while True:
        for image in Baits:
            bait_location = pyautogui.locateOnScreen(image, confidence=0.8)
            if bait_location is not None:
                pyautogui.rightClick(bait_location)
                return  # Exit the loop after selecting the first bait found

def Fishing():
    print("dvs")
    keyboard.press('z')
    time.sleep(0.2)
    keyboard.release('z')
    ThrowFishingRod()
    #bottomHit = pyautogui.locateOnScreen("bottomLabel.png", confidence=0.8)
    #while bottomHit!=None:
        #ThrowFishingRod()
        #ThrowFishingRod()
def select_input_file():

    input_file_path = filedialog.askopenfilename(title="Select garbage image",
                                                 filetypes=(("Png files", "*.png"),("All files", "*.*")))
    if input_file_path:
        if not input_file_path.endswith(".png"):
            messagebox.showerror("Error", "Input file must be a .png file!")
            input_file_path = ""
        else:
            Garbage.append(input_file_path)

            #input_file_label['text'] = input_file_path

def select_output_file():


    output_file_path = filedialog.askopenfilename(title="Select garbage place image",
                                                 filetypes=(("Png files", "*.png"),("All files", "*.*")))
    if output_file_path:
        if not output_file_path.endswith(".png"):
            messagebox.showerror("Error", "Input file must be a .xls or .png file!")
           # output_file_path = ""
        else:
            GarbagePlace.append(output_file_path)
            #output_file_label['text'] = output_file_path

def select_Bait_Images():


    output_file_path = filedialog.askopenfilename(title="Select bait image",
                                                 filetypes=(("Png files", "*.png"),("All files", "*.*")))
    if output_file_path:
        if not output_file_path.endswith(".png"):
            messagebox.showerror("Error", "Input file must be a .xls or .png file!")
           # output_file_path = ""
        else:
            Baits.append(output_file_path)
            #output_file_label['text'] = output_file_path


def StartBot():
    time.sleep(2)
    ThrowGarbage()
    prepare()
    select_bait()
    Fishing()

root = tk.Tk()
Garbage_Image_button = tk.Button(root, text="Select Garbage Images", command=select_input_file, font=('Verdana', 14), padx=20, pady=10)
Garbage_Image_button.pack()

input_file_label = tk.Label(root, text="", font=('Verdana', 10))
input_file_label.pack(pady=10)

Garbage_Place_button = tk.Button(root, text="Select Garbage place images", command=select_output_file, font=('Verdana', 14), padx=20, pady=10)
Garbage_Place_button.pack()


Garbage_Place_button = tk.Button(root, text="Select Bait images", command=select_Bait_Images, font=('Verdana', 14), padx=20, pady=10)
Garbage_Place_button.pack()

output_file_label = tk.Label(root, text="", font=('Verdana', 10))
output_file_label.pack(pady=10)

process_button = tk.Button(root, text="Start Script", command=StartBot, font=('Verdana', 14), padx=20, pady=10)
process_button.pack()

root.mainloop()



#time.sleep(3)
