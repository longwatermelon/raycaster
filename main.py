from tkinter import *
import time
import math
import sys

tk = Tk()
canvas = Canvas(tk, width=1024, height=512, highlightthickness=0)
tk.resizable(0,0)
tk.title('thats sick bro')
canvas.pack()
tk.update()

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pxl = 0
        self.pyl = 0
        self.canvas = canvas
        self.lineLength = 10
        self.dangle = 0
        self.px = 240
        self.py = 300
        self.speed = 0
        self.angle = 159
        self.disT = 0
        self.rays = [r for r in range(0, 60)]
        self.walls = [w for w in range(0, 60)]
        self.id = canvas.create_rectangle(self.px - 5, self.py - 5, self.px + 5, self.py + 5, fill='yellow')
        canvas.bind_all('<KeyPress-Up>', self.move_f)
        canvas.bind_all('<KeyPress-Down>', self.move_b)
        canvas.bind_all('<KeyPress-Right>', self.turn_r)
        canvas.bind_all('<KeyPress-Left>', self.turn_l)

        canvas.bind_all('<KeyRelease-Up>', self.stop_y)
        canvas.bind_all('<KeyRelease-Down>', self.stop_y)
        canvas.bind_all('<KeyRelease-Right>', self.stop_rotation)
        canvas.bind_all('<KeyRelease-Left>', self.stop_rotation)

    def stop_rotation(self, evt):
        self.dangle = 0

    def move_f(self, evt):
        self.speed = 2

    def move_b(self, evt):
        self.speed = -2

    def turn_r(self, evt):
        self.dangle = 2

    def turn_l(self, evt):
        self.dangle = -2

    def stop_y(self, evt):
        self.speed = 0

    def move(self):
        if self.y > 0:
            yoffset = 5
        else:
            yoffset = -5

        if self.x > 0:
            xoffset = 5
        else:
            xoffset = -5
            
        if grid[int(((self.py + yoffset) + self.y) / 64)][int(((self.px + xoffset) ) / 64)][0] == 0:
            self.canvas.move(self.id, 0, self.y)
            self.py += self.y
        if grid[int((self.py)/64)][int((self.px+xoffset+self.x)/64)][0] == 0:
            self.canvas.move(self.id, self.x, 0)
            self.px += self.x
            
        self.angle += self.dangle
        
        self.drawRays2()
        self.line = self.canvas.create_line(self.px, self.py, self.px + self.pxl, self.py + self.pyl, fill='green')
        self.pxl = math.cos(math.radians(self.angle)) * self.lineLength
        self.pyl = math.sin(math.radians(self.angle)) * self.lineLength

        self.x = (math.cos(math.radians(self.angle)) * self.speed)
        self.y = (math.sin(math.radians(self.angle)) * self.speed)
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360

        pos = self.canvas.coords(self.id)


    def drawRays2(self):
        global gridX, gridY, blockS
        self.rayAngle = self.angle - 31
        #print(self.px, self.py, self.angle)
        for r in range(len(self.rays)):
            self.rayAngle += 1
            if self.rayAngle >= 360:
                self.rayAngle -= 360
            if self.rayAngle <0:
                self.rayAngle += 360

            bx1 = int(self.px // blockS)
            by1 = int(self.py // blockS)
        
            if grid[by1][bx1][0] == 1:
                print("error: in a block")
                self.rx = self.px
                self.ry = self.py
                horX = 0
                horY =0
                verX = 0
                verY = 0
                lineO = 0
                lineH = 0
                
                
            else:
    
                vx = [n*blockS for n in range(0, gridX)]
                vy = [n*0 for n in range(0, gridX)]
                for k in range(0, len(vy)):
                    vy[k] = (self.py + math.tan(self.rayAngle/180.0*math.pi)*(vx[k]-self.px))

                #print(vx)
                #print(vy)

                hy = [n*blockS for n in range(0, gridY)]
                hx = [n*0 for n in range(0, gridY)]
                for k in range(len(hy)):
                    if (abs(self.rayAngle) < 0.001) or (abs(self.rayAngle-180) < 0.001):
                        hx[k] = 1000000
                    else:
                        hx[k] = (self.px + 1./math.tan(self.rayAngle/180.0*math.pi)*(hy[k]-self.py))

                #print(hx)
                #print(hy)

                delta = 0.001
                # vertical lines
                
                if (self.rayAngle < 90) or (self.rayAngle > 270):
                    for bx in range(bx1+1, gridX):
                        by = int((vy[bx]-delta) // blockS)
                        #print(bx, by)
                        if (by > -1) and (by < gridY):
                            if grid[by][bx][0] == 1:
                                #print(bx, by, '1')
                                break

                        byp = int((vy[bx]+delta) // blockS)
                        if (byp > -1) and (byp < gridY):
                            if grid[byp][bx][0] == 1:
                                by = byp
                                break

                else:
                    for bx in range(bx1, 0, -1):
                        by = int((vy[bx]+delta) // blockS)
                        #print(bx-1, by)
                        if (by > -1) and (by < gridY):
                            #print(grid[by][bx-1][0])
                            if grid[by][bx-1][0] == 1:
                                #print(bx, by, '1')
                                break

                        byp = int((vy[bx] - delta) // blockS)
                        if (byp > -1) and (byp < gridY):
                            if grid[byp][bx-1][0] == 1:
                                by = byp
                                break

                #print('V final', self.rayAngle, bx, by)

                if (by > -1) and (by < gridY):
                    verX = vx[bx]
                    verY = vy[bx]
                    #self.rx = vx[bx]
                    #self.ry = vy[bx]
                    #canvas.create_line(self.px, self.py, self.rx, self.ry, fill='red')
                else:
                    verX = -1
                    verY = -1


                # horizontal lines
                if (self.rayAngle < 180):
                    for by in range(by1+1, gridY):
                        bx = int((hx[by]-delta) // blockS)
                        if (bx > -1) and (bx < gridX):
                            if grid[by][bx][0] == 1:
                                break

                        bxp = int((hx[by]+delta) // blockS)
                        if (bxp > -1) and (bxp < gridX):
                            if grid[by][bxp][0] == 1:
                                bx = bxp
                                break
                else:
                    for by in range(by1,0,-1):
                        bx = int((hx[by]-delta) // blockS)
                        if (bx > -1) and (bx < gridX):
                            if grid[by-1][bx][0] == 1:
                                break

                        bxp = int((hx[by] + delta) // blockS)
                        if (bxp > -1) and (bxp < gridX):
                            if grid[by-1][bxp][0] == 1:
                                bx = bxp
                                break

                #print('H final', self.rayAngle, bx, by)

                if (bx > -1) and (bx < gridX):
                    #self.rx = hx[by]
                    #self.ry = hy[by]
                    #canvas.create_line(self.px, self.py, self.rx, self.ry, fill='blue')
                    horX = hx[by]
                    horY = hy[by]
                else:
                    horX = -1
                    horY = -1


                if verX < 0:
                    self.rx = horX
                    self.ry = horY
                elif horX < 0:
                    self.rx = verX
                    self.ry = verY
                else:
                    disH = ((self.px - horX) ** 2) + ((self.py - horY) ** 2)
                    disV = ((self.px - verX) ** 2) + ((self.py - verY) ** 2)
                    if disV < disH:
                    #if abs(self.px - verX) < abs(self.px - horX): 
                        self.rx = verX
                        self.ry = verY
                    else:
                        self.rx = horX
                        self.ry = horY

                
                self.rays[r] = canvas.create_line(self.px, self.py, self.rx, self.ry, fill='red')
                disT = math.sqrt((self.ry - self.py) ** 2 + (self.rx - self.px) ** 2)

                ca = self.angle - self.rayAngle
                if ca < 0:
                    ca += 360
                if ca > 360:
                    ca -= 360
                disT = disT*math.cos(math.radians(ca))
                lineH = (64 * 320) / disT
                if lineH > 512:
                    lineH = 512
                lineO = 256 - lineH/2
            if abs(self.rx - horX) < 0.00001 and abs(self.ry - horY) < 0.00001:
                self.walls[r] = canvas.create_line(r*8 + 530, lineO, r*8+530,lineH + lineO, fill='green', width=8)
            else:
                self.walls[r] = canvas.create_line(r*8 + 530, lineO, r*8 + 530, lineH + lineO, fill='red', width=8)

                    
            
                
gridX, gridY, blockS = 8, 8, 64
grid = [[[1],[1],[1],[1],[1],[1],[1],[1]],
       [[1],[0],[0],[0],[0],[0],[0],[1]],
       [[1],[0],[1],[0],[0],[1],[0],[1]],
       [[1],[0],[0],[0],[0],[0],[0],[1]],
       [[1],[0],[0],[0],[0],[0],[0],[1]],
       [[1],[0],[1],[0],[0],[1],[0],[1]],
       [[1],[0],[0],[0],[0],[0],[0],[1]],
       [[1],[1],[1],[1],[1],[1],[1],[1]]]


def drawGrid():
    px = blockS/2
    py = blockS/2
    for y in range(len(grid)):
        if y != 0:
            py += blockS
            px = blockS/2
        for x in range(len(grid[y])):
            if x != 0:
                px += blockS
            if grid[y][x] == [1]:
                canvas.create_rectangle(px - blockS/2 + 1, py - blockS/2 +1, px + blockS/2 -1, py + blockS/2 -1, fill='gray')
            else:
                pass
drawGrid()
player = Player()




#player.drawRays2()

flag = 1
while flag:
    player.move()
    tk.update()
    #flag = 0
    #break
    canvas.delete(player.line)
    for r in range(len(player.rays)):
        canvas.delete(player.rays[r])
        canvas.delete(player.walls[r])
    time.sleep(0.01)

