# Creating total variance/uncertainty and studentized posterior probability models
# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Fac1, Fac2, ...
# -----------------------------------------------------------------------------------------------------------------
import csv
import itertools
import math

# Threshold value for the target element
threshold = 0.4 # Replace with your desired number
# A list of threshold values for evidential models with respect to the input csv file
thresholds = [] # Fill the list with your desired numbers
# A list of the variances calculated for the positive weights of evidential models with respect to the input csv file
var_w_pos = [] # Fill the list with your desired numbers
# A list of the variances calculated for the negative weights of evidential models with respect to the input csv file
var_w_neg = [] # Fill the list with your desired numbers

# Variance of each voxel in evidential models
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Variance.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row in input_reader:
    row_temp.append(row[0])
    row_temp.append(row[1])
    row_temp.append(row[2])
    for i in range(len(thresholds)):
        if float(row[i+4]) > thresholds[i]:
            row_temp.append(var_w_pos[i])
        else:
            row_temp.append(var_w_neg[i])
    output_writer.writerow(row_temp)
    row_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Total variance/uncertainty of each voxel
input_file = open("D:/Variance.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Total Variance.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row in input_reader:
    row_temp.append(row[0])
    row_temp.append(row[1])
    row_temp.append(row[2])
    list_temp = [float(n) for n in row[3:]]
    row_temp.append(sum(list_temp))
    output_writer.writerow(row_temp)
    row_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Studentized posterior probability
input1_file = open("D:/Posterior Probability.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/Total Variance.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/Studentized Posterior Probability.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    row_temp.append(row1[0])
    row_temp.append(row1[1])
    row_temp.append(row1[2])
    row_temp.append(float(row1[3])/(math.sqrt(float(row2[3]))))
    output_writer.writerow(row_temp)
    row_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer
