# Three-dimensional weights of evidence prospectivity modeling
# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Fac1, Fac2, ...
# -----------------------------------------------------------------------------------------------------------------
import csv
import math

# Calculating the number of voxels for different items
# NumT: total number of voxels
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
NumT = 0
for row in input_reader:
    NumT += 1
del input_file
del input_reader
NumT = float(NumT)

# NumD: number of known mineralization-bearing voxels
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
threshold = 0.4 # Replace with your desired number
NumD = 0
for row in input_reader:
    if float(row[3]) > threshold:
        NumD += 1
del input_file
del input_reader
NumD = float(NumD)

# NumB: number of anomalous voxels in evidential models
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
thresholds = [] # Fill this list with your desired numbers
NumB = [0]*len(thresholds)
for row in input_reader:
    for i in range(len(thresholds)):
        if float(row[i+4]) > thresholds[i]:
            NumB[i] += 1
del input_file
del input_reader

# NumBD: number of intersected mineralization-bearing voxels and anomalous voxels of evidential models
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
NumBD = [0]*len(thresholds)
for row in input_reader:
    for i in range(len(thresholds)):
        if float(row[3]) > threshold and float(row[i+4]) > thresholds[i]:
            NumBD[i] += 1
del input_file
del input_reader

# Calculating required probabilities, odds and logits
ProBD = []
for n in NumBD:
    ProBD.append(n/NumD)

# "_abs" means in the absence of the last character before "_"
ProBD_abs = []
i = 0
for n in NumB:
    ProBD_abs.append((n-NumBD[i])/(NumT-NumD))
    i += 1

ProB_absD = []
for n in NumBD:
    ProB_absD.append((NumD-n)/NumD)

ProB_absD_abs = []
i = 0
for n in NumB:
    ProB_absD_abs.append((NumT-n-NumD+NumBD[i])/(NumT-NumD))
    i += 1

LS = []
i = 0
for p in ProBD:
    LS.append(p/ProBD_abs[i])
    i += 1

W_pos = []
for i in LS:
    W_pos.append(math.log(i))

LN = []
i = 0
for p in ProB_absD:
    LN.append(p/ProB_absD_abs[i])
    i += 1

W_neg = []
for i in LN:
    W_neg.append(math.log(i))

prior_p = NumD/NumT

prior_o = prior_p/(1-prior_p)

prior_l = math.log(prior_o)

post_o_DB = []
for i in LS:
    post_o_DB.append(prior_o*i)

post_l_DB = []
for i in W_pos:
    post_l_DB.append(math.log(prior_o)+i)

post_o_DB_abs = []
for i in LN:
    post_o_DB_abs.append(prior_o*i)

post_l_DB_abs = []
for i in W_neg:
    post_l_DB_abs.append(math.log(prior_o)+i)

post_p_DB = []
for i in post_o_DB:
    post_p_DB.append(i/1+i)

post_p_DB_abs = []
for i in post_o_DB_abs:
    post_p_DB_abs.append(i/1+i)

# Combining evidential models
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Weights.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row in input_reader:
    row_temp.append(row[0])
    row_temp.append(row[1])
    row_temp.append(row[2])
    for i in range(len(thresholds)):
        if float(row[i+4]) > thresholds[i]:
            row_temp.append(W_pos[i])
        else:
            row_temp.append(W_neg[i])
    output_writer.writerow(row_temp)
    row_temp = []
del input_file
del input_reader
del output_file
del output_writer

input_file = open("D:/Weights.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Posterior Logit.csv", "wb")
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

input_file = open("D:/Posterior Logit.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Posterior Odds.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row in input_reader:
    row_temp.append(row[0])
    row_temp.append(row[1])
    row_temp.append(row[2])
    row_temp.append(math.exp(float(row[3])))
    output_writer.writerow(row_temp)
    row_temp = []
del input_file
del input_reader
del output_file
del output_writer

input_file = open("D:/Posterior Odds.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Posterior Probability.csv", "wb")
output_writer = csv.writer(output_file)
row_temp = []
for row in input_reader:
    row_temp.append(row[0])
    row_temp.append(row[1])
    row_temp.append(row[2])
    row_temp.append(float(row[3])/(1+float(row[3])))
    output_writer.writerow(row_temp)
    row_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Overall test of conditional independence
input_file = open("D:/Posterior Probability.csv")
input_reader = csv.reader(input_file)
list_temp = []
for row in input_reader:
    list_temp.append(float(row[3]))
del input_file
del input_reader
predictedNum = sum(list_temp)
