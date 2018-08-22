import pygame
from pygame.locals import *
import math
import time
import random
import glob
import os, os.path
import cv2
import detect_face_white
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0, 30)

def resize_img(img, w, h, interpolation = cv2.INTER_AREA):
    res = cv2.resize(img, (w, h), interpolation = interpolation)

    return res

pygame.init()

width = 480
height = 680
w_small = 50
h_small = 50
w_big = 95
h_big = 50

display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("How to be a beautiful girl?")

screen_ = pygame.display.set_mode((width, height))

color = {
    'white': (255, 255, 255),
    'bright_white': (255, 255, 200),
    'blue': (0, 0, 255),
    'bright_blue': (117, 156, 255),
    'green': (0, 200, 0),
    'black': (0, 0, 0),
    'bright_green': (0, 255, 0),
    'red': (200,0,0),
    'bright_red': (255,0,0),
    'yellow': (200,200,0),
    'bright_yellow': (255,255,0),
}

bg = cv2.imread("picture\\bg.jpg")
bg = resize_img(bg, width, height)
path = "picture/"
cv2.imwrite(path + "bg.jpg", bg)
bg = pygame.image.load('picture/bg.jpg').convert_alpha()

menu_img = {
    "EYE": cv2.imread('picture/eye_menu.jpg'),
    "LIP": cv2.imread('picture/lip_menu.jpg'),
    "EYEBROW": cv2.imread('picture/eyebrow_menu.jpg'),
    "BEARD": cv2.imread('picture/beard_menu.jpg')
}

for key in menu_img.keys():
    menu_img[key] = resize_img(menu_img[key], width, height)
    cv2.imwrite(path + key.lower() + '_menu.jpg', menu_img[key])
    menu_img[key] = pygame.image.load('picture/' + key.lower() + '_menu.jpg').convert_alpha()

fps = 200 #Số frame trên giây
fps_clock = pygame.time.Clock()

btn_0 = []
btn_1 = []

btn_clicked = {"EYE": [],
               "LIP": [],
               "EYEBROW": [],
               "BEARD": []}

class Button:
    def __init__(self, x, y, w, h, func, mouse_pos, click, tier, text = None, img = None, color = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.func = func
        self.mouse_pos = mouse_pos
        self.click = click
        self.tier = tier
        self.text = text
        self.color = color
        self.img = img
        self.check = False
    def display(self):
        if self.x + self.w > self.mouse_pos[0] > self.x\
            and self.y + self.h > self.mouse_pos[1] > self.y:
            if self.tier == 0:
                pygame.draw.rect(display_surf, color['bright_' + self.color], (self.x, self.y, self.w, self.h), 0)
            else:
                display_surf.blit(self.img, (self.x, self.y))

            if self.click[0] == 1:
                print("shit")
                self.button_func()
        else:
            if self.tier == 0:
                pygame.draw.rect(display_surf, color[self.color], (self.x, self.y, self.w, self.h), 0)
            else:
                display_surf.blit(self.img, (self.x, self.y))

        if self.text is not None:
            font = pygame.font.Font(None, 20)
            button_text = font.render(self.text, True, color['white'])
            display_surf.blit(button_text, (self.x + 5, self.y + self.h / 2 - 8))
    def button_func(self):
        if self.tier == 0:
            if self.func in ["EYE", "LIP", "EYEBROW", "BEARD"]:
                face_menu(self.func)
            elif self.func == "BACK":
                main()
        else:
            if self.func == "BACK":
                main()
            else:
                self.check = True

class Program:
    def __init__(self, button):
        self.btn = button
    def draw_arena(self):
        display_surf.blit(bg, (0, 0))
        for btn in self.btn:
            btn.display()

def face_menu(part):
    global btn_clicked
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        display_surf.fill(color["black"])
        display_surf.blit(menu_img[part], (0, 0))

        old_pos = (0, 20)

        low_part = part.lower()
        path = "picture/" + low_part + "/"
        path_cv = "picture\\" + low_part + "\\"

        btns = []

        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if len(glob.glob(path + "*")) > 0:
            for i in range(len(glob.glob(path + "*"))):
                img_path = path_cv + low_part + str(i + 1) + ".png"
                img = cv2.imread(img_path)
                img = resize_img(img, w_small, h_small)
                cv2.imwrite(path + low_part + str(i + 1) + ".png", img)

                img = pygame.image.load(img_path).convert_alpha()

                if old_pos[0] + 20 < width - w_small - 20:
                    btns.append(Button(old_pos[0] + 20, old_pos[1], w_small, h_small, low_part + str(i + 1), mousepos, click, 1, img= img))
                    old_pos = (old_pos[0] + w_small + 20, old_pos[1])
                else:
                    btns.append(Button(20 , old_pos[1] + h_small + 20, w_small, h_small, low_part + str(i + 1), mousepos, click, 1, img = img))
                    old_pos = (20 + w_small, old_pos[1] + h_small + 20)

            for btn in btns:
                btn.display()
                if btn.check == True:
                    btn_clicked[part].append(low_part + str(btns.index(btn) + 1))

            if len(btn_clicked[part]) > 1:
                for i in range(len(btn_clicked[part]) - 1):
                    del btn_clicked[part][i]

        back_img = cv2.imread("picture\\back_button.png")
        back_img = resize_img(back_img, w_small, h_small)
        cv2.imwrite("picture/back_button.png", back_img)
        back_img = pygame.image.load('picture/back_button.png').convert_alpha()
        back = Button(10, height - h_small - 15, w_small, h_small, "BACK", mousepos, click, 1, img = back_img)
        # back = Button(20, height - h_small- 15, w_big, h_big, "BACK", mousepos, click, 0, "Back", color= "red")
        back.display()
        pygame.display.update()

def main():
    global FLAG
    FLAG = True
    n = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flag = True

        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        lip_btn = Button(20, height - h_big - 20, w_big, h_big, "LIP", mousepos, click, 0, "Lip",
                         color="blue")
        eye_btn = Button(20 + w_big + 20, height - h_big - 20, w_big, h_big, "EYE", mousepos, click, 0,
                         "Eye", color="blue")
        eyebrow_btn = Button(20 + w_big * 2 + 40, height - h_big - 20, w_big, h_big, "EYEBROW", mousepos, click,
                             0, "Eyebrow", color="blue")
        beard_btn = Button(20 + w_big * 3 + 60, height - h_big - 20, w_big, h_big, "BEARD", mousepos, click, 0,
                           "Beard", color="blue")

        btns = [lip_btn, eye_btn, eyebrow_btn, beard_btn]
        program = Program(btns)
        program.draw_arena()
        # if n==0:
        #     n = 1
        #     program.draw_arena()
        # else:
        #     if FLAG and click[0] == 1:
        #         FLAG = False
        #         program.draw_arena()

        pygame.display.update()
        fps_clock.tick(fps)

if __name__ == '__main__':
    main()