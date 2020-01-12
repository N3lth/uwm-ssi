import csv
import math

def openAndParseTypeFile(filename):
    try:
        with open(filename) as types:
            reader = csv.reader(types, delimiter=' ')
            attributes_with_types = dict()
            for row in reader:
                attributes_with_types[row[0]] = row[1]
    except:
        print('Wystąpił błąd')
    return attributes_with_types

def openAndParseDataFile(filename):
    try:
        with open(filename) as types:
            reader = csv.reader(types, delimiter=' ')
            rows = list()
            for row in reader:
                rows.append(row)
    except:
        print('Wystąpił błąd')
    return rows

def getAllDecisionClasses(data_rows):
    decision_classes = set()
    for row in data_rows:
        decision_classes.add(row[-1])
    return decision_classes

def getClassQuantity(data_rows):
    class_qty = dict()
    for row in data_rows:
        dec_class = row[-1]
        if dec_class in class_qty:
            class_qty[dec_class] = class_qty[dec_class] + 1
        else:
            class_qty[dec_class] = 1
    return class_qty

def getUniqueAttrValueQty(data_rows):
    attr_unique_values = dict()
    for attr_idx in range(len(data_rows[0]) - 1):
        col_values = list(map(lambda row: row[attr_idx], data_rows))
        attr_unique_values['a' + str(attr_idx + 1)] = len(set(col_values))
    return attr_unique_values

def getNumericCols(data_rows, attributes_with_types):
    num_attr_idx = set()
    num_cols = dict()
    i = 0
    for attr_type in attributes_with_types.values():
        if attr_type == 'n':
            num_attr_idx.add(i)
        i += 1
    for idx in num_attr_idx:
        num_cols['a' + str(idx + 1)] = list(map(lambda row: float(row[idx]), data_rows))
    return num_cols

def getAvailableValues(data_rows):
    av_values = dict()
    for attr_idx in range(len(data_rows[0]) - 1):
        av_values['a' + str(attr_idx + 1)] = set(map(lambda row: row[attr_idx], data_rows))
    return av_values

def getAttributeStandardDeviation(num_cols):
    attr_dev = dict()
    for attr, col in num_cols.items():
        col_sum = sum(col)
        avg = col_sum / len(col)
        dev_sum = 0
        for row in col:
            dev_sum += pow((row - avg), 2)
        dev = math.sqrt(dev_sum / (len(col) - 1))
        attr_dev[attr] = round(dev, 3)
    return attr_dev

def getAttributeStandardDeviation(num_cols):
    attr_dev = dict()
    for attr, col in num_cols.items():
        col_sum = sum(col)
        avg = col_sum / len(col)
        dev_sum = 0
        for row in col:
            dev_sum += pow((row - avg), 2)
        dev = math.sqrt(dev_sum / (len(col) - 1))
        attr_dev[attr] = round(dev, 3)
    return attr_dev

def separateDataRowsByDecisionClasses(data_rows):
    separated_rows = dict()
    for row in data_rows:
        if row[-1] in separated_rows.keys():
            separated_rows[row[len(row) - 1]].append(row)
        else:
            separated_rows[row[len(row) - 1]] = [row]
    return separated_rows

def countDevForEachDecClass(rows_by_decision_classes, attributes_with_types):
    class_with_dev = dict()
    for dec_class, rows in rows_by_decision_classes.items():
        dec_class_num_cols = getNumericCols(rows, attributes_with_types)
        class_with_dev[dec_class] = getAttributeStandardDeviation(dec_class_num_cols)
    return class_with_dev

# data assembling
print("Wpisz pełną nazwę pliku danych:")
data_filename = str(input())
print("Wpisz pełną nazwę pliku typów:")
type_filename = str(input())

# processing
data_rows = openAndParseDataFile(data_filename)
attributes_with_types = openAndParseTypeFile(type_filename)
decision_classes = getAllDecisionClasses(data_rows)
class_qty = getClassQuantity(data_rows)
attr_unique_values = getUniqueAttrValueQty(data_rows)
num_cols = getNumericCols(data_rows, attributes_with_types)
av_values = getAvailableValues(data_rows)
attr_dev = getAttributeStandardDeviation(num_cols)
rows_by_decision_classes = separateDataRowsByDecisionClasses(data_rows)
dev_for_each_dec_class = countDevForEachDecClass(rows_by_decision_classes, attributes_with_types)

# listing
print('=========================================================')
print('WIELKOŚĆ KLASY DECYZYJNEJ:')
print('--------------------------')
for decision_class in decision_classes:
    print(decision_class, end = " -> ")
    print(class_qty[decision_class])
print('')
print('=========================================================')
print('MINIMALNE I MAKSYMALNE WARTOŚCI ATRYBUTÓW:')
print('--------------------------')
for atr, values in av_values.items():
    if atr in num_cols:
        print('MAX \'%s\'' % atr, end = " -> ")
        print(max(map(float, values)))
        print('MIN \'%s\'' % atr, end = " -> ")
        print(min(map(float, values)))
        print('--------------------------')
print()
print('')
print('=========================================================')
print('UNIKALNE WARTOŚCI ATRYBUTÓW')
print('--------------------------')
for atr, values in av_values.items():
    print('\'%s\'' % atr, end = " -> ")
    print(len(values))
    print('--------------------------')
print('')
print('=========================================================')
print('DOSTĘPNE WARTOŚCI ATRYBUTÓW')
print('--------------------------')
for atr, values in av_values.items():
    print('\'%s\'' % atr, end = " -> ")
    print(values)
    print('--------------------------')
print('')
print('=========================================================')
print('ODCHYLENIE STANDARDOWE')
print('--------------------------')
for atr, value in attr_dev.items():
    if atr in num_cols:
        print('\'%s\'' % atr, end = " -> ")
        print(value)
        print('--------------------------')
print('')
for dc_class, dev in dev_for_each_dec_class.items():
    print('=========================================================')
    print('ODCHYLENIE STANDARDOWE DLA KLASY %s' % dc_class)
    print('--------------------------')
    for atr, value in dev.items():
        if atr in num_cols:
            print('\'%s\'' % atr, end=" -> ")
            print(value)
            print('--------------------------')
print('')