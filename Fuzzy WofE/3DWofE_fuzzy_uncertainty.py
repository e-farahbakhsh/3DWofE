# Creating uncertainty and studentized posterior probability models
# The input files are ...
# -----------------------------------------------------------------------------------------------------------------
import csv
import itertools
import math
import pandas

# Threshold value for the target element
threshold = 0.4

# Creating a variance list of positive weights for binary models
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Binary_Var_W_pos.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    binary_var_w_pos = row
del input_file
del input_reader

# Creating a variance list of negative weights for binary models
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Binary_Var_W_neg.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    binary_var_w_neg = row
del input_file
del input_reader

input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Final/Input_Binary.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance_Binary.csv", "wb")
output_writer = csv.writer(output_file)
variance_binary_temp = []
for row in input_reader:
    variance_binary_temp.append(row[0])
    variance_binary_temp.append(row[1])
    variance_binary_temp.append(row[2])
    for i in range(len(row)-4):
        if float(row[i+4]) == 1:
            variance_binary_temp.append(binary_var_w_pos[i])
        else:
            variance_binary_temp.append(binary_var_w_neg[i])
    output_writer.writerow(variance_binary_temp)
    variance_binary_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Continuous models
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Final/Input_Continuous.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    num_fac = len(row)-4
    break
del input_file
del input_reader

thresholds_continuous = []
varProD = []
for i in range(num_fac):
    df1 = pandas.read_csv("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Final/Thresholds_Continuous.csv", header=None, usecols=[i])
    thresholds_continuous_temp = df1[i].values.tolist()
    df2 = pandas.read_csv("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD_FC_B.csv", header=None, usecols=[i])
    varProD_temp = df2[i].values.tolist()
    thresholds_continuous.append(thresholds_continuous_temp)
    varProD.append(varProD_temp)

input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Final/Input_Continuous.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance_Continuous.csv", "wb")
output_writer = csv.writer(output_file)
variance_continuous_temp = []
for row in input_reader:
    variance_continuous_temp.append(row[0])
    variance_continuous_temp.append(row[1])
    variance_continuous_temp.append(row[2])
    for i in range(num_fac):
        for j in range(len(varProD_temp)-1):
            if j == 0:
                if float(row[i+4]) <= thresholds_continuous[i][j]:
                    variance_continuous_temp.append(varProD[i][j])
                    break
            elif j == len(varProD_temp)-2:
                if thresholds_continuous[i][j-1] < float(row[i+4]) <= thresholds_continuous[i][j]:
                    variance_continuous_temp.append(varProD[i][j])
                    break
                elif float(row[i+4]) > thresholds_continuous[i][j]:
                    variance_continuous_temp.append(varProD[i][j+1])
                    break
            else:
                if thresholds_continuous[i][j-1] < float(row[i+4]) <= thresholds_continuous[i][j]:
                    variance_continuous_temp.append(varProD[i][j])
                    break
    output_writer.writerow(variance_continuous_temp)
    variance_continuous_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Total variance/uncertainty of each voxel
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance_Binary.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance_Continuous.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Total Variance.csv", "wb")
output_writer = csv.writer(output_file)
totalVariance_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    totalVariance_temp.append(row[0])
    totalVariance_temp.append(row[1])
    totalVariance_temp.append(row[2])
    list1_temp = [float(n) for n in row1[3:]]
    list2_temp = [float(n) for n in row2[3:]]
    totalVariance_temp.append(sum(list1_temp)+sum(list2_temp))
    output_writer.writerow(totalVariance_temp)
    totalVariance_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# Studentized posterior probability
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Final/Posterior Probability.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Total Variance.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Studentized Posterior Probability.csv", "wb")
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
