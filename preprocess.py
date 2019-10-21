import csv
import argparse

def loadData(path):
    data = []
    f = open(path, "r", encoding = "utf-8")
    for row in csv.reader(f):
        for i in range(len(row)):
            row[i] = row[i].strip(".?")
            try:
                row[i] = eval(row[i])
            except NameError:
                pass
        data += [row]
    f.close()
    return data

def saveData(path, data):
    f = open(path, "w", encoding = "utf-8", newline = "")
    csv.writer(f).writerows(data)
    f.close()

def zScoreNorm(data, prop):
    if prop not in data[0]:
        return data
    pos = data[0].index(prop)

    column = [data[i][pos] for i in range(1, len(data))]
    mean = sum(column) / len(column)
    deviation = (sum([(column[i] - mean) ** 2 for i in range(len(column))]) / len(column)) ** (1/2)
    
    f = lambda x: (x - mean) / deviation
    column = list(map(f, column))
    for i in range(1, len(data)):
        data[i][pos] = column[i - 1]
    
    return data

def removeOutlier(data, prop, threshold):
    if prop not in data[0]:
        return data
    pos = data[0].index(prop)

    data[1:] = [row for row in data[1:] if row[pos] <= threshold and row[pos] >= -threshold]
    return data

def main():
    parser = argparse.ArgumentParser(description = "Data preprocessing")
    parser.add_argument("--input", help = "Input file path", required = True)
    parser.add_argument("--output", help = "Output file path", required = True)
    parser.add_argument("--task", help = "Preprocessing task", required = True)
    parser.add_argument("--prop", help = "Property", required = True, nargs = "*")
    parser.add_argument("--threshold", help = "Threshold for removing outlier")
    args = parser.parse_args()

    data = loadData(args.input)
    if args.task == "zScoreNorm":
        for prop in args.prop:
            data = zScoreNorm(data, prop)
    elif args.task == "removeOutlier":
        for prop in args.prop:
            data = removeOutlier(data, prop, eval(args.threshold))
    saveData(args.output, data)

main()