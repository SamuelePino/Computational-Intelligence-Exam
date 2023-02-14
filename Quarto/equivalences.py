
from numpy import rot90, flip, fliplr, flipud
import numpy as np


def flip_over_diag(M: np.ndarray, on_anti_diag: bool=False) -> np.ndarray:
    return rot90(fliplr(M)) if not on_anti_diag else rot90(flipud(M))

if  __name__== "__main__":

    # for test
    M = np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15]])

    print(np.linalg.eigvals(M) )

    M1 = flip_over_diag(M, on_anti_diag=True)

    print(np.linalg.eigvals(M1) )