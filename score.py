from utility import utility

def avg(lst, start, end, jump):
    num = 11
    total = 0
    for i in range(start, end, jump):
        try:
            total += float(lst[i])
        except ValueError:
            num -= 1
    return total / num

def main():
    with open('/Users/yaocheng/Downloads/CS235a_Term_Project_Ideas - Sheet1.tsv', 'r') as fp:
        excts = []
        bigs = []
        techs = []
        
        for line in fp.readlines()[1:-2]:
            elmts = line.strip().split('\t')
            l = len(elmts)

            avg_exct = avg(elmts, 6, l, 3)
            excts.append(avg_exct)
            
            avg_big = avg(elmts, 7, l, 3)
            bigs.append(avg_big)

            avg_tech = avg(elmts, 8, l, 3)
            techs.append(avg_tech)

    for i in range(len(excts)):
        print excts[i], bigs[i], techs[i]
            


if __name__ == '__main__':
    main()