import numpy as np

class Item:
    #Initialization of an Item
    def __init__(self, ind, val, wt, alphas):
        self.ind = ind
        self.val = val
        self.wt = wt
        self.size = np.dot(wt, alphas)
        #self.max_wt = max(wt)
        #self.new_density = val/max(wt)
        self.n_max_wt = max([wt[i]/alphas[i] for i in range(len(wt))])
        self.n_density = val/max([wt[i]/alphas[i] for i in range(len(wt))])
        self.swap_item = "no"

    def __str1__(self):
        string = ""
        for i in self.wt:
            string += f'{i }'
        return f'Ind: {self.ind}, Val: {self.val}, Wt: [{string}], Density: {round(self.n_density,2)}'

    def __str2__(self):
        string = ""
        for i in self.wt:
            string += f'{i} '
        return f'Ind: {self.ind}, SWAP-ITEM: {self.swap_item}, Val: {self.val}, Wt: [{string}], l_max: [{self.n_max_wt}], Density: {round(self.density,2)}'