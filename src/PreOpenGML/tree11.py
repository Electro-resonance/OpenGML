#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Created By  : Martin Timms
# Created Date: 06/12/2022
# License: BSD-3-Clause License
# LicenseDir: https://github.com/Electro-resonance/OpenGML/blob/main/LICENSE
# Organisation: OpenGML.org/
# Project: https://github.com/Electro-resonance/OpenGML
# Description: Early BlochCircles demo (Pre OpenGML)
# Runs purely from PyGame without any of the methods to easily build GML trees.
# Provided as is.
# =============================================================================

#sudo easy_install-3.7 anytree

#https://anytree.readthedocs.io/en/latest/

from anytree import NodeMixin, RenderTree
import math
import pygame

from random import randint

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

class GMLBaseClass(object):  # Just an example of a base class
   foo=0
class GML(GMLBaseClass, NodeMixin):  # Add Node feature
   osc_count=0
   def __init__(self, name, screen, diameter, colour, freq, phase, phase_total, parent=None, child=None):
      super(GML, self).__init__()
      self.count=0
      self.name = name
      self.screen = screen
      self.diameter = diameter
      self.colour = colour
      if (freq==0):
          freq=0.5
      self.freq = (100+self.count)/freq+0.1
      self.orbit_radius = abs(freq*1)
      self.phase = phase
      self.phase_total= phase_total
      self.parent = parent
      self.mypos = [400,400]
      self.visited=False
      self.children1=[]
      if child:  # set children only if given
          self.children = children
      GML.osc_count+=1

   def add_child(self,node):
      self.children1.append(node)

   def oscillators(self):
      return GML.osc_count

   def clear_visited(self):
      self.visited=False

   def run1(self,limit):
      self.phase+=self.freq
      if(self.phase>360):
          self.phase-=360
      radians=self.phase/180*3.1245926535
      self.pos=[self.orbit_radius*math.sin(radians),self.orbit_radius*math.cos(radians)]
      if(self.parent==None):
          self.mypos=[400,400]
      else:
          self.mypos=self.parent.mypos
      pygame.draw.circle(screen,self.colour, self.mypos , self.orbit_radius, 1)
      self.mypos=[self.mypos[0]+self.pos[0],self.mypos[1]+self.pos[1]]
      pygame.draw.circle(screen,self.colour, self.mypos , self.diameter, 0)

      limit-=1
      if(limit>0):
          for child_node in self.children1:
              if (child_node!=None):
                 child_node.run1(limit)

      self.phase_total+=self.phase
      if(self.phase_total>360):
          self.phase_total-=360
      if(self.phase_total<360):
          self.phase_total+=360

      self.count+=0.00003
      if self.count>1000:
          self.count=100
      self.count=1.31234

          

def nest(parent_node,i):
    if(i==10):
        return
    colour=[255/(i+1),255-(255/(i+1)),randint(1,255)]
    gm1=GML('GML1',screen,5,colour,randint(20,40)/(i+1)*2, 0,0, parent=parent_node)
    gm2=GML('GML2',screen,7,colour,randint(40,60)/(i+1)*2, 120,0, parent=parent_node)
    gm3=GML('GML3',screen,9,colour,randint(-70,-60)/(i+1)*3, 240,0, parent=parent_node)
    parent_node.add_child(gm1)
    parent_node.add_child(gm2)
    parent_node.add_child(gm3)
    i=i+1
    nest(gm1,i)
    nest(gm2,i)
    nest(gm3,i)
    

parent_node=None
rootNode=GML('GML',screen,10,[255,0,0],0.0001, 10,0, parent=parent_node)
i=0
nest(rootNode,0)

#Print the text tree view
#clocks=0
#for pre, fill, node in RenderTree(rootNode):
#     treestr = u"%s%s" % (pre, node.name)
#     print(treestr.ljust(8), round(node.freq,3), node.phase)
#     clocks+=1
#print("Clocks: ",clocks)
print("Clocks: ",rootNode.oscillators())



done = False

start=True
while (start==False):
    keypress=pygame.key.get_pressed()
    if (keypress[pygame.K_s]==True):
       start=True 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

loop=2
dir=1
while not done:
    if(loop>10 or loop<2):
        dir=-dir
    loop+=0.01*dir
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pos = (screen.get_width()/2, screen.get_height()/2)
    
    screen.fill(0)
 
    limit=int(loop)
    rootNode.run1(limit)


    pygame.display.flip()
    
pygame.quit()
exit()
