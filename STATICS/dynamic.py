import numpy

class Dynamic:

    def __init__(self,mass=1.0):
        self.x0=[[0],[0],[0],[1]]
        self.v0=[[0],[0],[0],[0]]



    def f_to_a(self,f,m):
        return f/m
    def a_to_v(self,a,t):
        return self.v0+a*t
    def v_to_x(self,v,t):
        return self.x0+v*t


    def set_dynamic(self,f,m,t):
        a=self.f_to_a(f,m)
        v=self.a_to_v(a,t)
        x=self.v_to_x(v,t)

        self.v0=v
        self.x0=x

