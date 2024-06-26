import numpy as np
import pygame as pg
import os
from src.vertex import Vertex

class Object:
    vertices: list[Vertex]
    lines: list[(Vertex, Vertex)]

    def __init__(self, vertices: list[Vertex], lines: list[(Vertex, Vertex)]):
        self.vertices = vertices
        self.lines = lines

    def attach_renderer(self, renderer):
        self.__renderer = renderer

    def draw(self):
        vertices_matrix = np.array([[v.x, v.y, v.z, 1.0] for v in self.vertices])
        vertices_matrix = vertices_matrix @ self.__renderer.camera.camera_matrix()
        hidden_vertices = [row[0, 2] <= 0 for row in vertices_matrix]
        vertices_matrix = vertices_matrix @ self.__renderer.camera.projection_matrix()
        vertices_matrix /= vertices_matrix[:, -1].reshape(-1, 1)
        vertices_matrix = vertices_matrix @ self.__renderer.camera.screen_matrix()
        vertices_matrix = vertices_matrix[:, :2]
        vertices = {}
        for i in range(len(self.vertices)):
            if not hidden_vertices[i]:
                vertices[self.vertices[i]] = vertices_matrix[i].tolist()[0]

        for v in vertices.values():
            pg.draw.circle(self.__renderer.screen, pg.Color("black"), v, 2)
        for l in self.lines:
            v1 = vertices.get(l[0])
            v2 = vertices.get(l[1])
            if (v1 is None or v2 is None):
                continue
            pg.draw.line(self.__renderer.screen, pg.Color("black"), v1, v2, 1)
        
        