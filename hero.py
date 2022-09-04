from direct.showbase.ShowBase import ShowBase
import pickle
key_switch_camera = 'i'

key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'
key_up = 'u'
key_down = 'n'

key_turn_left = 'j'
key_turn_right = 'k'

key_change_mode = 'g'
key_build = 'mouse1'
key_destroy = 'mouse3'
key_save = 'mouse2'
key_load = 'l'
key_get_pos = 'h'

key_purpur_pillar = '1'
key_end_stone_brick = '2'
key_obsidian = '3'
key_wood = '4'
class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(51/255, 204/255, 51/255, 1)
        self.spectator = True
        self.color = (92, 219, 213, 1)
        self.hero.setScale(0.5)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUnbind(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUnbind()
        else:
            self.cameraBind()

    def accept_events(self):
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)

        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right+'-repeat', self.turn_right)

        base.accept(key_forward, self.move_forward)
        base.accept(key_forward+'-repeat', self.move_forward)

        base.accept(key_back, self.move_back)
        base.accept(key_back+'-repeat', self.move_back)

        base.accept(key_left, self.move_left)
        base.accept(key_left+'-repeat', self.move_left)

        base.accept(key_right, self.move_right)
        base.accept(key_right+'-repeat', self.move_right)

        base.accept(key_up, self.move_up)
        base.accept(key_up+'-repeat', self.move_up)

        base.accept(key_down, self.move_down)
        base.accept(key_down+'-repeat', self.move_down)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_change_mode, self.change_gm)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_load, self.land.load)
        base.accept(key_save, self.land.save)

        base.accept(key_get_pos, self.get_block_pos_print)
        
        base.accept(key_purpur_pillar, self.purpur_pillar)
        base.accept(key_end_stone_brick, self.end_stone_brick)
        base.accept(key_obsidian, self.obsidian)
        base.accept(key_wood, self.wood)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5)%360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5)%360)

    def spect_move(self, angle):
        self.hero.setPos(self.look_at(angle))

    def surv_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def move_choose(self, angle):
        if self.spectator:
            self.spect_move(angle)
        else:
            self.surv_move(angle)
    
    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        if (angle >= 0 and angle <= 20) or (angle > 335 and angle <= 360):
            return 0, -1
        elif angle <= 65:
            return 1, -1
        elif angle <= 110:
            return 1, 0
        elif angle <= 155:
            return 1, 1
        elif angle <= 200:
            return 0, 1
        elif angle <= 245:
            return -1, 1
        elif angle <= 290:
            return -1, 0
        elif angle <= 335:
            return -1, -1

    def move_forward(self):
        angle = self.hero.getH() % 360
        self.move_choose(angle)

    def move_back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_choose(angle)

    def move_left(self):
        angle = (self.hero.getH()+90) % 360
        self.move_choose(angle)

    def move_right(self):
        angle = (self.hero.getH()+270) % 360
        self.move_choose(angle)

    def move_up(self):
        self.hero.setZ(self.hero.getZ() + 1)
    
    def move_down(self):
        self.hero.setZ(self.hero.getZ() - 1)

    def change_gm(self):
        self.spectator = False if self.spectator else True

    def build(self, key = 'diamond_block'):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.spectator:
            self.land.addBlock(pos, self.land.colors_dict[key])
        else:
            self.land.buildBlock(pos, self.land.colors_dict[key])
    
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.spectator:
            self.land.delBlock(pos)
        else:
            self.land.destBlock(pos)

    def get_block_pos_print(self):
        angle = self.hero.getH() % 360
        print(self.look_at(angle))

    def get_block_pos_return(self):
        angle = self.hero.getH() % 360
        return self.look_at(angle)

    def purpur_pillar(self):
        self.build('purpur_pillar')
        with open('purpur_pillar.txt', 'a+') as file:
            file.write(str(self.get_block_pos_return())+'\n')


    def end_stone_brick(self):
        self.build('end_stone_brick')
        with open('end_stone_brick.txt', 'a+') as file:
            file.write(str(self.get_block_pos_return())+'\n')

    def obsidian(self):
        self.build('obsidian')
        with open('obsidian.txt', 'a+') as file:
            file.write(str(self.get_block_pos_return())+'\n')

    def wood(self):
        self.build('wood')
        with open('wood.txt', 'a+') as file:
            file.write(str(self.get_block_pos_return())+'\n')