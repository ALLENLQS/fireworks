#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : ALLEN
# @Time    : 2018/12/15 16:10
# @File    : fireworks.py
# @Software: PyCharm
import tkinter as tk
from PIL import Image,ImageTk
from time import time,sleep
from random import choice,uniform,randint
from math import sin,cos,radians

# 模拟重力
GRAVITY = 0.08
colors = ['red','blue','yellow','white','green','blue','orange','purple','seagreen','indigo','cornflowerblue']
'''
粒子在空中随机生成，变成一个圈、下坠、消失
属性：
-id:粒子的idroot.after
-x,y:粒子的坐标
-vx,vy:在坐标的变化速度
-total:总数
-age:粒子存在的时长
-color:颜色
-cv:画布
-lifespan:最高存在时长
'''

class Particle:
    def __init__(self,cv,idx,total,explosion_speed,x=0.,y=0.,vx=0.,vy=0.,size=2,color='red',lifespan=2,**kwargs):
        self.id = idx
        self.x = x
        self.y = y
        self.initial_speed = explosion_speed
        self.vx = vx
        self.vy = vy
        self.total = total
        self.age = 0
        self.color = color
        self.cv = cv
        self.cid = self.cv.create_oval(
            x - size,y - size,x + size,y + size,fill = self.color
        )
        self.lifespan = lifespan

    def update(self,dt):
        self.age += dt
        # 粒子范围扩大
        if self.alive() and self.expand():
            move_x = cos(radians(self.id * 360/self.total)) * self.initial_speed
            move_y = sin(radians(self.id * 360/self.total)) * self.initial_speed
            self.cv.move(self.cid,move_x,move_y)
            self.vx = move_x / (float(dt) * 1000)
        # 以自由落体坠落
        elif self.alive():
            move_x = cos(radians(self.id * 360/self.total))
            self.cv.move(self.cid, self.vx + move_x,self.vy + GRAVITY * dt)
            self.vy += GRAVITY * dt
        # 移除超过最高时长的粒子
        elif self.cid is not None:
            self.cv.delete(self.cid)
            self.cid = None

    # 扩大时间
    def expand(self):
        return self.age <= 1.2

    # 粒子是否在最高存在的时长内
    def alive(self):
        return self.age <= self.lifespan

'''循环保持不停'''
def simulate(cv):
    t = time()
    explode_points = []
    wait_time = randint(10,100)
    number_explode = randint(6,10)
    for point in range(number_explode):
        objects = []
        x_cordi = randint(50,550)
        y_cordi = randint(50,150)
        speed = uniform(0.5,2)
        size = uniform(0.5,3)
        color = choice(colors)
        explosion_speed = uniform(0.2,1.5)
        total_particles = randint(10,50)
        for i in range(1,total_particles):
            r = Particle(cv,idx=i,total=total_particles,explosion_speed=explosion_speed,x = x_cordi,y=y_cordi,
                         vx=speed,vy=speed,color=color,size=size,lifespan=uniform(0.6,1.75))
            objects.append(r)
        explode_points.append(objects)
    total_time = .0
    # 1.8s内一直扩大
    while total_time < 1.8:
        sleep(0.01)
        tnew = time()
        t,dt = tnew,tnew - t
        for point in explode_points:
            for item in point:
                item.update(dt)
        cv.update()
        total_time += dt
    # 循环调用
    root.after(wait_time,simulate,cv)

def close(*ignore):
    '''退出程序，关闭窗口'''
    global root
    root.quit()

if __name__ == '__main__':
    root =tk.Tk()
    cv = tk.Canvas(root,height=400,width=600)
    # 选一个好看的背景会让效果更惊艳
    image = Image.open("./images/timg.jpg")
    photo = ImageTk.PhotoImage(image)

    cv.create_image(1,1,image=photo)
    cv.pack()

    root.protocol("WM_DELETE_WINDOW",close)
    root.after(100,simulate,cv)
    root.mainloop()