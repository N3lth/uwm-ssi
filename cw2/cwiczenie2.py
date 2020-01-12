import csv
import random
from collections import Counter

def openAndParseSystemData(filename):
    with open(filename) as types:
        reader = csv.reader(types, delimiter=' ')
        rows = list()
        for row in reader:
            if row[-1] == '':
                row.pop()
            rows.append(row)
    return rows

def getClassChance(trn_data, selected_trn_class):
    amount_of_class_selected = 0
    for trn_object in trn_data:
        if trn_object[-1] == selected_trn_class:
            amount_of_class_selected += 1
    total_objects_of_trn = len(trn_data)
    return amount_of_class_selected / total_objects_of_trn

def getClassObjects(trn_data, trn_class):
    result = list()
    for trn_object in trn_data:
        if trn_object[-1] == trn_class:
            result.append(trn_object)
    return result


def getHighestChanceClasses(values, highest_chance):
    result = set()
    for (trn_class, chance) in values.items():
        if chance == highest_chance:
            result.add(trn_class)
    return list(result)

def getClassQuantity(data_rows):
    class_qty = dict()
    for row in data_rows:
        dec_class = row[-1]
        if dec_class in class_qty:
            class_qty[dec_class] = class_qty[dec_class] + 1
        else:
            class_qty[dec_class] = 1
    return class_qty

def getAllDecisionClasses(data_rows):
    decision_classes = set()
    for row in data_rows:
        decision_classes.add(row[-1])
    return decision_classes

def getTrainingClassEstimations(trn_classes):
    trn_class_estimations = dict()
    for trn_class in trn_classes:
        trn_class_objects = getClassObjects(trn_data, trn_class)
        tst_object_atr_chances = dict()
        for tst_object_idx in range(len(tst_data)):
            tst_object = tst_data[tst_object_idx]
            tst_object_atr_chances[tst_object_idx] = []
            for atr_idx_of_tst_object in range(len(tst_object)):
                if atr_idx_of_tst_object == len(tst_object) - 1:
                    break
                tst_object_atr = tst_object[atr_idx_of_tst_object]
                trn_objects_of_same_class_as_tst_object = list(
                    map(lambda atr: atr[atr_idx_of_tst_object], trn_class_objects))
                occurrence = trn_objects_of_same_class_as_tst_object.count(tst_object_atr)
                tst_object_atr_chances[tst_object_idx].append(occurrence / len(trn_objects_of_same_class_as_tst_object))
        trn_class_estimations[trn_class] = tst_object_atr_chances
    return trn_class_estimations

def calculateClassesClasificationChance(trn_class_estimations):
    global calculated_class_estimations, trn_class
    calculated_class_estimations = dict()
    for trn_class in trn_class_estimations.keys():
        trn_class_chance = getClassChance(trn_data, trn_class)
        for trn_estimations in trn_class_estimations.get(trn_class).values():
            if trn_class in calculated_class_estimations.keys():
                calculated_class_estimations[trn_class].append(trn_class_chance * sum(trn_estimations))
            else:
                calculated_class_estimations[trn_class] = [trn_class_chance * sum(trn_estimations)]

def classifyNewDecisionAndCountGlobalAccuracy():
    global altered_tst_data, overall_amount_of_correctly_classified, amount_of_correctly_classified_for_class, trn_class
    altered_tst_data = list()

    altered_tst_data = copySystemData(tst_data)
    overall_amount_of_correctly_classified = 0
    amount_of_correctly_classified_for_class = dict()

    for object_idx in range(len(tst_data)):
        comparison_lookup_dict = dict()
        for trn_class, estimations in calculated_class_estimations.items():
            comparison_lookup_dict[trn_class] = estimations[object_idx]
        comparison_lambda = lambda x: max(x, key=lambda item: item[1])
        highest_chance = comparison_lambda(Counter(comparison_lookup_dict).most_common())[1]
        highest_chance_classes = getHighestChanceClasses(comparison_lookup_dict, highest_chance)
        classified_by_trn_data = random.choice(highest_chance_classes)
        if tst_data[object_idx][-1] == classified_by_trn_data:
            overall_amount_of_correctly_classified += 1
            if tst_data[object_idx][-1] in amount_of_correctly_classified_for_class.keys():
                amount_of_correctly_classified_for_class[tst_data[object_idx][-1]] += 1
            else:
                amount_of_correctly_classified_for_class[tst_data[object_idx][-1]] = 1
        altered_tst_data[object_idx][-1] = random.choice(
            getHighestChanceClasses(comparison_lookup_dict, highest_chance))

def copySystemData(tst_data):
    copy = list()
    for tst_object in tst_data:
        copy.append(tst_object[:])
    return copy

def getGlobalAccuracy():
    return overall_amount_of_correctly_classified / len(tst_data)

def getBalancedAccuracy():
    values = list()
    for tst_class, class_quantity in class_qty.items():
        if tst_class in amount_of_correctly_classified_for_class.keys():
            values.append(amount_of_correctly_classified_for_class[tst_class] / class_quantity)
    balanced_accuracy = sum(values) / len(all_classes)
    return balanced_accuracy

def saveAccuracyFile():
    accuracy_template_file = open("acc_bayes.txt", "w+")
    accuracy_template_file.writelines(["global_accuracy;balanced_accuracy\n",
                                       f'{getGlobalAccuracy()};{getBalancedAccuracy()}'])
    accuracy_template_file.close()

def saveBayesClassificationResults():
    dec_bayes_template: [str] = ["tst_object;classifier_decision\n"]
    for idx in range(len(tst_data)):
        dec_bayes_template.append(
            f'{tst_data[idx]};{altered_tst_data[idx][-1]}\n')
    dec_bayes_template_file = open("dec_bayes.txt", "w+")
    dec_bayes_template_file.writelines(dec_bayes_template)
    dec_bayes_template_file.close()

# data assembling
print("Wpisz pełną nazwę pliku systemu testowego:")
data_filename = str(input())
print("Wpisz pełną nazwę pliku systemu treningowego:")
type_filename = str(input())

tst_data = openAndParseSystemData('australian_TST.txt')
trn_data = openAndParseSystemData('australian_TRN.txt')
class_qty = getClassQuantity(tst_data)
all_classes = getAllDecisionClasses(tst_data)
tst_classification = list(map(lambda row: row[-1], tst_data))
trn_classes = set(map(lambda row: row[-1], trn_data))

# processing
calculateClassesClasificationChance(getTrainingClassEstimations(trn_classes))
classifyNewDecisionAndCountGlobalAccuracy()
saveAccuracyFile()
saveBayesClassificationResults()








