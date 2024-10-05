import numpy as np
import math

def LS(A, b, l_reg=0):

    C = np.dot(A.T, A)

    return np.dot(np.dot(np.linalg.inv(C + l_reg * np.eye(C.shape[0])), A.T),b)

def create_sinh_taylor_feature_matrix(u, n):

    u_feature = np.zeros((u.shape[0], n+1))
    for i in range(u.shape[0]):
        for n in range(0, n+1):
            u_feature[i,n] = (1 / math.factorial(2*n+1)) * (u[i] ** (2*n+1))
    
    return u_feature

def create_exp_taylor_feature_matrix(u, n):

    u_feature = np.zeros((u.shape[0], n + 1))
    for i in range(u.shape[0]):
        for n in range(0, n+1):
            u_feature[i,n] = (1 / math.factorial(n+1))*(u[i]**(n+1))
            
    return u_feature

def find_c_LRS(w):
    c1 = w[0] * np.sqrt(w[0] / w[1])
    c2 = np.sqrt(w[1] / w[0])

    return c1, c2

def find_c_HRS(w):
    c4 = w[1] / w[0]
    c3 = w[0] / c4

    return c3, c4