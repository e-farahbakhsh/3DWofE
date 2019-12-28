# P-A Plot
# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Post Probability,
# Studentized Post Probability
# ----------------------------
# The first way is to count voxels without taking them into fuzzy space
# ---------------------------------------------------------------------
import csv
import math
import numpy

threshold_target = 0.4
# threshold_variance = 0.531251151868501
# num_class = 10

# # Min and max of the both factors
# col_temp = []
# min_fac = []
# max_fac = []
# for i in range(2):
#     input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Input.csv")
#     input_reader = csv.reader(input_file)
#     for row in input_reader:
#         col_temp.append(float(row[i+4]))
#     min_fac.append(min(col_temp))
#     max_fac.append(max(col_temp))
#     col_temp = []
# del input_file
# del input_reader

# # Calculating the increment of each factor
# increment_fac = []
# for i in range(2):
#     increment_fac.append((max_fac[i]-min_fac[i])/num_class)

# # Generating a csv file containing the thresholds for classifying each factor
# output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Thresholds.csv", "wb")
# output_writer = csv.writer(output_file)
# thresholds_fac_temp = []
# j = 1
# while j < num_class:
#     for i in range(2):
#         thresholds_fac_temp.append(min_fac[i]+(j*increment_fac[i]))
#     output_writer.writerow(thresholds_fac_temp)
#     thresholds_fac_temp = []
#     j += 1
# del output_file
# del output_writer

# # Generating a csv file containing the numbers we need to plot P-A graphs
# input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Thresholds.csv")
# input1_reader = csv.reader(input1_file)
# output1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Anomaly.csv", "wb")
# output1_writer = csv.writer(output1_file)
# output2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Area.csv", "wb")
# output2_writer = csv.writer(output2_file)
# NumAnomaly = [0]*2
# NumArea = [0]*2
# for row1 in input1_reader:
#     input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Input.csv")
#     input2_reader = csv.reader(input2_file)
#     for row2 in input2_reader:
#         if float(row2[3]) > threshold_target and float(row2[4]) > float(row1[0]):
#             NumAnomaly[0] += 1
#         if float(row2[3]) > threshold_target and float(row2[5]) > float(row1[1]):
#             NumAnomaly[1] += 1
#         if float(row2[4]) > float(row1[0]):
#             NumArea[0] += 1
#         if float(row2[5]) > float(row1[1]):
#             NumArea[1] += 1
#     output1_writer.writerow(NumAnomaly)
#     output2_writer.writerow(NumArea)
#     NumAnomaly = [0]*2
#     NumArea = [0]*2
# del input1_file
# del input1_reader
# del input2_file
# del input2_reader
# del output1_file
# del output1_writer
# del output2_file
# del output2_writer
# ------------------
# Min and max of the both factors
col_temp = []
min_fac = []
max_fac = []
for i in range(2):
    input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Input.csv")
    input_reader = csv.reader(input_file)
    for row in input_reader:
        col_temp.append(float(row[i+4]))
    min_fac.append(min(col_temp))
    max_fac.append(max(col_temp))
    col_temp = []
del input_file
del input_reader

# Calculating parameters of the logistic function
par_s = []
par_i = []
for i in range(2):
    par_s.append((2*math.log(99))/(max_fac[i]-min_fac[i]))
    par_i.append((max_fac[i]+min_fac[i])/2)

# Taking factor values into fuzzy space using the logistic function
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Input.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Fuzzy Scores.csv", "wb")
output_writer = csv.writer(output_file)
col_temp = []
for row in input_reader:
    col_temp.append(row[3])
    for i in range(2):
        col_temp.append(1/(1+math.exp(-1*par_s[i]*(float(row[i+4])-par_i[i]))))
    # Total variance
    # col_temp.append(row[6])
    output_writer.writerow(col_temp)
    col_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Generating a csv file containing the numbers we need to plot P-A graphs
output1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Anomaly.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Volume.csv", "wb")
output2_writer = csv.writer(output2_file)
thresholds = list(numpy.arange(0, 1, 0.05))
NumAnomaly = [0]*2
NumArea = [0]*2
for i in range(len(thresholds)):
    input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Fuzzy Scores.csv")
    input_reader = csv.reader(input_file)
    for row in input_reader:
        if float(row[0]) > threshold_target and float(row[1]) > thresholds[i]:
            NumAnomaly[0] += 1
        if float(row[0]) > threshold_target and float(row[2]) > thresholds[i]:
            NumAnomaly[1] += 1
        if float(row[1]) > thresholds[i]:
            NumArea[0] += 1
        if float(row[2]) > thresholds[i]:
            NumArea[1] += 1
    output1_writer.writerow(NumAnomaly)
    output2_writer.writerow(NumArea)
    NumAnomaly = [0]*2
    NumArea = [0]*2
del input_file
del input_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

# Masking out voxels with high total variance
# output1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Anomaly.csv", "wb")
# output1_writer = csv.writer(output1_file)
# output2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Volume.csv", "wb")
# output2_writer = csv.writer(output2_file)
# thresholds = list(numpy.arange(0, 1, 0.05))
# NumAnomaly = [0]*2
# NumArea = [0]*2
# for i in range(len(thresholds)):
#     input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/P-A/Fuzzy Scores.csv")
#     input_reader = csv.reader(input_file)
#     for row in input_reader:
#         if float(row[0]) > threshold_target and float(row[1]) > thresholds[i] and float(row[3]) < threshold_variance:
#             NumAnomaly[0] += 1
#         if float(row[0]) > threshold_target and float(row[2]) > thresholds[i] and float(row[3]) < threshold_variance:
#             NumAnomaly[1] += 1
#         if float(row[1]) > thresholds[i] and float(row[3]) < threshold_variance:
#             NumArea[0] += 1
#         if float(row[2]) > thresholds[i] and float(row[3]) < threshold_variance:
#             NumArea[1] += 1
#     output1_writer.writerow(NumAnomaly)
#     output2_writer.writerow(NumArea)
#     NumAnomaly = [0]*2
#     NumArea = [0]*2
# del input_file
# del input_reader
# del output1_file
# del output1_writer
# del output2_file
# del output2_writer
