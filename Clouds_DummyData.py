import sys
import pandas as pd
import scipy as sc
from scipy import stats
import numpy as np




#0  = wolkenlos
#1  = sonnig
#2  = heiter
#3  = leicht bewoelkt
#4  = wolkig
#5  = bewoelkt
#6  = starkt bewoelkt
#7  = fast bedeckt
#8  = bedeckt

dwd = [2,3,6,7,8,4,2,1,0];
wetterdienst = ['heiter','wolkig','sonnig', 'stark bewoelkt', 'bedeckt', 'leicht bewoelkt','wolkenlos','fast bedeckt', 'bewoelkt'];


def cloudy_convert_wetterdienst(cloud_wetterdienst):
    cloudo_list = []
    ## for l in range(len(list)):
    ##line = list.rstrip()
    ## list.split(",")

    cloud_list = []
    for cloud in cloud_wetterdienst:
            if cloud  == 'wolkenlos':
                cloud_list.append(0)
            elif cloud == 'sonnig':
                cloud_list.append(1)
            elif cloud == 'heiter':
                cloud_list.append(2)
            elif cloud == 'leicht bewoelkt':
                cloud_list.append(3)
            elif cloud == 'wolkig':
                cloud_list.append(4)
            elif cloud == 'bewoelkt':
                append = cloud_list.append(5)
            elif cloud == 'stark bewoelkt':
                cloud_list.append(6)
            elif cloud == 'fast bedeckt':
                cloud_list.append(7)
            else:
                cloud_list.append(8)
    cloudo_list.append(cloud_list)

    return cloudo_list




listi = []
#listi.append('a')
print(listi)

temperature_diff = []
def Temp_difference(x,y):

    for i in range(len(x)):
        temp_diff = x(i) - y(i)
        abs(temp_diff)
    return temp_diff


def mean_square(x,y):
    x = np.ravel(x)
    y = np.ravel(y)

    x_ms = np.sum(((x-y)**2))

    x_ms = np.sqrt(x_ms / len(x))

    return x_ms


def mean_square_data(x,y):
    difflist =[]
    for i in range(len(x)):
        a = mean_square(x,y)
        difflist.append(a)
    return difflist



cloudy_list = cloudy_convert_wetterdienst (wetterdienst)
cloudy_list = np.ravel(cloudy_list)
print('cloudy list:',cloudy_list)
difflist_comparison_all_data = mean_square_data(cloudy_list,dwd)
print('all data:',difflist_comparison_all_data)
#mock_data_wetter = [['sonnig', 'heiter', 'wolkig', 'fast_bedeckt'],
                #['wolkig','fast_bedeckt','sonnig','heiter']]


#Dahlem_dwd = np.array([6.2,5.6,6.1,6.1,6.3,5.3,5.7,7.2,8,3.4])
#Dahlem_waether = np.array([29,21,49,46,47,16,54,57,54,88])



#cloudy_list = [[0.25, 0.375, 0.625, 0.875], [0.625, 0.875, 0.25, 0.375]]


#mock_data_dbd = [[6/8, 1/8, 7/8, 2/8],
 #                [6/8, 1/8, 7/8, 3/8]]

#def spearman(mock_data,cloudlist):
 #   korrel = []
  #  pvall = []
   # for i in range(len(mock_data)):
    #        korr, pval = sc.stats.spearmanr(mock_data[i], cloudy_list[i])
     #       korrel.append(korr)
      #      pvall.append(pvall)
    #return korrel, pvall

#print(cloudy_spearman(mock_data_dbd, cloudy_list))
#print(sc.stats.spearmanr(mock_data_dbd, cloudy_list))

#print(spearman(mock_data_dbd,cloudy_list))


def rms(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())
###########################







#if __name__ == "__main__":
 #   main(sys.argv)
