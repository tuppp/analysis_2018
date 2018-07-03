import fileinput




def create_Postcode_List(lineElements):
    if lineElements[0].find("–") != -1:
        if len(lineElements)< 2:
            return ''
        new_line = [[]]
        numbers = lineElements[0].split('–')
        for x in range(int(numbers[0]), int(numbers[1])):
            new_line.append(str(x))
            new_line.append(lineElements[1])
            new_line =list(filter(None, new_line))
        return new_line
    else:
        return lineElements


def main():
    url = open("./PostCodesData.dat",'r')
    out = url.readlines()
    wholelines = []
    longstring = ''
    for line in out:
        line = line.rstrip('\n')
        line = line.replace(' ','')
        lines = line.split('-')
        lines = create_Postcode_List(lines)
        

        
        longstring = longstring+str(lines)


        #if line != '':
        #    print(lines)
        #    wholelines.append(line+';')
        
    longstring = longstring.replace('\'','')
    longstring = longstring.replace('[',',')
    longstring = longstring.replace(']','')
    longstring = longstring.replace(' ','')

    mass_list = longstring.split(',')

    print(mass_list)

main()



def sort(list):
    placeholder = ''
    for x in list:
        if represents_int(x):
            print(x)
        else :


def city(city,placeholder):
    new_line = placeholder+city

def postcode(postcode, placeholder):
    





def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False




