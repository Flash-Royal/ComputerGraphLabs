from vpython import *
import numpy as np
from copy import deepcopy

def rotatePoint(vert,angle,color,center):  #= vertex(pos = vec(0,0,0))
    mx = np.asmatrix([  [1,0,0],
                        [0,cos(radians(angle.pos.x)),-1*sin(radians(angle.pos.x))],
                        [0,sin(radians(angle.pos.x)),cos(radians(angle.pos.x))]
                        ])
    my = np.asmatrix([  [cos(radians(angle.pos.y)),0,sin(radians(angle.pos.y))],
                        [0,1,0],
                        [-1*sin(radians(angle.pos.y)),0,cos(radians(angle.pos.y))]
                        ])
    mz = np.asmatrix([  [cos(radians(angle.pos.z)),-1*sin(radians(angle.pos.z)),0],
                        [sin(radians(angle.pos.z)),cos(radians(angle.pos.z)),0],
                        [0,0,1]
                        ])
    point = np.array(np.asmatrix([vert.pos.x-center.pos.x,vert.pos.y-center.pos.y,vert.pos.z-center.pos.z]) * mx * my * mz)
    vertexx = vertex(pos=vec(point[0][0]+center.pos.x,point[0][1]+center.pos.y,point[0][2]+center.pos.z),color = color)
    return vertexx

class Rect3d:
    def __init__(self, center, length, width, height, color = [vec(0.2,0.2,0.2), vec(0.2,0.2,0.2)]):
        self.vertexes = []
        self.quads = []
        self.height = height
        self.center = center
        self.length = length
        self.width = width
        self.color = color
        self.angleCenter = vertex(pos = vec(0, 0, 0))
        self.angleAxis = vertex(pos = vec(0, 0, 0))
        self.centerAxis = self.center

    def cpRotate(self):
        center = rotatePoint(self.center,self.angleCenter,self.center.color,self.center)
        center = rotatePoint(center,self.angleAxis,self.center.color,self.centerAxis)
        return center

    def startPoint2(self):
        return vertex(pos = vec(self.center.pos.x - self.length / 2, self.center.pos.y, self.center.pos.z - self.width / 2), color = self.color[0])

    def initPoints(self):
        startPoint = self.startPoint2()
        if self.vertexes:
            self.vertexes[0] = startPoint
            self.vertexes[1] = vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y, startPoint.pos.z))
            self.vertexes[2] = vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y, startPoint.pos.z + self.width))
            self.vertexes[3] = vertex(pos = vec(startPoint.pos.x, startPoint.pos.y, startPoint.pos.z + self.width))
            self.vertexes[4] = vertex(pos = vec(startPoint.pos.x, startPoint.pos.y + self.height, startPoint.pos.z))
            self.vertexes[5] = vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y + self.height, startPoint.pos.z))
            self.vertexes[6] = vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y + self.height, startPoint.pos.z + self.width))
            self.vertexes[7] = vertex(pos = vec(startPoint.pos.x, startPoint.pos.y + self.height, startPoint.pos.z + self.width))
            self.setColor(self.color)
            self.rotateCenter()
        else:
            self.vertexes.append(startPoint)
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y, startPoint.pos.z)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y, startPoint.pos.z + self.width)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x, startPoint.pos.y, startPoint.pos.z + self.width)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x, startPoint.pos.y + self.height, startPoint.pos.z)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y + self.height, startPoint.pos.z)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x + self.length, startPoint.pos.y + self.height, startPoint.pos.z + self.width)))
            self.vertexes.append(vertex(pos = vec(startPoint.pos.x, startPoint.pos.y + self.height, startPoint.pos.z + self.width)))
            self.setColor(self.color)
            self.rotateCenter()

    def refill(self):
        if self.quads:
            self.quads[0].vs = [self.vertexes[0], self.vertexes[1], self.vertexes[2], self.vertexes[3]]
            self.quads[1].vs = [self.vertexes[0], self.vertexes[1], self.vertexes[5], self.vertexes[4]]
            self.quads[2].vs = [self.vertexes[0], self.vertexes[3], self.vertexes[7], self.vertexes[4]]
            self.quads[3].vs = [self.vertexes[2], self.vertexes[1], self.vertexes[5], self.vertexes[6]]
            self.quads[4].vs = [self.vertexes[2], self.vertexes[3], self.vertexes[7], self.vertexes[6]]
            self.quads[5].vs = [self.vertexes[4], self.vertexes[5], self.vertexes[6], self.vertexes[7]]
        else:
            self.quads.append(quad(vs = [self.vertexes[0], self.vertexes[1], self.vertexes[2], self.vertexes[3]]))
            self.quads.append(quad(vs = [self.vertexes[0], self.vertexes[1], self.vertexes[5], self.vertexes[4]]))
            self.quads.append(quad(vs = [self.vertexes[0], self.vertexes[3], self.vertexes[7], self.vertexes[4]]))
            self.quads.append(quad(vs = [self.vertexes[2], self.vertexes[1], self.vertexes[5], self.vertexes[6]]))
            self.quads.append(quad(vs = [self.vertexes[2], self.vertexes[3], self.vertexes[7], self.vertexes[6]]))
            self.quads.append(quad(vs = [self.vertexes[4], self.vertexes[5], self.vertexes[6], self.vertexes[7]]))

    def fill(self):
        self.initPoints()
        self.refill()

    def changeParams(self, center, length, width, height):
        self.height = height
        self.center = center
        self.length = length
        self.width = width

        self.fill()

    def resize(self, height):
        self.height += height
        self.fill()

    def setColor(self, color):
        self.color = color
        for i, el in enumerate(self.vertexes):
            el.color = self.color[0 if i % 4 < 2 else 1]

    def rotateCenter(self):
        for i,el in enumerate(self.vertexes):
            self.vertexes[i] = rotatePoint(el,self.angleCenter,self.vertexes[i].color,self.center)
        for i,el in enumerate(self.vertexes):
            self.vertexes[i] = rotatePoint(el,self.angleAxis,self.vertexes[i].color,self.centerAxis)
        self.refill()

    def rotateSelf(self, vector):
        #self.center = rotatePoint(self.center,vector,self.center.color,self.center)
        self.angleCenter = vertex(pos = vec(self.angleCenter.pos.x + vector.pos.x, self.angleCenter.pos.y + vector.pos.y, self.angleCenter.pos.z + vector.pos.z))
        self.fill()

    def rotate(self, vector, center):
        #self.center = rotatePoint(self.center,vector,self.center.color,self.center)
        self.angleAxis = vertex(pos = vec(self.angleAxis.pos.x + vector.pos.x, self.angleAxis.pos.y + vector.pos.y, self.angleAxis.pos.z + vector.pos.z))
        self.centerAxis = center
        self.fill()

    # def rotateSelf(self, vector):
    #     #self.center = rotatePoint(self.center,vector,self.center.color,self.center)
    #     self.angleCenter = vertex(pos = vec((self.angleCenter.pos.x + vector.pos.x) % 360, (self.angleCenter.pos.y + vector.pos.y) % 360, (self.angleCenter.pos.z + vector.pos.z) % 360))
    #     # for i,el in enumerate(self.vertexes):
    #     #     self.vertexes[i] = rotatePoint(el,vector,self.vertexes[i].color,self.center)
    #     # self.refill()
    #
    # def rotate(self, vector, center):
    #     #self.center = rotatePoint(self.center,vector,self.center.color,self.center)
    #     self.angleAxis = vertex(pos = vec((self.angleAxis.pos.x + vector.pos.x) % 360, (self.angleAxis.pos.y + vector.pos.y) % 360, (self.angleAxis.pos.z + vector.pos.z) % 360))
    #     # self.centerAxis = center
    #     # for i,el in enumerate(self.vertexes):
    #     #     self.vertexes[i] = rotatePoint(el,vector,self.vertexes[i].color,self.centerAxis)
    #     # self.refill()

    def transform(self, vert):
        # print(vert.pos)
        self.center.pos.x += vert.pos.x
        self.center.pos.y += vert.pos.y
        self.center.pos.z += vert.pos.z
        # for i, el in enumerate(self.vertexes):
        #     self.vertexes[i].pos = vec(self.vertexes[i].pos.x + vert.pos.x, self.vertexes[i].pos.y + vert.pos.y, self.vertexes[i].pos.z + vert.pos.z)
        self.fill()

    def transform2(self, vert):
        # print(vert.pos)
        self.center.pos.x += vert.pos.x
        self.center.pos.y += vert.pos.y
        self.center.pos.z += vert.pos.z
        for i, el in enumerate(self.vertexes):
            self.vertexes[i].pos = vec(self.vertexes[i].pos.x + vert.pos.x, self.vertexes[i].pos.y + vert.pos.y, self.vertexes[i].pos.z + vert.pos.z)
        # self.fill()

    def vertexAdd(self, vert):
        return vertex(pos = vec(self.center.pos.x + vert.pos.x, self.center.pos.y + vert.pos.y, self.center.pos.z + vert.pos.z))

    def getRet(self):
        return Rect3d(self.center, self.length, self.width, self.height, self.color)

    def __str__(self):
        return f'Rec(height = {self.height}, width = {self.width}, length = {self.length}, angleCenter(x = {self.angleCenter.pos.x}, y = {self.angleCenter.pos.y}, z = {self.angleCenter.pos.z}), angleAxis(x = {self.angleAxis.pos.x}, y = {self.angleAxis.pos.y}, z = {self.angleAxis.pos.z}))'

class Axis():
    def __init__(self, length, width, height, center = vertex(pos = vec(0, 0, 0))):
        self.length = length
        self.width = width
        self.height = height
        self.center = center
        self.e = 0.05
        self.sp11 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp12 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp23 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp34 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp41 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp42 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp53 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp64 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp71 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp72 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp83 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        self.sp94 = sphere(pos = center.pos, radius = self.e, color = vec(1, 0, 0))
        # self.rec1 = Rect3d(center, 0, 0, 0, color = [vec(0, 1, 0), vec(0, 1, 0)])
        # self.rec2 = Rect3d(center, 0, 0, 0, color = [vec(0, 1, 0), vec(0, 1, 0)])
        # self.rec3 = Rect3d(center, 0, 0, 0, color = [vec(0, 1, 0), vec(0, 1, 0)])
        self.sq1 = quad(vs = [center, center, center, center])
        self.sq2 = quad(vs = [center, center, center, center])
        self.sq3 = quad(vs = [center, center, center, center])
        self.sq4 = quad(vs = [center, center, center, center])
        self.sq5 = quad(vs = [center, center, center, center])
        self.sq6 = quad(vs = [center, center, center, center])
        self.sq7 = quad(vs = [center, center, center, center])
        self.sq8 = quad(vs = [center, center, center, center])
        self.sq9 = quad(vs = [center, center, center, center])

    def initAxis(self):
        rectX = Rect3d(self.center, 100, self.e, self.e, color = [vec(1,1,1), vec(1,1,1)])
        rectZ = Rect3d(self.center, self.e, 100, self.e, color = [vec(1,1,1), vec(1,1,1)])
        rectY = Rect3d(self.center, self.e, self.e, 100, color = [vec(1,1,1), vec(1,1,1)])

        rectX.fill()
        rectY.fill()
        rectZ.fill()

    def lengthPoint(self, p1, p2):
        lenX = sqrt((p2.pos.y - p1.pos.y)*(p2.pos.y - p1.pos.y) + (p2.pos.z - p1.pos.z)*(p2.pos.z - p1.pos.z))
        lenY = sqrt((p2.pos.z - p1.pos.z)*(p2.pos.z - p1.pos.z) + (p2.pos.x - p1.pos.x)*(p2.pos.x - p1.pos.x))
        lenZ = sqrt((p2.pos.y - p1.pos.y)*(p2.pos.y - p1.pos.y) + (p2.pos.x - p1.pos.x)*(p2.pos.x - p1.pos.x))
        return lenX, lenY, lenZ

    def anglePoint(self, p1, p2):
        lenX, lenY, lenZ = self.lengthPoint(p1, p2)
        angleX = lenX if lenX == 0 else degrees(acos((p2.pos.y - p1.pos.y) / lenX))
        angleY = lenY if lenY == 0 else degrees(acos((p2.pos.z - p1.pos.z) / lenY))
        angleZ = lenZ if lenZ == 0 else degrees(acos((p2.pos.x - p1.pos.x) / lenZ))
        return angleX, angleY, angleZ

    def XZProection(self, p1, p2, p3, p4):
        p1.pos = vec(p1.pos.x, 0, p1.pos.z)
        p2.pos = vec(p2.pos.x, 0, p2.pos.z)
        p3.pos = vec(p3.pos.x, 0, p3.pos.z)
        p4.pos = vec(p4.pos.x, 0, p4.pos.z)

        # lenX1, lenY1, lenZ1 = self.lengthPoint(p1, p2)
        # print(lenX1, lenY1, lenZ1)
        # angleX1, angleY1, angleZ1 = self.anglePoint(p1, p2)
        # print(angleX1, angleY1, angleZ1)
        # # rec1 = Rect3d(p1, self.e, self.e, lenY1, color = [vec(0, 1, 0), vec(0, 1, 0)])
        # self.rec1.changeParams(p1, self.e, lenY1, self.e)
        # self.rec1.angleCenter.pos = vec(0, 0, 0)
        # self.rec1.fill()
        self.sp11.pos = p1.pos
        self.sp12.pos = p2.pos
        self.sp23.pos = p3.pos
        self.sp34.pos = p4.pos

        self.sq1.vs = [vertex(pos = vec(p1.pos.x, self.e, p1.pos.z), color = vec(0,1,0)), vertex(pos = vec(p1.pos.x, -self.e, p1.pos.z), color = vec(0,1,0)), vertex(pos = vec(p2.pos.x, -self.e, p2.pos.z), color = vec(0,1,0)),vertex(pos = vec(p2.pos.x, self.e, p2.pos.z), color = vec(0,1,0))]
        self.sq2.vs = [vertex(pos = vec(p3.pos.x, self.e, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(p3.pos.x, -self.e, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(p2.pos.x, -self.e, p2.pos.z), color = vec(0,1,0)),vertex(pos = vec(p2.pos.x, self.e, p2.pos.z), color = vec(0,1,0))]
        self.sq3.vs = [vertex(pos = vec(p3.pos.x, self.e, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(p3.pos.x, -self.e, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(p4.pos.x, -self.e, p4.pos.z), color = vec(0,1,0)),vertex(pos = vec(p4.pos.x, self.e, p4.pos.z), color = vec(0,1,0))]

        # lenX2, lenY2, lenZ2 = self.lengthPoint(p2, p3)
        # print(lenX2, lenY2, lenZ2)
        # angleX2, angleY2, angleZ2 = self.anglePoint(p2, p3)
        # print(angleX2, angleY2, angleZ2)
        # # self.rec2 = Rect3d(p2, self.e, self.e, lenY2, color = [vec(0, 1, 0), vec(0, 1, 0)])
        # self.rec2.changeParams(p2, self.e, lenY2, self.e)
        # self.rec2.angleCenter.pos = vec(0, 0, 0)
        # self.rec2.fill()


        # _, lenY3, _ = self.lengthPoint(p3, p4)
        # angleX3, angleY3, angleZ3 = self.anglePoint(p3, p4)
        # # rec3 = Rect3d(p3, self.e, self.e, lenY3, color = [vec(0, 1, 0), vec(0, 1, 0)])
        # self.rec3.changeParams(p3, self.e, lenY3, self.e)
        # self.rec3.angleCenter.pos = vec(angleY3, 0, 0)
        # self.rec3.fill()



    def YXProection(self, p1, p2, p3, p4):
        p1.pos = vec(p1.pos.x, p1.pos.y, 0)
        p2.pos = vec(p2.pos.x, p2.pos.y, 0)
        p3.pos = vec(p3.pos.x, p3.pos.y, 0)
        p4.pos = vec(p4.pos.x, p4.pos.y, 0)

        self.sp41.pos = p1.pos
        self.sp42.pos = p2.pos
        self.sp53.pos = p3.pos
        self.sp64.pos = p4.pos

        self.sq4.vs = [vertex(pos = vec(p1.pos.x, p1.pos.y, self.e), color = vec(0,1,0)), vertex(pos = vec(p1.pos.x, p1.pos.y, -self.e), color = vec(0,1,0)), vertex(pos = vec(p2.pos.x, p2.pos.y, -self.e), color = vec(0,1,0)),vertex(pos = vec(p2.pos.x, p2.pos.y, self.e), color = vec(0,1,0))]
        self.sq5.vs = [vertex(pos = vec(p3.pos.x, p3.pos.y, self.e), color = vec(0,1,0)), vertex(pos = vec(p3.pos.x, p3.pos.y, -self.e), color = vec(0,1,0)), vertex(pos = vec(p2.pos.x, p2.pos.y, -self.e), color = vec(0,1,0)),vertex(pos = vec(p2.pos.x, p2.pos.y, self.e), color = vec(0,1,0))]
        self.sq6.vs = [vertex(pos = vec(p3.pos.x, p3.pos.y, self.e), color = vec(0,1,0)), vertex(pos = vec(p3.pos.x, p3.pos.y, -self.e), color = vec(0,1,0)), vertex(pos = vec(p4.pos.x, p4.pos.y, -self.e), color = vec(0,1,0)),vertex(pos = vec(p4.pos.x, p4.pos.y, self.e), color = vec(0,1,0))]


    def YZProection(self, p1, p2, p3, p4):
        p1.pos = vec(0, p1.pos.y, p1.pos.z)
        p2.pos = vec(0, p2.pos.y, p2.pos.z)
        p3.pos = vec(0, p3.pos.y, p3.pos.z)
        p4.pos = vec(0, p4.pos.y, p4.pos.z)

        self.sp71.pos = p1.pos
        self.sp72.pos = p2.pos
        self.sp83.pos = p3.pos
        self.sp94.pos = p4.pos

        self.sq7.vs = [vertex(pos = vec(self.e, p1.pos.y, p1.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p1.pos.y, p1.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p2.pos.y, p2.pos.z), color = vec(0,1,0)),vertex(pos = vec(self.e, p2.pos.y, p2.pos.z), color = vec(0,1,0))]
        self.sq8.vs = [vertex(pos = vec(self.e, p3.pos.y, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p3.pos.y, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p2.pos.y, p2.pos.z), color = vec(0,1,0)),vertex(pos = vec(self.e, p2.pos.y, p2.pos.z), color = vec(0,1,0))]
        self.sq9.vs = [vertex(pos = vec(self.e, p3.pos.y, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p3.pos.y, p3.pos.z), color = vec(0,1,0)), vertex(pos = vec(-self.e, p4.pos.y, p4.pos.z), color = vec(0,1,0)),vertex(pos = vec(self.e, p4.pos.y, p4.pos.z), color = vec(0,1,0))]



class Crane():
    def __init__(self):
        self.leg = []
        self.arm = []
        self.hand = []
        self.legH = 0
        self.armH = 0
        self.handH = 0
        self.legdH = 1
        self.armdH = 1
        self.handdH = 1
        self.legAngle = 0
        self.armAngle = 0
        self.centersIndexes = []
        self.angle1 = vertex(pos = vec(0, 45, 0))
        self.angle2 = vertex(pos = vec(45, 0, 0))
        self.center = vertex(pos = vec(0, 0, 0))
        self.axis = Axis(100, 100, 100)
        self.legHUp = None
        self.legHDown = None
        self.armHUp = None
        self.armHDown = None
        self.handHUp = None
        self.handHDown = None
        self.winputLegH = None
        self.winputArmH = None
        self.winputHandH = None
        self.legAngleUp = None
        self.legAngleDown = None
        self.armAngleUp = None
        self.legAngleDown = None
        self.winputLegAngle = None
        self.winputArmAngle = None
        self.cbRotateArm = None
        self.cbRotateLeg = None

    def initParts(self):
        self.axis.initAxis()
        center = vertex(pos = vec(0, 0, 0))
        color = [vec(1, 0, 0), vec(0, 0, 1)]
        color2 = [vec(0, 1, 0), vec(1, 0, 1)]
        rec = Rect3d(vertex(pos = vec(5,0,5)), 1, 1, 4, color = color)
        rec.fill()
        self.leg.append(rec)
        rec2 = Rect3d(rec.vertexAdd(vertex(pos = vec(0, rec.height, 0))), 0.25, 0.25, 1, color = color)
        rec2.fill()
        self.leg.append(rec2)
        rec3 = Rect3d(rec2.vertexAdd(vertex(pos = vec(0, rec2.height, 0))), 0.5, 0.5, 0.5, color = color)
        rec3.fill()
        self.leg.append(rec3)
        self.centersIndexes.append(2)
        rec4 = Rect3d(rec3.vertexAdd(vertex(pos = vec(rec3.width / 2, rec3.height / 2, 0))), 0.25, 0.25, 1, color = color)
        rec4.fill()
        rec4.rotateSelf(vertex(pos = vec(0, 0, 90)))
        self.arm.append(rec4)
        self.centersIndexes.append(0)
        rec5 = Rect3d(rec4.vertexAdd(vertex(pos = vec(rec4.height, 0, 0))), 1, 1, 4, color = color)
        rec5.fill()
        rec5.rotateSelf(vertex(pos = vec(0, 0, 90)))
        self.arm.append(rec5)
        rec6 = Rect3d(rec5.vertexAdd(vertex(pos = vec(rec5.height, 0, 0))),  0.25, 0.25, 1, color = color)
        rec6.fill()
        rec6.rotateSelf(vertex(pos = vec(0, 0, 90)))
        self.arm.append(rec6)
        rec7 = Rect3d(rec6.vertexAdd(vertex(pos = vec(rec6.height, 0, 0))), 0.5, 0.5, 0.5, color = color)
        rec7.fill()
        rec7.rotateSelf(vertex(pos = vec(0, 0, 90)))
        self.arm.append(rec7)
        self.centersIndexes.append(3)
        rec8 = Rect3d(rec7.vertexAdd(vertex(pos = vec(rec7.width / 2, -rec7.width / 2, 0))), 0.25, 0.25, 1, color = color)
        rec8.fill()
        rec8.rotateSelf(vertex(pos = vec(0, 0, 180)))
        self.hand.append(rec8)
        rec9 = Rect3d(rec8.vertexAdd(vertex(pos = vec(0, -rec8.height, 0))), 1, 1, 1.5, color)
        rec9.fill()
        rec9.rotateSelf(vertex(pos = vec(0, 0, 180)))
        self.hand.append(rec9)
        rec10 = Rect3d(rec9.vertexAdd(vertex(pos = vec(0, -rec9.height, 0))), 0.25, 0.25, 0.5, color = color)
        rec10.fill()
        rec10.rotateSelf(vertex(pos = vec(0, 0, 180)))
        self.hand.append(rec10)
        rec11 = Rect3d(rec10.vertexAdd(vertex(pos = vec(0, -rec10.height, 0))), 0.5, 0.5, 0.5, color = color)
        rec11.fill()
        rec11.rotateSelf(vertex(pos = vec(0, 0, 180)))
        self.hand.append(rec11)
        self.getHs()
        self.proection()

    def getHs(self):
        self.legH = self.leg[0].height
        self.armH = self.arm[1].height
        self.handH = self.hand[1].height
        if self.legHDown is not None:
            if self.legdH > self.legH:
                self.legHDown.disabled = True
            else:
                self.legHDown.disabled = False
        if self.armHDown is not None:
            if self.armdH > self.armH:
                self.armHDown.disabled = True
            else:
                self.armHDown.disabled = False

        if self.handHDown is not None:
            if self.handdH > self.handH:
                self.handHDown.disabled = True
            else:
                self.handHDown.disabled = False

    def proection(self):
        p1 = self.leg[0].cpRotate()
        p2 = self.newCenter(self.leg[2].cpRotate(), self.leg[self.centersIndexes[0]].height)
        p3 = self.newCenter(self.arm[3].cpRotate(), self.arm[3].height)
        p4 = self.newCenter(self.hand[3].cpRotate(), -self.hand[3].height)
        self.axis.YZProection(p1,p2,p3,p4)
        p1 = self.leg[0].cpRotate()
        p2 = self.newCenter(self.leg[2].cpRotate(), self.leg[self.centersIndexes[0]].height)
        p3 = self.newCenter(self.arm[3].cpRotate(), self.arm[3].height)
        p4 = self.newCenter(self.hand[3].cpRotate(), -self.hand[3].height)
        self.axis.YXProection(p1,p2,p3,p4)
        p1 = self.leg[0].cpRotate()
        p2 = self.newCenter(self.leg[2].cpRotate(), self.leg[self.centersIndexes[0]].height)
        p3 = self.newCenter(self.arm[3].cpRotate(), self.arm[3].height)
        p4 = self.newCenter(self.hand[3].cpRotate(), -self.hand[3].height)
        self.axis.XZProection(p1,p2,p3,p4)

    def newCenter(self, center, height):
        return vertex(pos = vec(center.pos.x, center.pos.y + height / 2, center.pos.z))

    def rotateLegUp(self):
        # print(f'x = {self.leg[self.centersIndexes[0]].center.pos.x}, y = {self.leg[self.centersIndexes[0]].center.pos.y}, z = {self.leg[self.centersIndexes[0]].center.pos.z}')
        for i, el in enumerate(self.leg):
            self.leg[i].rotate(self.angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        for i, el in enumerate(self.arm):
            self.arm[i].rotate(self.angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        for i, el in enumerate(self.hand):
            self.hand[i].rotate(self.angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        self.proection()

    def rotateLegDown(self):
        # print(f'x = {self.leg[self.centersIndexes[0]].center.pos.x}, y = {self.leg[self.centersIndexes[0]].center.pos.y}, z = {self.leg[self.centersIndexes[0]].center.pos.z}')
        angle1 = self.angle1
        angle1.pos.y = -angle1.pos.y

        for i, el in enumerate(self.leg):
            self.leg[i].rotate(angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        for i, el in enumerate(self.arm):
            self.arm[i].rotate(angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        for i, el in enumerate(self.hand):
            self.hand[i].rotate(angle1, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        self.proection()

    def rotateArmUp(self):
        # print(f'x = {self.arm[self.centersIndexes[1]].center.pos.x}, y = {self.arm[self.centersIndexes[1]].center.pos.y}, z = {self.arm[self.centersIndexes[0]].center.pos.z}')
        for i, el in enumerate(self.arm):
            self.arm[i].rotateSelf(self.angle1)
        for i, el in enumerate(self.hand):
            self.hand[i].rotate(self.angle2, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        self.proection()

    def rotateArmDown(self):
        # print(f'x = {self.arm[self.centersIndexes[1]].center.pos.x}, y = {self.arm[self.centersIndexes[1]].center.pos.y}, z = {self.arm[self.centersIndexes[0]].center.pos.z}')
        angle1 = self.angle1
        angle1.pos.y = -angle1.pos.y
        angle2 = self.angle2
        angle2.pos.x = -angle2.pos.x
        for i, el in enumerate(self.arm):
            self.arm[i].rotateSelf(angle1)
        for i, el in enumerate(self.hand):
            self.hand[i].rotate(angle2, self.newCenter(self.leg[self.centersIndexes[0]].center, self.leg[self.centersIndexes[0]].height))
        self.proection()

    def resizeLegUp(self, b):
        self.leg[0].resize(self.legdH)
        self.getHs()
        for i, el in enumerate(self.leg):
            if i > 0:
                self.leg[i].transform(vertex(pos = vec(0, self.legdH, 0)))
        for i, el in enumerate(self.arm):
            self.arm[i].transform(vertex(pos = vec(0, self.legdH, 0)))

        for i, el in enumerate(self.hand):
            self.hand[i].transform2(vertex(pos = vec(0, self.legdH, 0)))
        # self.proection()

    def resizeLegDown(self, b):
        self.leg[0].resize(-self.legdH)
        self.getHs()
        for i, el in enumerate(self.leg):
            if i > 0:
                self.leg[i].transform(vertex(pos = vec(0, -self.legdH, 0)))
        for i, el in enumerate(self.arm):
            self.arm[i].transform(vertex(pos = vec(0, -self.legdH, 0)))

        for i, el in enumerate(self.hand):
            self.hand[i].transform2(vertex(pos = vec(0, -self.legdH, 0)))
        # self.proection()

    def resizeArmUp(self, b):
        self.arm[1].resize(self.armdH)
        self.getHs()
        for i, el in enumerate(self.arm):
            if i > 1:
                self.arm[i].transform(vertex(pos = vec(self.armdH, 0, 0)))

        for i, el in enumerate(self.hand):
            self.hand[i].transform(vertex(pos = vec(self.armdH, 0, 0)))
        self.proection()

    def resizeArmDown(self, b):
        if self.armH - self.armdH < 0:
            b.disabled = True
        else:
            self.arm[1].resize(-self.armdH)
            self.getHs()
            for i, el in enumerate(self.arm):
                if i > 1:
                    self.arm[i].transform(vertex(pos = vec(-self.armdH, 0, 0)))

            for i, el in enumerate(self.hand):
                self.hand[i].transform(vertex(pos = vec(-self.armdH, 0, 0)))
            self.proection()

    def resizeHandUp(self, b):
        self.hand[1].resize(self.handdH)
        self.getHs()
        for i, el in enumerate(self.hand):
            if i > 1:
                self.hand[i].transform(vertex(pos = vec(0, -self.handdH, 0)))
        self.proection()

    def resizeHandDown(self, b):
        self.hand[1].resize(-self.handdH)
        self.getHs()
        for i, el in enumerate(self.hand):
            if i > 1:
                self.hand[i].transform(vertex(pos = vec(0, self.handdH, 0)))
        self.proection()

    def legHInput(self, s):
        if s.number is None or ( s.number > 5 or  s.number < 1):
            s.text = self.legdH
        else:
            try:
                self.legdH = int(s.number)
                if self.legdH > self.legH:
                    self.legHDown.disabled = True
                else:
                    self.legHDown.disabled = False
            except:
                s.text = self.legdH

    def armHInput(self, s):
        if s.number is None or ( s.number > 5 or  s.number < 1):
            s.text = self.armdH
        else:
            try:
                self.armdH = int(s.number)
                if self.armdH > self.armH:
                    self.armHDown.disabled = True
                else:
                    self.armHDown.disabled = False
            except:
                s.text = self.armdH

    def handHInput(self, s):
        if s.number is None or ( s.number > 5 or  s.number < 1):
            s.text = self.handdH
        else:
            try:
                self.handdH = int(s.number)
                if self.handdH > self.handH:
                    self.handHDown.disabled = True
                else:
                    self.handHDown.disabled = False
            except:
                s.text = self.handdH

    def legAngleInput(self, s):
        if s.number is None or ( s.number > 180 or  s.number < -180):
            s.text = self.angle1.pos.y
        else:
            try:
                self.angle1.pos.y = int(s.number)
            except:
                s.text = self.angle1.pos.y

    def armAngleInput(self, s):
        if s.number is None or ( s.number > 180 or  s.number < -180):
            s.text = self.angle2.pos.x
        else:
            try:
                self.angle2.pos.x = int(s.number)
            except:
                s.text = self.angle2.pos.x

    def autoRotateLeg(self, b):
        while b.checked:
            self.rotateLegUp()

    def autoRotateArm(self, b):
        while b.checked:
            self.rotateArmUp()

    def initInterface(self):
        self.legHUp = button(text='<b>LegH+</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeLegUp, bottom=3)
        scene.append_to_caption('  ')
        self.legHDown = button(text='<b>LegH-</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeLegDown, bottom=3)
        scene.append_to_caption('  ')
        self.armHUp = button(text='<b>ArmH+</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeArmUp, bottom=3)
        scene.append_to_caption('  ')
        self.armHDown = button(text='<b>ArmH-</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeArmDown, bottom=3)
        scene.append_to_caption('  ')
        self.handHUp = button(text='<b>HandH+</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeHandUp, bottom=3)
        scene.append_to_caption('  ')
        self.handHDown = button(text='<b>HandH-</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.resizeHandDown, bottom=3)
        scene.append_to_caption('  ')
        self.legAngleUp = button(text='<b>LegAngle+</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.rotateLegUp, bottom=3)
        scene.append_to_caption('  ')
        self.legAngleDown = button(text='<b>LegAngle-</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.rotateLegDown, bottom=3)
        scene.append_to_caption('  ')
        self.armAngleUp = button(text='<b>ArmAngle+</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.rotateArmUp, bottom=3)
        scene.append_to_caption('  ')
        self.legAngleDown = button(text='<b>ArmAngle-</b>', color=color.red, background=color.cyan, pos=scene.title_anchor, bind=self.rotateArmDown, bottom=3)

        scene.append_to_caption('\n')
        self.winputLegH = winput(pos=scene.caption_anchor, bind = self.legHInput, text = f"{self.legdH}")
        scene.append_to_caption(' Change LegHValue\n')
        self.winputArmH = winput(pos=scene.caption_anchor, bind = self.armHInput, text = f"{self.armdH}")
        scene.append_to_caption(' Change ArmHValue\n')
        self.winputHandH = winput(pos=scene.caption_anchor, bind = self.handHInput, text = f"{self.handdH}")
        scene.append_to_caption(' Change HandHValue\n')
        self.winputLegAngle = winput(pos=scene.caption_anchor, bind = self.legAngleInput, text = f"{self.angle1.pos.y}")
        scene.append_to_caption(' Change LegAngleValue      ')
        self.cbRotateLeg = checkbox(bind=self.autoRotateLeg, text='AutoRotateLeg')
        scene.append_to_caption('\n')
        self.winputArmAngle = winput(pos=scene.caption_anchor, bind = self.armAngleInput, text = f"{self.angle2.pos.x}")
        scene.append_to_caption(' Change ArmAngleValue      ')
        self.cbRotateArm = checkbox(bind=self.autoRotateArm, text='autoRotateArm')




crane = Crane()
crane.initParts()
crane.initInterface()
