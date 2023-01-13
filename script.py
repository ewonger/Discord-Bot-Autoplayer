#Pokemeow Autoplayer
#Requires Tesseract OCR v5.0.0
#Needs to be run on Windows or MacOS

from PIL import Image, ImageGrab
import pytesseract
import keyboard
import time
import re
import sys
import random
import pyautogui
import smtplib
import emails
from email.message import EmailMessage


# needs to be set depending on your window position
messagebar_x = 765
messagebar_y = 1839
balls_box = (695, 1649, 966, 1738)
rarity_box = (693, 1537, 1062, 1608)


def check_email():
    if emails.server_email == '' or emails.server_pass == '' or emails.to_email == '':
        sys.exit('Empty field for email/pass')

def send_email():
    msg = EmailMessage()
    msg.set_content(time.ctime(time.time()))
    msg['Subject'] = 'Pokemeow Captcha'
    msg['From'] = emails.server_email
    msg['To'] = emails.to_email

    server = smtplib.SMTP_SSL('smtp.gmail.com: 465')
    server.login(emails.server_email, emails.server_pass)
    server.send_message(msg)
    server.quit()
    print('\nEmail successfully sent')


def click_messagebar():
    old_pos = pyautogui.position()
    pyautogui.click(messagebar_x, messagebar_y)
    pyautogui.moveTo(old_pos)
    return


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

word_check =  ['[AC]', 'PokeCoins!', 'Premierballs:', 'Garlic,']
time.sleep(5)

while True:
    check_email()
    click_messagebar()
    keyboard.write(';p')
    keyboard.send('enter')

    time.sleep(float(random.randrange(100, 300))/100)
    img_rarity = ImageGrab.grab(bbox=rarity_box)
    img_balls = ImageGrab.grab(bbox=balls_box)
    # img_rarity.save('ss.png')
    # img_balls.save('s.png')
    # img_rarity = Image.open('rarity.png')
    # img_balls =  Image.open('balls.png')
    rarity_list = pytesseract.image_to_string(img_rarity).split()
    try:
        rarity  = rarity_list[0]
    except:
        sys.exit("Cannot detect rarity/balls box")

    # Retake screenshot if OCR is incorrect
    if any(item in word_check for item in rarity_list):
        print('Retake screenshot: ', rarity_list)
        time.sleep(1)
        img_rarity = ImageGrab.grab(bbox=rarity_box)
        rarity_list = pytesseract.image_to_string(img_rarity).split()
        rarity  = rarity_list[0]

    # Send email if captcha
    elif any('captcha' in item for item in rarity_list):
        send_email()
        print(rarity_list)
        break

    # Converts rarity streak from string to int
    try:
        if rarity_list[-1] == 'O':
            streak = 0
        else:
            streak = int(rarity_list[-1])
    except ValueError:
        print('err rarity\n')
        img_rarity.save('ss.png')
        print(rarity_list)
        break

    balls_list = pytesseract.image_to_string(img_balls).split()
    print(rarity_list[0], rarity_list[-1])
    # print(balls_list)

    
    if 'Common' == rarity or '‘Common' == rarity:
        old_pos = pyautogui.position()
        pyautogui.click(765, 1839)
        pyautogui.moveTo(old_pos)

        if streak % 15 >= 7:
            keyboard.write('gb')
            keyboard.send('enter')
        else:
            keyboard.write('pb')
            keyboard.send('enter')
    elif 'Uncommon' == rarity or '‘Uncommon' == rarity:
        old_pos = pyautogui.position()
        pyautogui.click(765, 1839)
        pyautogui.moveTo(old_pos)

        if streak % 10 >= 5:
            keyboard.write('gb')
            keyboard.send('enter')
        else:
            keyboard.write('pb')
            keyboard.send('enter')
    elif 'Rare' == rarity or '‘Rare' == rarity:
        old_pos = pyautogui.position()
        pyautogui.click(765, 1839)
        pyautogui.moveTo(old_pos)

        if streak % 5 >= 3:
            keyboard.write('ub')
            keyboard.send('enter')
        else:
            keyboard.write('gb')
            keyboard.send('enter')
    elif 'Super' == rarity or '‘Super' == rarity:
        old_pos = pyautogui.position()
        pyautogui.click(765, 1839)
        pyautogui.moveTo(old_pos)

        keyboard.write('ub')
        keyboard.send('enter')
    elif 'Legendary' == rarity or '‘Legendary' == rarity or 'Shiny' == rarity or '‘Shiny' == rarity:
        old_pos = pyautogui.position()
        pyautogui.click(765, 1839)
        pyautogui.moveTo(old_pos)

        keyboard.write('mb')
        keyboard.send('enter')
    else:
        print('err rarity\n')
        img_rarity.save('ss.png')
        print(rarity_list)
        break
    
    if 'Pokeballs:' == balls_list[0] or 'Pokeballs' == balls_list[0]:
        buy_flag = False
        balls_num = []
        for item in balls_list:
            found = re.findall(r'\d+', item)
            if found: 
                balls_num.append(found[0])
        print(balls_num)

        time.sleep(float(random.randrange(200, 400))/100)
        #Pokeballs
        if int(balls_num[0]) < 2:
            buy_flag = True
            click_messagebar()
            keyboard.write(';s buy 1 20')
            keyboard.send('enter')
            time.sleep(float(random.randrange(500, 700))/100)
        #Ultraballs
        if int(balls_num[1]) < 2:
            buy_flag = True
            click_messagebar()
            keyboard.write(';s buy 3 2')
            keyboard.send('enter')
            time.sleep(float(random.randrange(500, 700))/100)
        #GreatBalls
        if int(balls_num[2]) < 2:
            buy_flag = True
            click_messagebar()
            keyboard.write(';s buy 2 5')
            keyboard.send('enter')
            time.sleep(float(random.randrange(500, 700))/100)

        if not buy_flag:
            time.sleep(float(random.randrange(700, 900))/100)
        else:
            time.sleep(float(random.randrange(300, 500))/100)
    else:
        print('err balls\n')
        img_balls.save('s.png')
        # break
        time.sleep(float(random.randrange(900, 1100))/100)
    