from vpython import *
import numpy as np
# canopy = None
# umbrella = compound([handle,canopy])

handle = None

def rotatePoint(vert,angle,color,center):  #= vertex(pos = vec(0,0,0))
    mx = np.asmatrix([  [1,0,0],
                        [0,cos(radians(angle.x)),-1*sin(radians(angle.x))],
                        [0,sin(radians(angle.x)),cos(radians(angle.x))]
                        ])
    my = np.asmatrix([  [cos(radians(angle.y)),0,sin(radians(angle.y))],
                        [0,1,0],
                        [-1*sin(radians(angle.y)),0,cos(radians(angle.y))]
                        ])
    mz = np.asmatrix([  [cos(radians(angle.z)),-1*sin(radians(angle.z)),0],
                        [sin(radians(angle.z)),cos(radians(angle.z)),0],
                        [0,0,1]
                        ])
    point = np.array(np.asmatrix([vert.pos.x-center.pos.x,vert.pos.y-center.pos.y,vert.pos.z-center.pos.z]) * mx * my * mz)
    vertexx = vertex(pos=vec(point[0][0]+center.pos.x,point[0][1]+center.pos.y,point[0][2]+center.pos.z),color = color)
    return vertexx


class Circle:
    def __init__(self,center,radius,n, color = vec(0.2,0.2,0.2)):
        self.vertexes = []
        self.triangles = []
        self.edges = []
        self.radius = radius
        self.center = center
        self.color = color
        self.n = n


    def count(self):
        if self.vertexes:
            for i,vert in enumerate(self.vertexes):
                angle = 2*pi*i/self.n
                vert.pos = vec( self.radius*cos(angle)+self.center.pos.x,
                                self.radius*sin(angle)+self.center.pos.y,
                                self.center.pos.z)
                vert.color = self.color
        else:
            for i in range(self.n):
                angle = 2*pi*i/self.n
                self.vertexes.append(vertex(pos=vec(self.radius*cos(angle)+self.center.pos.x,
                                                    self.radius*sin(angle)+self.center.pos.y,
                                                    self.center.pos.z),color = self.color))


    def color(self, vert):
        for i in range(len(self.vertexes)):
            self.vertexes[i].color = vert


    def fill(self):
        self.center.color = self.color
        # print(self.center.pos)
        if self.triangles:
            for i,triang in enumerate(self.triangles):
                triang.vs=[ self.center,
                            self.vertexes[i-1],
                            self.vertexes[i]]
        else:
            for i in range(len(self.vertexes)):
                self.triangles.append(triangle(vs=[self.center,
                                                   self.vertexes[i-1],
                                                   self.vertexes[i]]))

    def rotate(self,vector):
        self.center = rotatePoint(self.center,vector,self.color,self.center)
        for i,vertex in enumerate(self.vertexes):
            self.vertexes[i] = rotatePoint(vertex,vector,self.color,self.center)

    def attach(self,circle):
        n = min(len(self.vertexes), len(circle.vertexes))
        if self.edges:
            for i in range(len(self.edges)):
                self.edges[i].vs = [self.vertexes[i-1],self.vertexes[i],circle.vertexes[i],circle.vertexes[i-1]]
        else:
            for i in range(n):
                self.edges.append(quad(vs = [self.vertexes[i-1],self.vertexes[i],circle.vertexes[i],circle.vertexes[i-1]]))


    def transform(self, vert):
        self.center.pos.x += vert.pos.x
        self.center.pos.y += vert.pos.y
        self.center.pos.z += vert.pos.z
        self.count()

class EpiCycloid(Circle):
    def count(self,n):
        if self.vertexes:
            for i,vert in enumerate(self.vertexes):
                angle = 2*pi*i/self.n
                vert.pos = vec( self.radius*(n + 1)*(cos(angle)-cos((n + 1) * angle)/(n + 1))+self.center.pos.x,
                                self.radius*(n + 1)*(sin(angle)-sin((n + 1) * angle)/(n + 1))+self.center.pos.y,
                                self.center.pos.z)
                vert.color = self.color
        else:
            for i in range(self.n):
                angle = 2*pi*i/self.n
                self.vertexes.append(vertex(pos=vec(self.radius*(n + 1)*(cos(angle)-cos((n + 1) * angle)/(n + 1))+self.center.pos.x,
                                                    self.radius*(n + 1)*(sin(angle)-sin((n + 1) * angle)/(n + 1))+self.center.pos.y,
                                                    self.center.pos.z),color = self.color))

class HyperCycloid(Circle):
    def count(self,n):
        if self.vertexes:
            for i,vert in enumerate(self.vertexes):
                angle = 2*pi*i/self.n
                vert.pos = vec( self.radius*(n - 1)*(cos(angle)+cos((n - 1) * angle)/(n - 1))+self.center.pos.x,
                                self.radius*(n - 1)*(sin(angle)-sin((n - 1) * angle)/(n - 1))+self.center.pos.y,
                                self.center.pos.z)
                vert.color = self.color
        else:
            for i in range(self.n):
                angle = 2*pi*i/self.n
                self.vertexes.append(vertex(pos=vec(self.radius*(n - 1)*(cos(angle)+cos((n - 1) * angle)/(n - 1))+self.center.pos.x,
                                                    self.radius*(n - 1)*(sin(angle)-sin((n - 1) * angle)/(n - 1))+self.center.pos.y,
                                                    self.center.pos.z),color = self.color))

flower = []
base2 = []
base = []
for i in range(10):
    base.append(HyperCycloid(vertex(pos = vec(0,0,0)), 5, 24, vec((i+1)/20,(i+1)/10,(10-i+1)/10)))
    base2.append(Circle(vertex(pos = vec(0,0,-0.1)), 5, 24, vec(1,0.4,0.1)))

base2[len(base2) - 1].fill()

for i in range(5):
    flower.append(EpiCycloid(vertex(pos = vec(0,0,5 + i * 10)), 5 + i, 24, vec(i/4,(1-i/4),0)))
    flower[i].count(5)

for i in range(5):
    flower.append(EpiCycloid(vertex(pos = vec(0,0,45 - i * 2)), 9 + i / 5, 24, vec(1,i/4,i/4)))
    flower[i+5].count(5)

base[0].count(5)
base2[0].count()
base2[0].attach(base[0])
base[0].fill()
# test.attach(test2)
base[0].attach(flower[0])

for i in range(9):
    flower[i].attach(flower[i+1])

def testanimation():
    for delta in range(100):
        rate(60)
        scene.waitfor('redraw')
        for i, epi in enumerate(flower):
            flower[i].radius -= i / 100
            flower[i].center.pos -= vec(0, 0, i*30 / 300)
            flower[i].count(5)

        for i, circ in enumerate(base2):
            base2[i].center.pos -= vec(0, 0, i / 7)
            base2[i].count()

        for i, hyp in enumerate(base):
            base[i].radius -= 5*(i - 3) / 600
            if i < 3:
                base[i].radius += 2*i / 100
            base[i].center.pos += vec(0, 0, i/5)
            if i >= 3:
                base[i].center.pos += vec(0, 0, i/5)
            base[i].count(5)

        for i, epi in enumerate(flower):
            if i != len(flower) - 1:
                flower[i].attach(flower[i+1])

        for i, circ in enumerate(base2):
            if i != len(base2) - 1:
                base2[len(base2) - i - 1].attach(base2[len(base2) - i - 2])

        for i, hyp in enumerate(base):
            if i != len(base) - 1:
                base[len(base) - i - 1].attach(base[len(base) - i - 2])
        scene.background += vec(0.01,0,0)
def anim2():
    for delta in range(100):
        for i, epi in enumerate(flower):
            flower[i].radius += i / 100
            flower[i].center.pos += vec(0, 0, i*30 / 300)
            flower[i].count(5)

        for i, hyp in enumerate(base):
            base[i].radius += 5*(i - 3) / 600
            if i < 3:
                base[i].radius -= 2*i / 100
            base[i].center.pos -= vec(0, 0, i/5)
            if i >= 3:
                base[i].center.pos -= vec(0, 0, i/5)
            base[i].count(5)

        for i, circ in enumerate(base2):
            base2[i].center.pos += vec(0, 0, i / 7)
            base2[i].count()

        for i, epi in enumerate(flower):
            if i != len(flower) - 1:
                flower[i].attach(flower[i+1])

        for i, circ in enumerate(base2):
            if i != len(base2) - 1:
                base2[len(base2) - i - 1].attach(base2[len(base2) - i - 2])

        for i, hyp in enumerate(base):
            if i != len(base) - 1:
                base[len(base) - i - 1].attach(base[len(base) - i - 2])
        scene.background -= vec(0.01,0,0)


cbutton1 = button(text='<b>Lance</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=testanimation, bottom=5)
cbutton2 = button(text='<b>Mold</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=anim2, bottom=5)

scene.width = 900
scene.height = 900
scene.background = vec(0, 0.47, 0.77)
