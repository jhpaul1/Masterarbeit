import numpy as np

def d_p(max_capacity, weights, values, alp, factor):
    d = len(max_capacity)
    #all_o_r = all_optimal_results
    #r_o_r = relevsant_optimal_results
    r_o_r = np.zeros(factor) 
    if d == 1:
        all_o_r = d_p_1(max_capacity, weights, values)
        for i in range(1,factor+1):
            r_o_r[i-1] = all_o_r[i*alp[0]]
    elif d == 2:
        all_o_r = d_p_2(max_capacity, weights, values)
        for i in range(1,factor+1):
            r_o_r[i-1] = all_o_r[i*alp[0],i*alp[1]]
    elif d == 3:
        all_o_r = d_p_3(max_capacity, weights, values)
        for i in range(1,factor+1):
            r_o_r[i-1] = all_o_r[i*alp[0],i*alp[1],i*alp[2]]
    elif d == 4:
        all_o_r = d_p_4(max_capacity, weights, values)
        for i in range(1,factor+1):
            r_o_r[i-1] = all_o_r[i*alp[0],i*alp[1],i*alp[2],i*alp[3]]
    elif d == 5:
        all_o_r = d_p_5(max_capacity, weights, values)
        for i in range(1,factor+1):
            r_o_r[i-1] = all_o_r[i*alp[0],i*alp[1],i*alp[2],i*alp[3],i*alp[4]]
    return r_o_r

# Dynamische Programmierung dimension d=1
def d_p_1(max_capacity, weights, values):
    DP = np.zeros(np.append(len(values)+1,max_capacity+1))
    C1, wt1 = max_capacity[0],weights[0]
    for i in range(1,len(values)+1):
        for c_1 in range(C1+1):
                if c_1 == 0:
                    DP[i][c_1] = 0
                elif wt1[i-1] <= c_1:
                    if values[i-1] + DP[i-1][c_1-wt1[i-1]] > DP[i-1][c_1]:
                        DP[i][c_1] = values[i-1] + DP[i-1][c_1-wt1[i-1]]
                    else:
                        DP[i][c_1]=DP[i-1][c_1]
                else:
                    DP[i][c_1] = DP[i-1][c_1]
    return DP[-1]
# Dynamische Programmierung dimension d=2
def d_p_2(max_capacity, weights, values):
    DP = np.zeros(np.append(len(values)+1,max_capacity+1))
    C1,C2 = max_capacity[0],max_capacity[1]
    wt1,wt2 = weights[0],weights[1]
    for i in range(1,len(values)+1):
        for c_1 in range(C1+1):
            for c_2 in range(C2+1):
                if c_1 == 0 and c_2 ==0:
                    DP[i][c_1][c_2] = 0
                elif wt1[i-1] <= c_1 and wt2[i-1] <= c_2:
                    if values[i-1] + DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]] > DP[i-1][c_1][c_2]:
                        DP[i][c_1][c_2] = values[i-1] + DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]]
                    else:
                        DP[i][c_1][c_2] = DP[i-1][c_1][c_2]
                else:
                    DP[i][c_1][c_2] = DP[i-1][c_1][c_2]
    return DP[-1]

# Dynamische Programmierung dimension d=3
def d_p_3(max_capacity, weights, values):
    DP = np.zeros(np.append(len(values)+1,max_capacity+1))
    C1,C2,C3 = max_capacity[0],max_capacity[1],max_capacity[2]
    wt1,wt2,wt3 = weights[0],weights[1],weights[2]  
    for i in range(1,len(values)+1):
        for c_1 in range(C1+1):
            for c_2 in range(C2+1):
                for c_3 in range(C3+1):
                    if c_1 == 0 and c_2 == 0 and c_3 == 0:
                        DP[i][c_1][c_2][c_3] = 0
                    elif wt1[i-1] <= c_1 and wt2[i-1] <= c_2 and wt3[i-1] <= c_3:
                        if values[i-1] + DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]] > DP[i-1][c_1][c_2][c_3]:
                            DP[i][c_1][c_2][c_3] = values[i-1] + DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]]
                        else:
                            DP[i][c_1][c_2][c_3] = DP[i-1][c_1][c_2][c_3]
                    else:
                        DP[i][c_1][c_2][c_3] = DP[i-1][c_1][c_2][c_3]
    return DP[-1]


def d_p_4(max_capacity, weights, values):

    DP = np.zeros(np.append(len(values)+1,max_capacity+1))
    
    C1 = max_capacity[0]
    C2 = max_capacity[1]
    C3 = max_capacity[2]
    C4 = max_capacity[3]
    wt1 = weights[0]
    wt2 = weights[1]
    wt3 = weights[2]
    wt4 = weights[3]

    for i in range(1,len(values)+1):
        for c_1 in range(C1+1):
            for c_2 in range(C2+1):
                for c_3 in range(C3+1):
                    for c_4 in range(C4+1):
                        if c_1 == 0 and c_2 == 0 and c_3 == 0 and c_4 == 0:
                            DP[i][c_1][c_2][c_3][c_4] = 0

                        elif wt1[i-1] <= c_1 and wt2[i-1] <= c_2 and wt3[i-1] <= c_3 and wt4[i-1] <= c_4:

                            if values[i-1]+ DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]][c_4-wt4[i-1]] > DP[i-1][c_1][c_2][c_3][c_4]:
                                DP[i][c_1][c_2][c_3][c_4] = values[i-1]+ DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]][c_4-wt4[i-1]]
                            else:
                                DP[i][c_1][c_2][c_3][c_4] = DP[i-1][c_1][c_2][c_3][c_4]
                        
                        else:
                            DP[i][c_1][c_2][c_3][c_4] = DP[i-1][c_1][c_2][c_3][c_4]
 
    return DP[-1]


def d_p_5(max_capacity, weights, values):

    DP = np.zeros(np.append(len(values)+1,max_capacity+1))
    
    C1 = max_capacity[0]
    C2 = max_capacity[1]
    C3 = max_capacity[2]
    C4 = max_capacity[3]
    C5 = max_capacity[4]
    wt1 = weights[0]
    wt2 = weights[1]
    wt3 = weights[2]
    wt4 = weights[3]
    wt5 = weights[4]

    for i in range(1,len(values)+1):
        for c_1 in range(C1+1):
            for c_2 in range(C2+1):
                for c_3 in range(C3+1):
                    for c_4 in range(C4+1):
                        for c_5 in range(C5+1):
                            if c_1 == 0 and c_2 == 0 and c_3 == 0 and c_4 == 0 and c_5 == 0:
                                DP[i][c_1][c_2][c_3][c_4][c_5] = 0

                            elif wt1[i-1] <= c_1 and wt2[i-1] <= c_2 and wt3[i-1] <= c_3 and wt4[i-1] <= c_4 and wt5[i-1] <= c_5:

                                if values[i-1]+ DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]][c_4-wt4[i-1]][c_5-wt5[i-1]] > DP[i-1][c_1][c_2][c_3][c_4][c_5]:
                                    DP[i][c_1][c_2][c_3][c_4][c_5] = values[i-1]+ DP[i-1][c_1-wt1[i-1]][c_2-wt2[i-1]][c_3-wt3[i-1]][c_4-wt4[i-1]][c_5-wt5[i-1]]
                                else:
                                    DP[i][c_1][c_2][c_3][c_4][c_5] = DP[i-1][c_1][c_2][c_3][c_4][c_5]
                            
                            else:
                                DP[i][c_1][c_2][c_3][c_4][c_5] = DP[i-1][c_1][c_2][c_3][c_4][c_5]
    
    return DP[-1]
