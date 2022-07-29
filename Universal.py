import numpy as np
import matplotlib.pyplot as plt
import time

from DP import d_p
from Item import Item
from generate_examples import discrete_uniform_distribution_weights,discrete_uniform_distribution_values,normal_distribution_values,sum_values
from own_examples import own_example

class Items:
    #dimensions: weights dxn, values 1xn
    All_Items = []
    Order = []

    def __init__(self, weights, values, alphas):
        self.All_Items = []
        self.Order = []
        transposedWeights = np.transpose(weights)
        for i in range(len(values)):
            self.All_Items.append(Item(i+1, values[i], transposedWeights[i], alphas))

    
    def sortBy_density(self):
        self.All_Items.sort(key=lambda x: x.ind, reverse=True)
        self.All_Items.sort(key=lambda x: x.n_density, reverse=True)


    def sortBy_lmax(self):
        #Improvement of Universal
        #self.All_Items.sort(key=lambda x: x.size)
        self.All_Items.sort(key=lambda x: x.n_max_wt)


    def __str__(self,m):
        if m == 1:
            for i in self.All_Items:
                print(i.__str1__())
        elif m == 2:
            for i in self.All_Items:
                print(i.__str2__())
        return


    #MGreedy for every relevant capacity
    def ALL_Greedy(self,alphas,factor):
        self.sortBy_density()
        #self.__str__(1)
        
        Greedy_results = np.zeros(factor)
        for i in range(1,factor+1):
            Greedy_results[i-1] = self.MGreedy(i*alphas)

        return Greedy_results

    #Algorithm described in Thesis
    def MGreedy(self, capacity):
        #self.sortBydensity()
        #self.__str__(1)

        k = 0
        totalValue = 0
        total_wt = np.zeros(len(capacity))
        for i in self.All_Items:
            if all(i.wt <= capacity):
                current_val = i.val
                total_wt += i.wt
                if all(capacity - total_wt >= 0):
                    totalValue += current_val 
                    k += 1   
                else:
                    break
            else:
                k += 1

        #no Item fit in or every Item fit in
        if k == len(self.All_Items):
            return totalValue
        else:
            while any(self.All_Items[k].wt > capacity):
                k += 1
                if k == len(self.All_Items):
                    return totalValue
            #V(P)>=V(D_{k^*+1})
            if totalValue >= self.All_Items[k].val:
                #print(totalValue,self.All_Items[k].val)
                return totalValue
            #V(D_{k^*+1})>V(P)
            else:
                #print(totalValue,self.All_Items[k].val)
                return self.All_Items[k].val


    #Determines all SWAP ITEMS, Def from Thesis
    def determineswapitems(self):     
        for t1 in self.All_Items:
            summ = 0
            for t2 in self.All_Items:
                if t2.n_max_wt <= t1.n_max_wt and t2.n_density > t1.n_density:
                    summ += t2.val
                if t2.n_max_wt <= t1.n_max_wt and t2.n_density == t1.n_density and t2.ind > t1.ind:
                    summ += t2.val             
            #print(t1.val,summ)
            if t1.val > summ:
                t1.swap_item = "yes"

    #Comparison for density
    def comparison_density(self,j,ritem,Order):
        if j <=len(Order) and Order[j-1].n_density > ritem.n_density:
            return True
        elif j <=len(Order) and Order[j-1].n_density == ritem.n_density and Order[j-1].ind > ritem.ind:
            return True
        return False

    #Universal Alg from Paper, returns Permutation
    def Universal(self):
        self.determineswapitems()
        self.sortBy_lmax()
        #self.__str__(2)

        for ritem in self.All_Items:
            if ritem.swap_item == "yes":
                self.Order.insert(0,ritem)
            else:
                if len(self.Order)==0:
                    self.Order.append(ritem)
                else:
                    j=1
                    while True == self.comparison_density(j,ritem,self.Order):
                        j +=1
                    self.Order.insert(j-1,ritem)
        # print("ORDER UNIVERSAL: ")
        # for r in self.Order:
        #    print("Ind:",r.ind,"SW",r.swap_item,"Value:",r.val,"Weights:",r.wt,"Density:",round(r.n_density,2),"l_max:",r.n_max_wt)
        return self.Order 

#Uses Packing Order from Universal Alg and returns a solution
def PackingwithOrder(Order,capacity):
    total_Value = 0
    total_wt = np.zeros(len(capacity))
    for item in Order:
        if all(capacity - total_wt - item.wt >= 0):
            total_wt += item.wt
            total_Value += item.val   
    return total_Value

#Calculates Optimal results and results of Universal and MGreedy 
def opt_gre_uni(values,weights,alphas, mgreedy):
    #consider only relevant capacities
    max_cap = [np.sum(i, axis=0) for i in weights]
    factor = max([int(np.ceil(max_cap[i]/alphas[i])) for i in range(len(max_cap))])
    #maximal capacity of relevant capacties
    Maximal_Capacity =  alphas * factor
    #print("Maximal Capacity",Maximal_Capacity)

    start1 = time.time()
    optimal_results = d_p(Maximal_Capacity,weights,values,alphas,factor)
    ende1= time.time()
    time_opt = round(ende1-start1,4)
    
    all_items = Items(weights,values,alphas)
    start2=time.time()
    if mgreedy:
        greedy_results = all_items.ALL_Greedy(alphas,factor)
    ende2 = time.time()
    time_gre = round(ende2-start2,4)

    start3 = time.time()
    Order = all_items.Universal()
    universal_results = np.zeros(factor)
    for i in range(factor):
        universal_results[i] = PackingwithOrder(Order,(i+1)*alphas)
    ende3 = time.time()
    time_uni = round(ende3-start3,4)
    
    if mgreedy:
        return optimal_results, greedy_results, universal_results, time_opt, time_gre, time_uni
    else:
        return optimal_results, universal_results


#calculates ratio between optimum and universal or greedy
def calculate_ratio_wt(values,weights,alphas,mgreedy):

    if mgreedy:
        optimal_results, greedy_results, universal_results, time_opt, time_gre, time_uni = opt_gre_uni(values,weights,alphas,mgreedy)

    else:
        optimal_results, universal_results = opt_gre_uni(values,weights,alphas,mgreedy)

    #consider only relevant capacities   
    max_cap = [np.sum(i, axis=0) for i in weights]
    factor = max([int(np.ceil(max_cap[i]/alphas[i])) for i in range(len(max_cap))])
    #maximal capacity of relevant capacties
    #Maximal_Capacity =  alphas * factor

    ratio_gre = np.zeros(factor)
    ratio_uni = np.zeros(factor)

    for i in range(factor):
        if optimal_results[i] == 0 and universal_results[i] == 0:
            ratio_uni[i] = 1

            if mgreedy:
                ratio_gre[i] = 1
        else:
            ratio_uni[i]  = optimal_results[i]/universal_results[i]
            if mgreedy:
                ratio_gre[i] = optimal_results[i]/greedy_results[i]

    if mgreedy:
        mean_uni = np.mean(ratio_uni)
        mean_gre = np.mean(ratio_gre)
        return ratio_uni,mean_uni,ratio_gre,mean_gre,time_opt,time_uni,time_gre 

    else:
        return ratio_uni



#plot figure 5.1 thesis
def figure_1():

    # run own example
    #values, weights, alphas = own_example(1)

    n = 10
    L = 100
    sigma = L * 0.1
    d = 2
    weights = discrete_uniform_distribution_weights(n,d,L)
    values, alphas = normal_distribution_values(n,d,weights,sigma)

    print(values)
    print(weights)
    
    #calculate results of Optimum, MGreedy and Universal 
    opt,gre,uni, time_opt, time_gre, time_uni = opt_gre_uni(values, weights, alphas,True)
    capacities = np.arange(1,len(opt)+1)

    #test for which capacity universal returns a smaller value than before
    for i in range(len(uni)-2):
        if uni[i+1] < uni[i]:
            print(i+1,uni[i+1],uni[i])

    plt.plot(capacities,gre,'b', linewidth=0.9, label=r'$v(MGreedy(\mathcal{I},C))$')

    plt.plot(capacities,uni,'r', linewidth=0.9, label=r'$v(UNI(\mathcal{I},C))$')

    plt.plot(capacities,opt,'g', linewidth=0.9, label=r'$v(OPT(\mathcal{I},C))$')

    plt.ylabel('Gewinnwert $v(S)$')
    plt.xlabel('Kapazität C')
    plt.legend(loc='best',frameon =True)
    
    plt.show()







#plot figure 5.2 thesis
def figure_2():
    
    n = 10
    L = 5
    sigma = L * 0.1
    different_d = [1,2,3,4,5]

    fig , axs =plt.subplots(1,1)
    column_headers = ["W-C-Universal","W-C-MGreedy","Mean-Universal","Mean-MGreedy","Gesamt-Laufzeit","Opt.-Laufzeit","Uni.-Laufzeit","MGr.-Laufzeit"]
    row_headers = [" d = 1 "," d = 2 "," d = 3 "," d = 4 "," d = 5 "]
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.4))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.4)) 
    axs.axis('tight')
    axs.axis('off')
    data = np.zeros((len(row_headers),len(column_headers)))

    for d in different_d:
        #print(d)
        start = time.time()
        weights = discrete_uniform_distribution_weights(n,d,L)
        values, alphas = normal_distribution_values(n,d,weights,sigma)
       
        #calculate results of Optimum, MGreedy and Universal (and their runtime)
        ratio_uni,mean_uni,ratio_gre,mean_gre,time_opt,time_uni,time_gre = calculate_ratio_wt(values,weights,alphas,True)

        ende = time.time()
        data[d-1,0] = round(max(ratio_uni),4)
        data[d-1,1] = round(max(ratio_gre),4)        
        data[d-1,2] = round(mean_uni,4)
        data[d-1,3] = round(mean_gre,4)
        data[d-1,4] = round(ende-start,4)
        data[d-1,5] = time_opt
        data[d-1,6] = time_uni
        data[d-1,7] = time_gre
    axs.table(cellText=data,rowLabels=row_headers,rowColours=rcolors,rowLoc='right',colColours=ccolors,colLabels=column_headers,loc='center')

    plt.show()



#plot figure 5.3 thesis
def figure_3():
    number_examples = 20
    #Data Figure 5.3
    d=1
    different_n = [5,10,5]
    different_L = [5,10,50,100]
    
    fig , axs = plt.subplots(1,1)

    column_headers = ["n="+str(n) for n in different_n]
    row_headers = ["$L=$"+str(l) for l in different_L]
    data = np.zeros((len(row_headers),len(column_headers)))

    for n in range(len(different_n)):
        #print(different_n[n])
        for l in range(len(different_L)):
            #print(different_L[l])
            sigma = different_L[l] * 0.1
            wc_results = np.zeros(number_examples)

            for i in range(number_examples):
                weights = discrete_uniform_distribution_weights(different_n[n],d,different_L[l])
                values, alphas = normal_distribution_values(different_n[n],d,weights,sigma)
                ratio_uni = calculate_ratio_wt(values,weights,alphas,False)
                wc_results[i] = max(ratio_uni)
            
            data[l,n] = round(np.mean(wc_results),2)

    #Initialization colours
    colors = plt.cm.BuPu(np.linspace(0.1,0.6, len(row_headers)))
    
    #Initialize and plot bars
    index = np.arange(len(column_headers))+ 0.2
    bar_width = 0.8
    y_offset = np.zeros(len(column_headers))
    for row in range(len(data)):
        plt.bar(index, data[row], bar_width, 
                    bottom=y_offset, 
                    color=colors[row],
                    align = 'center')
        y_offset = y_offset + data[row]

    #Plot table
    the_table = plt.table(cellText=data,
                        rowLabels=row_headers,
                        rowColours=colors,
                        colLabels=column_headers,
                        loc='bottom')
    
    #Layout
    plt.subplots_adjust(left=0.2, bottom=0.2)
    plt.ylabel("Worst-Case")
    plt.xticks([])
    plt.yticks(np.arange(6))
    plt.title('Dimension $d=$'+str(d))
    
    plt.show()



#plot figure 5.4 thesis - very similar to figure_3()
def figure_4():

    number_examples = 20

    #Data Figure 5.4
    dimensions = [2,3]
    different_n = [5,10,15]
    different_L = [5,10,15]

    plt.subplots_adjust(wspace=0.5,hspace=0.5)

    position = [221,222]

    for i in range(len(dimensions)):
        d = dimensions[i]
        #print("dimension=",d)

        plt.subplot(position[i])
        column_headers = ["n="+str(n) for n in different_n]
        row_headers = ["$L=$"+str(l) for l in different_L]
        data = np.zeros((len(row_headers),len(column_headers)))

        for n in range(len(different_n)):
            #print("different_n",different_n[n])
            for l in range(len(different_L)):
                #print("L=",different_L[l])
                sigma = different_L[l] * 0.1
                wc_results = np.zeros(number_examples)

                for i in range(number_examples):
                    print(i)
                    weights = discrete_uniform_distribution_weights(different_n[n],d,different_L[l])
                    values, alphas = normal_distribution_values(different_n[n],d,weights,sigma)
                    ratio_uni = calculate_ratio_wt(values,weights,alphas,False)
                    wc_results[i] = max(ratio_uni)
                
                data[l,n] = round(np.mean(wc_results),2)

        #Initialization colours
        colors = plt.cm.BuPu(np.linspace(0.1,0.6, len(row_headers)))
    
        #Initialize and plot bars
        index = np.arange(len(column_headers))+ 0.2
        bar_width = 0.8
        y_offset = np.zeros(len(column_headers))

        for row in range(len(data)):
            plt.bar(index, data[row], bar_width, 
                    bottom=y_offset, 
                    color=colors[row],
                    align = 'center')
            y_offset = y_offset + data[row]

        #Plot table
        the_table = plt.table(cellText=data,
                            rowLabels=row_headers,
                            rowColours=colors,
                            colLabels=column_headers,
                            loc='bottom')
        
        #Adjust layout
        plt.ylabel("Worst-Case")
        plt.xticks([])
        plt.yticks(np.arange(6))
        plt.title('Dimension $d=$'+str(d))

    plt.show()





#plot figure 5.5 thesis
def figure_5():

    n = 15
    L = 20
    d = 3
    sigma = 0.1 * L

    fig , axs = plt.subplots(3,1)
    fig.suptitle("Verhältnis von " + str(r'$v(UNI(\mathcal{I},C))$') + " und " +str( r'$v(OPT(\mathcal{I},C))$')+ " für verschiedene Bsp.")
    plt.subplots_adjust(hspace=1)

    for i in range(len(axs)):
        print(i+1)
        weights = discrete_uniform_distribution_weights(n,d,L)
        values,alphas = normal_distribution_values(n,d,weights,sigma)
        ratio = calculate_ratio_wt(values,weights,alphas,False)
        #print(max(ratio))
        axs[i].plot(ratio)
        axs[i].set(xlabel="Kapazität C")
        
    plt.show()


#plot figure 5.3 thesis
def figure_6():

    n = 10
    L = 10
    v_min = 1
    v_max = 10
    sigma = 0.1 * L
    dimensions=[1,2,3]
    #d=1
    number_of_examples = 100
    
    labels = ["Bsp. 1", "Bsp. 2", "Bsp. 3"]
    #fig , axs = plt.subplots()
    fig , axs = plt.subplots(3,1)

    for i in range(len(dimensions)):
        d = dimensions[i]
        print("dimension",d)

        results = np.zeros((number_of_examples,3))
        for b in range(number_of_examples):
            print(b)
            weights = discrete_uniform_distribution_weights(n,d,L)
            values,alphas = sum_values(n,d,weights)   
            values1,alphas1 = normal_distribution_values(n,d,weights,sigma)
            values2, alphas2 = discrete_uniform_distribution_values(n,d,v_min,v_max)

            ratio_uni = calculate_ratio_wt(values, weights, alphas, False)
            ratio_uni1 = calculate_ratio_wt(values1, weights, alphas1, False)
            ratio_uni2 = calculate_ratio_wt(values2, weights, alphas2, False)

            results[b,0] = round(max(ratio_uni),4)
            results[b,1] = round(max(ratio_uni1),4)
            results[b,2] = round(max(ratio_uni2),4)

        axs[i].boxplot(results, patch_artist = True, labels = labels)

    plt.show()



#plot figures thesis
if __name__ == "__main__":


    #figure_1()

    #figure_2()

    #figure_3()

    #figure_4()
    
    #figure_5()

    #figure_6()