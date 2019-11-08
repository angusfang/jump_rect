from typing import Type, Any, Union

import numpy as np
import pygame
import transformation as tra
import math
from dynamic import Dynamic


class Atom:
    def __init__(self, dir, element_pos_atom, k=10000,m=10000):
        self.element_pos_atom: np.array() = np.array(element_pos_atom)
        self.element_posnow_atom = np.array(element_pos_atom)
        self.dir=np.array(dir)
        self.force = np.array([[0], [0], [0], [0]])
        self.mass=m
        self.dynamic=Dynamic(self.mass)
        self.dynamic.x0=self.element_pos_atom

        self.k = k
        self.rect = pygame.Rect

    def draw(self, world_T_element, size, a_surface: pygame.Surface):



        world_pos_atom = world_T_element.dot(self.element_pos_atom)
        x = world_pos_atom[0][0]
        y = world_pos_atom[1][0]
        atom_rect = pygame.Rect((0, 0), (size // 2, size // 2), )
        atom_rect.center = (x, y)
        self.rect = atom_rect
        # a_surface.fill([255, 255, 255,50], atom_rect)

        if np.shape(self.element_posnow_atom)==(4,1):
            world_posnow_atom = world_T_element.dot(self.element_posnow_atom)
            xn=int(world_posnow_atom[0][0])
            yn=int(world_posnow_atom[1][0])

            vec = np.array(self.element_posnow_atom) - np.array(self.element_pos_atom)
            atom_force = -self.k * vec
            self.dynamic.x0 = np.array(self.element_posnow_atom)
            self.dynamic.set_dynamic(atom_force, self.mass, 0.1)
            self.element_posnow_atom = self.dynamic.x0


            pygame.draw.line(a_surface,[255,0,0],(x,y),(xn,yn))
            pygame.draw.circle(a_surface,[255,0,0],(xn,yn),5)









    def self_be_collide_force(self, other_atom_pos_relative_this_element,atom_size):
        # self.now=other_atom_pos_relative_this_element*self.dir
        B=self.element_pos_atom - other_atom_pos_relative_this_element
        A=(B/(np.linalg.norm(B)))*atom_size//1

        self.element_posnow_atom=A+other_atom_pos_relative_this_element
        ele_force = -np.linalg.norm(self.k *(A-B)*self.dir)*self.dir
        self.force=ele_force

        # vec = self.element_posnow_atom - self.element_pos_atom
        # atom_force = -self.k * vec * self.dir

        # self.dynamic.x0 = self.element_posnow_atom
        # self.dynamic.set_dynamic(self.force, self.mass, 0.000001)
        # self.element_posnow_atom = self.dynamic.x0




        # self.element_posnow_atom=other_atom_pos_relative_this_element@self.dir
        # force_from_self=



surface = pygame.display.set_mode((1400, 800))

def find_other_collide_element(id, element_list,sur=surface):





    element = element_list[id]
    rect_list = []
    for elementI in element_list:
        rect_list.append(elementI.rect)
        pygame.draw.rect(sur, [0,255,0],elementI.rect)
    element_collide_list = element.rect.collidelistall(element_list)
    id_index = element_collide_list.index(id)
    del (element_collide_list[id_index])
    return element_collide_list


def find_other_collide_atom(atom, atom_list):
    rect_list = []
    for atomI in atom_list:
        if atomI.rect==pygame.Rect:
            return Atom
        rect_list.append(atomI.rect)
    atom_collide_index = atom.rect.collidelist(rect_list)
    if atom_collide_index is not -1:
        return atom_list[atom_collide_index]
    return Atom


def transform_to_this_coord(world_T_element, collide_atom_relative_world):
    element_T_world = tra.inverse_4x4(world_T_element)
    return element_T_world @ collide_atom_relative_world


class ElementSide:
    def __init__(self, world_T_element):
        self.world_T_element: np.array() = world_T_element
        self.atom_buf = Atom([0, 0, 0, 0], [[0], [0], [0], [0]])
        self.atom_list = [Atom]
        self.atom_list.clear()
        self.net_force = [[0], [0], [0], [0]]
        self.atom_size = 40
        self.g = np.array([[0], [10], [0], [0]])
        self.mass = 200
        self.dt = 0.1
        self.dynamic = Dynamic(self.mass)
        self.dynamic.x0 = self.world_T_element[0:4, 3:4]
        self.rect = pygame.Rect

    def create_rect_atom_list(self, w, h):
        self.mass=math.sqrt(w*h)/10
        x_small = -w // 2
        x_big = w // 2
        y_small = -h // 2
        y_big = h // 2
        rx = self.world_T_element[0][3]
        ry = self.world_T_element[1][3]
        self.rect = pygame.Rect((0, 0), (w, h))
        self.rect.center = (rx, ry)
        for x in range(x_small, x_big, self.atom_size//4):
            self.atom_buf = Atom([[0], [1], [0], [0]], [[x], [y_big], [0], [1]])
            self.atom_list.append(self.atom_buf)
            self.atom_buf = Atom([[0], [-1], [0], [0]], [[x], [y_small], [0], [1]])
            self.atom_list.append(self.atom_buf)
        for y in range(y_small, y_big, self.atom_size//4):
            self.atom_buf = Atom([[1], [0], [0], [0]], [[x_big], [y], [0], [1]])
            self.atom_list.append(self.atom_buf)
            self.atom_buf = Atom([[-1], [0], [0], [0]], [[x_small], [y], [0], [1]])
            self.atom_list.append(self.atom_buf)
        self.atom_buf = Atom([[1], [0], [0], [0]], [[x_big], [y_big], [0], [1]])
        self.atom_list.append(self.atom_buf)
        self.atom_buf = Atom([[0], [1], [0], [0]], [[x_big], [y_big], [0], [1]])
        self.atom_list.append(self.atom_buf)

    def create_boundary_atom_list(self, w, h):
        x_small = -w // 2
        x_big = w // 2
        y_small = -h // 2
        y_big = h // 2

        for x in range(x_small, x_big, self.atom_size//2):
            self.atom_buf = Atom([[0], [1], [0], [0]], [[x], [y_big], [0], [1]])
            self.atom_list.append(self.atom_buf)
            self.atom_buf = Atom([[0], [-1], [0], [0]], [[x], [y_small], [0], [1]])
            self.atom_list.append(self.atom_buf)
        for y in range(y_small, y_big, self.atom_size//2):
            self.atom_buf = Atom([[1], [0], [0], [0]], [[x_big], [y], [0], [1]])
            self.atom_list.append(self.atom_buf)
            self.atom_buf = Atom([[-1], [0], [0], [0]], [[x_small], [y], [0], [1]])
            self.atom_list.append(self.atom_buf)
        self.atom_buf = Atom([[1], [0], [0], [0]], [[x_big], [y_big], [0], [1]])
        self.atom_list.append(self.atom_buf)
        self.atom_buf = Atom([[0], [1], [0], [0]], [[x_big], [y_big], [0], [1]])
        self.atom_list.append(self.atom_buf)

    def rotation(self, radian):
        self.world_T_element: np.array()

        R = tra.rotation_matrix4_from_matrix4(self.world_T_element)
        R = tra.rotation(R, radian)
        P = tra.translation_matrix4_from_matrix4(self.world_T_element)
        self.world_T_element = P @ R

    def draw(self, e_surface: pygame.Surface):

        atomI: (Atom)
        for atomI in self.atom_list:
            atomI.draw(self.world_T_element, self.atom_size, e_surface)

    def cal_dynamic_and_move(self, id, element_side_list, element_boundary):
        """

        :type element_boundary: ElementSide
        """
        force_g = self.mass * self.g
        force_atom = np.array([[0], [0], [0], [0]])
        force_atom_from_boundary = np.array([[0], [0], [0], [0]])

        self.dynamic.set_dynamic(force_g, self.mass, self.dt)
        self.world_T_element = tra.change_translation(self.world_T_element, self.dynamic.x0)
        self.rect.center=[self.world_T_element[0][3], self.world_T_element[1][3]]

        if self.rect.colliderect(element_boundary.rect):
            for atomI in self.atom_list:
                collide_atom: Union[Type[Atom], Any] = find_other_collide_atom(atomI, element_boundary.atom_list)
                if collide_atom is not Atom:
                    collide_atom_relative_world =element_boundary.world_T_element@collide_atom.element_posnow_atom
                    other_atom_pos_relative_this_element = transform_to_this_coord(self.world_T_element,
                                                                                   collide_atom_relative_world)
                    atomI.self_be_collide_force(other_atom_pos_relative_this_element,self.atom_size)
                    self.dynamic.v0 = np.array(self.dynamic.v0) * 0.95
                    self.dynamic.set_dynamic(atomI.force, self.mass, self.dt/len(self.atom_list))
                    self.dynamic.v0 = np.array(self.dynamic.v0) *0.95
                    self.world_T_element = tra.change_translation(self.world_T_element, self.dynamic.x0)
                    self.rect.center = [self.world_T_element[0][3], self.world_T_element[1][3]]
                    force_atom_from_boundary = force_atom_from_boundary + atomI.force

        collide_element_list = find_other_collide_element(id, element_side_list)
        for collide_element_index in collide_element_list:
            for atomI in self.atom_list:

                collide_elementI=element_side_list[collide_element_index]
                collide_atom = find_other_collide_atom(atomI, collide_elementI.atom_list)
                if collide_atom is not Atom:
                    collide_atom_relative_world=collide_elementI.world_T_element@collide_atom.element_posnow_atom
                    other_atom_pos_relative_this_element = transform_to_this_coord(self.world_T_element,
                                                                                   collide_atom_relative_world)
                    atomI.self_be_collide_force(other_atom_pos_relative_this_element,self.atom_size)
                    self.dynamic.v0 = np.array(self.dynamic.v0) * 0.95
                    self.dynamic.set_dynamic(atomI.force, self.mass, self.dt/len(collide_element_list)/len(self.atom_list))
                    self.dynamic.v0 = np.array(self.dynamic.v0) * 0.95
                    self.world_T_element = tra.change_translation(self.world_T_element, self.dynamic.x0)
                    self.rect.center = [self.world_T_element[0][3], self.world_T_element[1][3]]
                    force_atom = force_atom + atomI.force

        # self.net_force = force_g + force_atom*1+force_atom_from_boundary*1
        # self.dynamic.set_dynamic(self.net_force, self.mass, self.dt)
        # self.dynamic.v0=self.dynamic.v0*0.99
        # self.world_T_element = tra.change_translation(self.world_T_element, self.dynamic.x0)
        # self.rect.center=[self.world_T_element[0][3], self.world_T_element[1][3]]


if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((1500, 800))
    clock = pygame.time.Clock()
    surfRect = surface.get_rect()

    ele1 = ElementSide(np.array([
        [1, 0, 0, 750],
        [0, 1, 0, 400],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]))
    ele1.create_rect_atom_list(200 * 2, 200)
    move = tra.vec4_4_to_4x1([100, 0, 0, 1])
    ele1.world_T_element = tra.translation(ele1.world_T_element, move)

    while True:
        event_list = pygame.event.get()
        for EV in event_list:
            if EV.type == pygame.KEYDOWN:
                if EV.key == pygame.K_ESCAPE:
                    quit()

        surface.fill([255, 255, 255])

        ele1.rotation(math.radians(10))
        x = math.cos(pygame.time.get_ticks() // 100)

        ele1.draw(surface)
        # text1.use()
        print(pygame.time.get_ticks())
        pygame.display.flip()
