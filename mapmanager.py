import pickle, fileinput
from panda3d.core import TransparencyAttrib
class Mapmanager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'
        self.startNew()
        self.orange_terracota_list = [(75, 63, 6), (73, 63, 6), (83, 63, 5), (83, 63, 7), (83, 63, 8), (81, 63, 5), 
        (81, 63, 7), (81, 63, 8), (82, 63, 3), (82, 63, 4), (82, 63, 6), (82, 63, 8), (66, 63, 3), (66, 63, 4),
        (84, 60, 5), (84, 60, 7),(84, 60, 8), (84, 62, 5), (84, 62, 7), (84, 62, 8), (84, 61, 3), (84, 61, 4),
        (84, 61, 6), (84, 61, 8),(67, 63, 5), (67, 63, 7), (67, 63, 8), (65, 63, 5),(65, 63, 7), (65, 63, 8),
        (66, 63, 6), (66, 63, 8), (64, 62, 5), (64, 62, 7), (64, 62, 8), (64, 60, 5), (64, 60, 7), (64, 60, 8),
        (64, 61, 3), (64, 61, 4), (64, 61, 6), (64, 61, 8), (74, 56, 1), (74, 55, 1), (74, 51, 1), (77, 53, 1),
        (74, 50, 1), (75, 52, 1), (73, 52, 1), (73, 54, 1), (75, 54, 1), (72, 53, 1), (71, 53, 1), (76, 53, 1)]
        self.blue_terracota_list = [(74, 53, 1)]
        self.treasure_list = [(122, 54, 11),
                (121, 54, 11),(121, 54, 12),
                (121, 55, 11),(120, 54, 11),
                (120, 55, 11),(120, 56, 11),
                (121, 56, 11),(121, 55, 12),
                (120, 55, 12),(119, 56, 11),
                (119, 54, 11),(119, 55, 11),
                (118, 64, 11),(118, 63, 11),
                (118, 64, 12),(118, 65, 11),
                (119, 64, 11),(119, 69, 11),
                (120, 69, 11),(121, 69, 11),
                (121, 68, 11),(120, 68, 11),
                (119, 68, 11),(119, 67, 11),
                (120, 67, 11),(121, 67, 11),
                (120, 68, 12),(123, 67, 12),
                (123, 66, 12),(118, 69, 12),
                (117, 66, 12),(117, 65, 12),
                (117, 63, 12),(117, 64, 12)]
        self.magenta_glass_list = [(124, 54, 15), (124, 55, 15),
        (116, 54, 15), (116, 55, 15),
        (118, 52, 15), (122, 52, 15),
        (124, 55, 14), (116, 61, 14),
        (116, 54, 14), (116, 55, 14), 
        (124, 61, 14), (116, 65, 14),
        (124, 65, 14)]
        self.colors_dict = {
            'diamond_block' : (92/255, 219/255, 213/255, 1),
            'sand' : (219/255, 207/255, 163/255, 1),
            'orange_terracota' : (161/255, 83/255, 37/255, 1),
            'blue_terracota' : (74/255, 59/255, 91/255 ,1),
            'purpur_block' : (169/255, 125/255, 169/255, 1),
            'purpur_pillar' : (171/255, 129/255, 171/255, 1),
            'end_stone_brick' : (218/255, 224/255, 162/255, 1),
            'obsidian' : (15/255, 10/255, 24/255, 1),
            'magenta_glass' : (178/255, 76/255, 216/255, 0.2),
            'wood' : (1, 1, 1, 1)
        }
        self.files = ['obsidian.txt', 'purpur_pillar.txt', 'end_stone_brick.txt', 'wood.txt']
 
    def startNew(self):
        self.land = render.attachNewNode("Land")
  
    def addBlock(self, position, color = (127/255, 178/255, 56/255, 1), transparency = False):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(color)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(position))
        if transparency:
            self.block.setTransparency(TransparencyAttrib.M_alpha)
            self.block.setDepthWrite(False)
            self.block.setBin('fixed', 0)

    def buildBlock(self, pos, color = (127/255, 178/255, 56/255, 1)):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z+1:
            self.addBlock(new, color)

    def del_pos_from_file(self, filename, pos):
        with open(filename, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            file.writelines(lines[:-1])

    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()
            for i in self.files:
                if pos in self.converter(i):
                    self.del_pos_from_file(i, pos)
            
    def destBlock(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        self.delBlock(pos)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadland(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z2 in range(int(z) + 1):
                        block = self.addBlock((x, y, z2))
                    x += 1
                y += 1  

    def isEmpty(self, pos):
        return False if self.findBlocks(pos) else True
    
    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def converter(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            tup_list = list()
            for tup in lines:
                tup_list.append(tuple(list(map(int, tup.strip('\n').replace('(', '').replace(')', '').replace(',', '').split()))))
            return tup_list

    def save(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as file:
            pickle.dump(len(blocks), file)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file)

    def load(self):
        self.clear()
        with open('my_map.dat', 'rb') as fil:
            length = pickle.load(fil)
            for i in range(length):
                pos = pickle.load(fil)
                if pos[2] > 0:
                    if (pos[0] <= 52 and pos[1] <= 62) or pos in self.treasure_list:#diamond pyramid
                        self.addBlock(pos, self.colors_dict['diamond_block'])

                    elif (pos[0] > 52 and pos[0] <= 84) and pos[1] <= 63:#desert temple
                        if pos in self.orange_terracota_list:
                            self.addBlock(pos, self.colors_dict['orange_terracota'])
                        elif pos in self.blue_terracota_list:
                            self.addBlock(pos, self.colors_dict['blue_terracota'])
                        else:
                            self.addBlock(pos, self.colors_dict['sand'])
                    
                    elif pos[0] > 84: #end ship
                        if pos in self.converter('obsidian.txt'):
                            self.addBlock(pos, self.colors_dict['obsidian'])
                        elif pos in self.converter('purpur_pillar.txt'):
                            self.addBlock(pos, self.colors_dict['purpur_pillar'])
                        elif pos in self.converter('end_stone_brick.txt'):
                            self.addBlock(pos, self.colors_dict['end_stone_brick'])
                        elif pos in self.converter('wood.txt'):
                            self.addBlock(pos, self.colors_dict['wood'])
                        elif pos in self.magenta_glass_list:
                            self.addBlock(pos, self.colors_dict['magenta_glass'], True)
                        else:
                            self.addBlock(pos, self.colors_dict['purpur_block'])
                else:
                    self.addBlock(pos)