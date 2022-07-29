import numpy as np

def own_example(N):
    if N==1:
        values = np.array([10,5,5,5,6])
        weights = np.array([[0,5,5,5,6],[10,0,0,5,0]])
        alphas = np.array([1,2])
        return values, weights, alphas
    
    if N==2:
        values = np.array([10,7,7])
        weights = np.array([[10,8,0],[10,0,8]])
        alphas = np.array([1,1])
        return values, weights, alphas
    
    if N==3:
        values = np.array([5,5,5,4,5])
        weights = np.array([[3,3,3,4,3],[3,3,3,0,3]])
        alphas = np.array([1,1])
        return values, weights, alphas
    
    if N==4:
        values = np.array([69, 16, 76, 135])
        weights = np.array([[72, 15, 6, 97],[1, 4, 66, 38],[0,0,0,100]])
        alphas = np.array([1,1])
        return values, weights, alphas
