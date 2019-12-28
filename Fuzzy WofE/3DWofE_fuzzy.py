# Three-dimensional fuzzy weights of evidence prospectivity modeling
# The input files are ...
# -----------------------------------------------------------------------------------------------------------------
import csv
import itertools
import math
import pandas

# Determining the positive or negative weight of each voxel in binary models
input_file = open("D:/Binary_W_pos.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    binary_w_pos = row
del input_file
del input_reader

input_file = open("D:/Binary_W_neg.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    binary_w_neg = row
del input_file
del input_reader

input_file = open("D:/Input_Binary.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Weights_Binary.csv", "wb")
output_writer = csv.writer(output_file)
weights_binary_temp = []
for row in input_reader:
    weights_binary_temp.append(row[0])
    weights_binary_temp.append(row[1])
    weights_binary_temp.append(row[2])
    for i in range(len(row)-4):
        if float(row[i+4]) == 1:
            weights_binary_temp.append(binary_w_pos[i])
        else:
            weights_binary_temp.append(binary_w_neg[i])
    output_writer.writerow(weights_binary_temp)
    weights_binary_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Determining the fuzzy weight of each voxel in continuous models
input_file = open("D:/Input_Continuous.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    num_fac = len(row)-4
    break
del input_file
del input_reader

thresholds_continuous = []
fuzzyWeight = []
for i in range(num_fac):
    df1 = pandas.read_csv("D:/Thresholds_Continuous.csv", header=None, usecols=[i])
    thresholds_continuous_temp = df1[i].values.tolist()
    df2 = pandas.read_csv("D:/Fuzzy Weight.csv", header=None, usecols=[i])
    fuzzyWeight_temp = df2[i].values.tolist()
    thresholds_continuous.append(thresholds_continuous_temp)
    fuzzyWeight.append(fuzzyWeight_temp)

input_file = open("D:/Input_Continuous.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Weights_Continuous.csv", "wb")
output_writer = csv.writer(output_file)
weights_continuous_temp = []
for row in input_reader:
    weights_continuous_temp.append(row[0])
    weights_continuous_temp.append(row[1])
    weights_continuous_temp.append(row[2])
    for i in range(num_fac):
        for j in range(len(fuzzyWeight_temp)-1):
            if j == 0:
                if float(row[i+4]) <= thresholds_continuous[i][j]:
                    weights_continuous_temp.append(fuzzyWeight[i][j])
                    break
            elif j == len(fuzzyWeight_temp)-2:
                if thresholds_continuous[i][j-1] < float(row[i+4]) <= thresholds_continuous[i][j]:
                    weights_continuous_temp.append(fuzzyWeight[i][j])
                    break
                elif float(row[i+4]) > thresholds_continuous[i][j]:
                    weights_continuous_temp.append(fuzzyWeight[i][j+1])
                    break
            else:
                if thresholds_continuous[i][j-1] < float(row[i+4]) <= thresholds_continuous[i][j]:
                    weights_continuous_temp.append(fuzzyWeight[i][j])
                    break
    output_writer.writerow(weights_continuous_temp)
    weights_continuous_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Calculating the posterior probability
# NumT: total number of voxels
input_file = open("D:/Input_Continuous.csv")
input_reader = csv.reader(input_file)
NumT = 0
for row in input_reader:
    NumT += 1
del input_file
del input_reader
NumT = float(NumT)

# NumD: number of known mineralization-bearing voxels
input_file = open("D:/Input_Continuous.csv")
input_reader = csv.reader(input_file)
threshold = 0.4
NumD = 0
for row in input_reader:
    if float(row[3]) > threshold:
        NumD += 1
del input_file
del input_reader
NumD = float(NumD)

prior_p = NumD/NumT
prior_o = prior_p/(1-prior_p)
prior_l = math.log(prior_o)

input1_file = open("D:/Weights_Binary.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/Weights_Continuous.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/Posterior Logit.csv", "wb")
output_writer = csv.writer(output_file)
posterior_logit_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    posterior_logit_temp.append(row1[0])
    posterior_logit_temp.append(row1[1])
    posterior_logit_temp.append(row1[2])
    posterior_logit1_temp = [float(i) for i in row1]
    posterior_logit2_temp = [float(j) for j in row2]
    posterior_logit_temp.append(prior_l+sum(posterior_logit1_temp[3:])+sum(posterior_logit2_temp[3:]))
    output_writer.writerow(posterior_logit_temp)
    posterior_logit_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("D:/Posterior Logit.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Posterior Odds.csv", "wb")
output_writer = csv.writer(output_file)
posterior_odds_temp = []
for row in input_reader:
    posterior_odds_temp.append(row[0])
    posterior_odds_temp.append(row[1])
    posterior_odds_temp.append(row[2])
    posterior_odds_temp.append(math.exp(float(row[3])))
    output_writer.writerow(posterior_odds_temp)
    posterior_odds_temp = []
del input_file
del input_reader
del output_file
del output_writer

input_file = open("D:/Posterior Odds.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/Posterior Probability.csv", "wb")
output_writer = csv.writer(output_file)
posterior_probability_temp = []
for row in input_reader:
    posterior_probability_temp.append(row[0])
    posterior_probability_temp.append(row[1])
    posterior_probability_temp.append(row[2])
    posterior_probability_temp.append(float(row[3])/(1+float(row[3])))
    output_writer.writerow(posterior_probability_temp)
    posterior_probability_temp = []
del input_file
del input_reader
del output_file
del output_writer
