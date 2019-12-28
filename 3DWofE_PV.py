# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Posterior Probability,
# Studentized Posterior Probability
# ----------------------------
import csv
import math
import numpy

threshold_target = 0.4

col_temp = []
min_fac = []
max_fac = []
for i in range(2):
    input_file = open("D:/Input.csv")
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
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Fuzzy Scores.csv", "wb")
output_writer = csv.writer(output_file)
col_temp = []
for row in input_reader:
    col_temp.append(row[3])
    for i in range(2):
        col_temp.append(1/(1+math.exp(-1*par_s[i]*(float(row[i+4])-par_i[i]))))
    output_writer.writerow(col_temp)
    col_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Generating a csv file containing the numbers we need to plot P-V graphs
output1_file = open("D:/Anomaly.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("D:/Volume.csv", "wb")
output2_writer = csv.writer(output2_file)
thresholds = list(numpy.arange(0, 1, 0.05))
NumAnomaly = [0]*2
NumArea = [0]*2
for i in range(len(thresholds)):
    input_file = open("D:/Fuzzy Scores.csv")
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
