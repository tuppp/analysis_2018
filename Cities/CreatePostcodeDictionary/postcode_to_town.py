import fileinput


def main():
    url = open("./PostCodesData.dat",'r')
    target = open("./bereinigtePostDaten.dat", 'w')
    out = url.readlines()
    for line in out:
        line = line.rstrip('\n')
        line = line.replace(' ','')
        lines = line.split(',')

        print(lines[1], " ist " ,lines[2])
        
        target.write(str(lines[1]+ "," +lines[2]+"\n"))



main()