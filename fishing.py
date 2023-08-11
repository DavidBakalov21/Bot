import time
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import keyboard
import numpy as np
import pyautogui
import win32api, win32con
Baits=['Baits/baitCuprumCoin.png', 'Baits/baitSilverCoin.png', 'Baits/baitWood.png']
#Garbage=['Garbage/garbage2.png']
Garbage=[]
def CheckIfRestart():
    image = pyautogui.screenshot()
    # Converting the screenshot to a numpy array
    image_np = np.array(image)
    # Converting the array to a BGR image for OpenCV
    screenshot = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    height, width, _ = screenshot.shape
    top_cut = int(0.91 * height)
    # Keep 86% from the top, which means cut 14% from the bottom

    right_cut = int(0.27 * width)
    screenshot = screenshot[top_cut:, :right_cut]  # Directly assign the cropped image to screenshot

    template_paths = ['Situations/Bottom_Hit.png', 'Situations/caught.png', 'Situations/lost_Bait.png',
                      'Situations/lost_Hook.png']
    max_vals = []

    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        alpha_channel = template[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, thresh=0, maxval=255, type=cv2.THRESH_BINARY)
        template_bgr = template[:, :, :3]
        masked_template = cv2.bitwise_and(template_bgr, template_bgr, mask=mask)
        result = cv2.matchTemplate(screenshot[:, :, :3], masked_template, cv2.TM_CCOEFF_NORMED, mask=mask)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        max_vals.append(max_val)

    best_template_index = np.argmax(max_vals)
    best_template_path = template_paths[best_template_index]

    if best_template_path in ['Situations/Bottom_Hit.png']:
        return 'BottomHit'
    elif best_template_path in ['Situations/caught.png']:
        return 'caught'
    elif best_template_path in ['Situations/lost_Bait.png']:
        return 'LostBait'
    elif best_template_path in ['Situations/lost_Hook.png']:
        return 'LostHook'
def CheckIfEmpty():
    image = pyautogui.screenshot()
    # Converting the screenshot to a numpy array
    image_np = np.array(image)
    # Converting the array to a BGR image for OpenCV
    screenshot = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    height, width, _ = screenshot.shape
    top_cut = int(0.75 * height)
    bottom_cut = height - int(0.1 * height)  # New line to cut 30% from the bottom
    left_cut = int(0.43 * width)
    right_cut = width - int(0.40 * width)
    cropped_screenshot = screenshot[top_cut:bottom_cut, left_cut:right_cut]

    template_path = 'empty.png'  # Path to the specific template you want to match
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    alpha_channel = template[:, :, 3]
    _, mask = cv2.threshold(alpha_channel, thresh=0, maxval=255, type=cv2.THRESH_BINARY)
    template_bgr = template[:, :, :3]
    masked_template = cv2.bitwise_and(template_bgr, template_bgr, mask=mask)
    result = cv2.matchTemplate(cropped_screenshot[:, :, :3], masked_template, cv2.TM_CCOEFF_NORMED, mask=mask)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    confidence_threshold = 0.94  # 90% confidence threshold
    if max_val >= confidence_threshold:
        return 'empty'
    else:
        return 'full'

def UltimateEye():
    image = pyautogui.screenshot()
    # Converting the screenshot to a numpy array
    image_np = np.array(image)
    # Converting the array to a BGR image for OpenCV
    screenshot = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    height, width, _ = screenshot.shape
    top_cut = int(0.35 * height)
    bottom_cut = height - int(0.46 * height)  # Cut 30% from the bottom
    left_cut = int(0.48 * width)
    right_cut = width - int(0.39 * width)
    screenshot = screenshot[top_cut:bottom_cut, left_cut:right_cut]  # Directly assign the cropped image to screenshot

    template_paths = ['Rods/DarkCurveSmall.png', 'Rods/curvedLightSmall.png', 'Rods/DarkCurvedSmall2.png',
                      'Rods/staightLightSmall.png', 'Rods/DarkStraightRodSmall.png', 'Rods/LightStraight.png']
    max_vals = []

    for path in template_paths:
        template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        alpha_channel = template[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, thresh=0, maxval=255, type=cv2.THRESH_BINARY)
        template_bgr = template[:, :, :3]
        masked_template = cv2.bitwise_and(template_bgr, template_bgr, mask=mask)
        result = cv2.matchTemplate(screenshot[:, :, :3], masked_template, cv2.TM_CCOEFF_NORMED, mask=mask)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        max_vals.append(max_val)

    best_template_index = np.argmax(max_vals)
    best_template_path = template_paths[best_template_index]


    if best_template_path in ['Rods/DarkStraightRodSmall.png', 'Rods/staightLightSmall.png', 'Rods/LightStraight.png']:
        return 'straight'
    if best_template_path in ['Rods/DarkCurveSmall.png', 'Rods/curvedLightSmall.png', 'Rods/DarkCurvedSmall2.png']:
        return 'bite'

def click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def Hold(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(3.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
def drag_and_drop(x_start, y_start, x_end, y_end):
    pyautogui.moveTo(x_start, y_start)
    pyautogui.mouseDown()
    pyautogui.moveTo(x_end, y_end, duration=1)
    pyautogui.mouseUp()
    #clickShort(x_end,y_end)


def CheckInventory():
    Inventory = pyautogui.locateOnScreen('Inventory.png', confidence=0.8)
    if Inventory==None:
        keyboard.press('i')
        time.sleep(0.2)
        keyboard.release('i')


def ThrowFishingRod():
    #win32api.SetCursorPos((x,y))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def clickShort(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def prepare():
    locationHook=None
    locationLine=None
    while locationLine==None or locationHook==None:
        locationHook = pyautogui.locateOnScreen('hook.png', confidence=0.7)
        locationLine = pyautogui.locateOnScreen('line.png', confidence=0.7)
        #iprint("Looking for hook and line")
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
def turnOff():
    print("dvs")
    keyboard.press('z')
    time.sleep(0.2)
    keyboard.release('z')
    # Experimental
    keyboard.press('i')
    time.sleep(0.2)
    keyboard.release('i')


def Fishing():

    #Experimantal

    ThrowFishingRod()
    if CheckIfRestart()=="BottomHit":
        return
    time.sleep(1.2)
    start_time = time.time()
    last_print_time = start_time




    while CheckIfEmpty()=="full":

        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        #time.sleep(1)
        Eye=UltimateEye()
        print(Eye)
        if Eye=='bite':
            #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            last_print_time = start_time
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            while UltimateEye()=='bite' and CheckIfEmpty()=="full":
                pass

            #time.sleep(0.7)

            #UltimateEye()
            #CheckIfEmpty()
            #time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

            NextMove=CheckIfRestart()
            if NextMove=='caught' or NextMove=='LostBait' or NextMove=='LostHook':
                return
            time.sleep(1)
            print("end")
            #return


        #time.sleep(0.3)
        #print("Searching")
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        #time.sleep(0.3)
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        if time.time() - last_print_time >= 80:
            Minormove()
            last_print_time = time.time()
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        #Minormove()






def ConvertPathToText(path):
    res=""
    for text in path:
        pathSplited=text.split("/")
        res+=pathSplited[len(pathSplited)-1]+", "
    return res




def select_input_files():
    input_file_paths = filedialog.askopenfilenames(title="Select garbage images",
                                                   filetypes=(("Image files", "*.png;*.jpg;*.jpeg"),
                                                              ("All files", "*.*")))
    if input_file_paths:
        for path in input_file_paths:
            if not path.lower().endswith((".png", ".jpg", ".jpeg")):
                messagebox.showerror("Error", "Input files must be .png, .jpg, or .jpeg files!")
                return
            Garbage.append(path)
        input_file_label['text'] = ConvertPathToText(Garbage)
def select_Bait_Images():
    output_file_paths = filedialog.askopenfilenames(title="Select bait images",
                                                    filetypes=(("Image files", "*.png;*.jpg;*.jpeg"),
                                                               ("All files", "*.*")))
    if output_file_paths:
        for path in output_file_paths:
            if not path.lower().endswith((".png", ".jpg", ".jpeg")):
                messagebox.showerror("Error", "Input files must be .png, .jpg, or .jpeg files!")
                return
            Baits.append(path)
        output_file_label['text'] = ConvertPathToText(Baits)

def move():
    print("Move")
    keyboard.press("a")
    time.sleep(1)
    keyboard.release('a')
    time.sleep(1)
    # Experimental
    keyboard.press('d')
    time.sleep(1)
    keyboard.release('d')
    print("Move Finished")

def Minormove():
    print("Move")
    keyboard.press("a")
    time.sleep(0.5)
    keyboard.release('a')
    time.sleep(0.7)
    # Experimental
    keyboard.press('d')
    time.sleep(0.5)
    keyboard.release('d')
    print("Move Finished")

def StartBot():
    while keyboard.is_pressed("q")==False:
        time.sleep(2)
        move()
        CheckInventory()
        ThrowGarbage()
        prepare()
        select_bait()
        turnOff()
        Fishing()
        keyboard.press("x")
        time.sleep(0.1)
        keyboard.release('x')
        time.sleep(0.5)
        keyboard.press("x")
        time.sleep(0.1)
        keyboard.release('x')
        time.sleep(0.5)
        keyboard.press("z")
        time.sleep(0.1)
        keyboard.release('z')


root = tk.Tk()
Garbage_Image_button = tk.Button(root, text="Select Garbage Images", command=select_input_files, font=('Verdana', 14), padx=20, pady=10)
Garbage_Image_button.pack()

input_file_label = tk.Label(root, text="", font=('Verdana', 10))
input_file_label.pack(pady=10)

Garbage_Place_button = tk.Button(root, text="Select Bait images", command=select_Bait_Images, font=('Verdana', 14), padx=20, pady=10)
Garbage_Place_button.pack()

output_file_label = tk.Label(root, text="", font=('Verdana', 10))
output_file_label.pack(pady=10)

process_button = tk.Button(root, text="Start Script", command=StartBot, font=('Verdana', 14), padx=20, pady=10)
process_button.pack()

root.mainloop()

