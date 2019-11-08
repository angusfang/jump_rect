import numpy as np
import math


def translation(matrix_4x4, matrix_4x1):
    transformation = np.array([[1, 0, 0, matrix_4x1[0][0]],
                               [0, 1, 0, matrix_4x1[1][0]],
                               [0, 0, 1, matrix_4x1[2][0]],
                               [0, 0, 0, 1]])
    return transformation.dot(matrix_4x4)


def rotation(matrix_4, r_radian):
    cos_x = math.cos(r_radian)
    sin_x = math.sin(r_radian)
    transformation = np.array([[cos_x, -sin_x, 0, 0],
                               [sin_x, cos_x, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])
    return transformation.dot(matrix_4)


def inverse_4x4(matrix_4x4):
    matrix_4x4: np.array()
    r = matrix_4x4[0:3, 0:3]
    t = matrix_4x4[0:3, 3:4]
    r_ = np.transpose(r)
    t_ = -1 * r_ @ t
    _T = np.hstack((r_, t_))
    T = np.vstack((_T, [[0, 0, 0, 1]]))
    return T


def vec4_4_to_4x1(vec4):
    matrix = np.array([
        [vec4[0]],
        [vec4[1]],
        [vec4[2]],
        [vec4[3]]
    ])
    return matrix
def vec4_4_to_4x4(vec4):
    matrix = np.array([
        [1,0,0,vec4[0]],
        [0,1,0,vec4[1]],
        [0,0,1,vec4[2]],
        [0,0,0,vec4[3]]
    ])
    return  matrix
def rotation_matrix3_to_matrix4(matrix3):
    R_3x3 = matrix3
    m_1x3=np.reshape(np.array([0, 0, 0]), (1, 3))
    R_4x3 = np.vstack((R_3x3,m_1x3))
    m_4x1= np.reshape(np.array([0, 0, 0, 1]),(4, 1))
    R_4x4 = np.hstack((R_4x3,m_4x1))
    return R_4x4
def rotation_matrix4_from_matrix4(matrix4):
    matrix3=matrix4[0:3,0:3]
    return rotation_matrix3_to_matrix4(matrix3)
def translation_matrix4_from_matrix4(matrix4):
    m_3x1=matrix4[0:3,3:4]
    i_3x3=np.eye(3)
    m_3x4=np.hstack([i_3x3,m_3x1])
    m_1x4=np.array([[0,0,0,1]])
    m_4x4=np.vstack([m_3x4,m_1x4])
    return m_4x4

def change_translation(matrix4,matrix41):
    matrix43=matrix4[0:4,0:3]
    matrix44=np.hstack((matrix43,matrix41))
    return matrix44

# a=np.arange(12).reshape((3,4))
# b=np.arange(12,24).reshape((3,4))
# print(a)
# print(b)
# print(np.vstack((a,b)))