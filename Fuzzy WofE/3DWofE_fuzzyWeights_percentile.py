# Calculating contrast, studentized contrast and fuzzy weight for continuous evidential models
# The input is a csv file with the following columns, respectively: X, Y, Z, Grade (Target Element), Fac1, Fac2, ...
# ------------------------------------------------------------------------------------------------------------------
import csv
import itertools
import math
import numpy
import pandas
import tqdm

# Number of factors
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    num_fac = len(row)-4
    break
del input_file
del input_reader

# Min and max of the target element
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Contrast/Input.csv")
input_reader = csv.reader(input_file)
col_temp = []
for row in input_reader:
    col_temp.append(float(row[3]))
del input_file
del input_reader
min_target = min(col_temp)
max_target = max(col_temp)

# Threshold values for the target element
# The number of classes are considered to be 10 here
num_class = 10
increment_target = (max_target-min_target)/num_class
thresholds_target = []
for i in range(1, num_class):
    thresholds_target.append(min_target+(i*increment_target))

# Thresholds for different factors
percentile = []
for i in range(num_class-1):
    percentile.append(100/num_class+(i*(100/num_class)))

thresholds_temp = []
thresholds = []
for i in range(num_fac):
    df = pandas.read_csv("D:/Input.csv", header=None, usecols=[i+4])
    input_temp = df[i+4].values.tolist()
    for p in percentile:
        thresholds_temp.append(numpy.percentile(input_temp, p))
    thresholds.append(thresholds_temp)
    thresholds_temp = []

thresholds_col = zip(*thresholds)
output_file = open("D:/Thresholds.csv", "wb")
output_writer = csv.writer(output_file)
output_writer.writerows(thresholds_col)
del output_file
del output_writer

# Calculating number of cells for different items
input_file = open("D:/Input.csv")
input_reader = csv.reader(input_file)
NumT = 0
for row in input_reader:
    NumT += 1
del input_file
del input_reader

NumD = [0]*(num_class-1)
for i in range(num_class-1):
    input_file = open("D:/Input.csv")
    input_reader = csv.reader(input_file)
    for row in input_reader:
        if float(row[3]) > thresholds_target[i]:
            NumD[i] += 1
del input_file
del input_reader

NumB = []
NumB_temp = [0]*num_class
for i in tqdm.tqdm(range(num_fac), desc="Factors"):
    df = pandas.read_csv("D:/Thresholds.csv", header=None, usecols=[i])
    thresholds_temp = df[i].values.tolist()
    for j in range(num_class-1):
        input_file = open("D:/Input.csv")
        input_reader = csv.reader(input_file)
        for row in input_reader:
            if j == 0:
                if float(row[i+4]) <= thresholds_temp[j]:
                    NumB_temp[j] += 1
            elif j == num_class-2:
                if thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                    NumB_temp[j] += 1
                elif float(row[i+4]) > thresholds_temp[j]:
                    NumB_temp[j+1] += 1
            else:
                if thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                    NumB_temp[j] += 1
    NumB.append(NumB_temp)
    NumB_temp = [0]*num_class
del input_file
del input_reader

NumB_col = zip(*NumB)
output_file = open("D:/NumB.csv", "wb")
output_writer = csv.writer(output_file)
output_writer.writerows(NumB_col)
del output_file
del output_writer

NumBD = []
NumB_absD = []
NumBD_abs = []
NumB_absD_abs = []
NumBD_temp = [0]*num_class
NumB_absD_temp = [0]*num_class
NumBD_abs_temp = [0]*num_class
NumB_absD_abs_temp = [0]*num_class
for threshold in tqdm.tqdm(thresholds_target, desc="Target thresholds"):
    for i in range(num_fac):
        df = pandas.read_csv("D:/Thresholds.csv", header=None, usecols=[i])
        thresholds_temp = df[i].values.tolist()
        for j in range(num_class-1):
            input_file = open("D:/Input.csv")
            input_reader = csv.reader(input_file)
            for row in input_reader:
                if j == 0:
                    if float(row[3]) > threshold and float(row[i+4]) <= thresholds_temp[j]:
                        NumBD_temp[j] += 1
                    elif float(row[3]) > threshold and float(row[i+4]) > thresholds_temp[j]:
                        NumB_absD_temp[j] += 1
                    elif float(row[3]) <= threshold and float(row[i+4]) <= thresholds_temp[j]:
                        NumBD_abs_temp[j] += 1
                    elif float(row[3]) <= threshold and float(row[i+4]) > thresholds_temp[j]:
                        NumB_absD_abs_temp[j] += 1
                elif j == num_class-2:
                    m = 1
                    n = 1
                    while m == 1:
                        if float(row[3]) > threshold and thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                            NumBD_temp[j] += 1
                            m += 1
                        elif float(row[3]) > threshold and float(row[i+4]) <= thresholds_temp[j-1]:
                            NumB_absD_temp[j] += 1
                            m += 1
                        elif float(row[3]) > threshold and float(row[i+4]) > thresholds_temp[j]:
                            NumB_absD_temp[j] += 1
                            m += 1
                        elif float(row[3]) <= threshold and thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                            NumBD_abs_temp[j] += 1
                            m += 1
                        elif float(row[3]) <= threshold and float(row[i+4]) <= thresholds_temp[j-1]:
                            NumB_absD_abs_temp[j] += 1
                            m += 1
                        elif float(row[3]) <= threshold and float(row[i+4]) > thresholds_temp[j]:
                            NumB_absD_abs_temp[j] += 1
                            m += 1
                    while n == 1:
                        if float(row[3]) > threshold and float(row[i+4]) > thresholds_temp[j]:
                            NumBD_temp[j+1] += 1
                            n += 1
                        elif float(row[3]) > threshold and float(row[i+4]) <= thresholds_temp[j]:
                            NumB_absD_temp[j+1] += 1
                            n += 1
                        elif float(row[3]) <= threshold and float(row[i+4]) > thresholds_temp[j]:
                            NumBD_abs_temp[j+1] += 1
                            n += 1
                        elif float(row[3]) <= threshold and float(row[i+4]) <= thresholds_temp[j]:
                            NumB_absD_abs_temp[j+1] += 1
                            n += 1
                else:
                    if float(row[3]) > threshold and thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                        NumBD_temp[j] += 1
                    elif float(row[3]) > threshold and float(row[i+4]) <= thresholds_temp[j-1]:
                        NumB_absD_temp[j] += 1
                    elif float(row[3]) > threshold and float(row[i+4]) > thresholds_temp[j]:
                        NumB_absD_temp[j] += 1
                    elif float(row[3]) <= threshold and thresholds_temp[j-1] < float(row[i+4]) <= thresholds_temp[j]:
                        NumBD_abs_temp[j] += 1
                    elif float(row[3]) <= threshold and float(row[i+4]) <= thresholds_temp[j-1]:
                        NumB_absD_abs_temp[j] += 1
                    elif float(row[3]) <= threshold and float(row[i+4]) > thresholds_temp[j]:
                        NumB_absD_abs_temp[j] += 1
        NumBD.append(NumBD_temp)
        NumB_absD.append(NumB_absD_temp)
        NumBD_abs.append(NumBD_abs_temp)
        NumB_absD_abs.append(NumB_absD_abs_temp)
        NumBD_temp = [0]*num_class
        NumB_absD_temp = [0]*num_class
        NumBD_abs_temp = [0]*num_class
        NumB_absD_abs_temp = [0]*num_class
del input_file
del input_reader

output_file = open("D:/NumBD.csv", "wb")
output_writer = csv.writer(output_file)
NumBD_temp = []
for i in range(num_class-1):
    for j in range(num_class):
        for k in range(num_fac):
            NumBD_temp.append(NumBD[(num_fac*i)+k][j])
        output_writer.writerow(NumBD_temp)
        NumBD_temp = []
del output_file
del output_writer

output_file = open("D:/NumB_absD.csv", "wb")
output_writer = csv.writer(output_file)
NumB_absD_temp = []
for i in range(num_class-1):
    for j in range(num_class):
        for k in range(num_fac):
            NumB_absD_temp.append(NumB_absD[(num_fac*i)+k][j])
        output_writer.writerow(NumB_absD_temp)
        NumB_absD_temp = []
del output_file
del output_writer

output_file = open("D:/NumBD_abs.csv", "wb")
output_writer = csv.writer(output_file)
NumBD_abs_temp = []
for i in range(num_class-1):
    for j in range(num_class):
        for k in range(num_fac):
            NumBD_abs_temp.append(NumBD_abs[(num_fac*i)+k][j])
        output_writer.writerow(NumBD_abs_temp)
        NumBD_abs_temp = []
del output_file
del output_writer

output_file = open("D:/NumB_absD_abs.csv", "wb")
output_writer = csv.writer(output_file)
NumB_absD_abs_temp = []
for i in range(num_class-1):
    for j in range(num_class):
        for k in range(num_fac):
            NumB_absD_abs_temp.append(NumB_absD_abs[(num_fac*i)+k][j])
        output_writer.writerow(NumB_absD_abs_temp)
        NumB_absD_abs_temp = []
del output_file
del output_writer

# Calculating required probabilities, odds and logits
input_file = open("D:/NumBD.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/ProBD.csv", "wb")
output_writer = csv.writer(output_file)
ProBD_temp = []
i = 1
j = 0
for row in input_reader:
    if i > num_class:
        j += 1
        i = 1
        for k in range(num_fac):
            ProBD_temp.append(float(row[k])/NumD[j])
    else:
        for k in range(num_fac):
            ProBD_temp.append(float(row[k])/NumD[j])
    output_writer.writerow(ProBD_temp)
    ProBD_temp = []
    i += 1
del input_file
del input_reader
del output_file
del output_writer

output_file = open("D:/NumB_Copied.csv", "wb")
output_writer = csv.writer(output_file)
i = 1
while i < num_class:
    input_file = open("D:/NumB.csv")
    input_reader = csv.reader(input_file)
    for row in input_reader:
        output_writer.writerow(row)
    i += 1
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("D:/NumB_Copied.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/NumBD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/ProBD_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProBD_abs_temp = []
i = 1
j = 0
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    if i > num_class:
        j += 1
        i = 1
        for k in range(num_fac):
            ProBD_abs_temp.append((float(row1[k])-float(row2[k]))/(NumT-NumD[j]))
    else:
        for k in range(num_fac):
            ProBD_abs_temp.append((float(row1[k])-float(row2[k]))/(NumT-NumD[j]))
    output_writer.writerow(ProBD_abs_temp)
    ProBD_abs_temp = []
    i += 1
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("D:/NumBD.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/ProB_absD.csv", "wb")
output_writer = csv.writer(output_file)
ProB_absD_temp = []
i = 1
j = 0
for row in input_reader:
    if i > num_class:
        j += 1
        i = 1
        for k in range(num_fac):
            ProB_absD_temp.append((NumD[j]-float(row[k]))/NumD[j])
    else:
        for k in range(num_fac):
            ProB_absD_temp.append((NumD[j]-float(row[k]))/NumD[j])
    output_writer.writerow(ProB_absD_temp)
    ProB_absD_temp = []
    i += 1
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("D:/NumB_Copied.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/NumBD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/ProB_absD_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProB_absD_abs_temp = []
i = 1
j = 0
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    if i > num_class:
        j += 1
        i = 1
        for k in range(num_fac):
            ProB_absD_abs_temp.append((NumT-float(row1[k])-NumD[j]+float(row2[k]))/(NumT-NumD[j]))
    else:
        for k in range(num_fac):
            ProB_absD_abs_temp.append((NumT-float(row1[k])-NumD[j]+float(row2[k]))/(NumT-NumD[j]))
    output_writer.writerow(ProB_absD_abs_temp)
    ProB_absD_abs_temp = []
    i += 1
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input1_file = open("D:/ProBD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/ProBD_abs.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/LS.csv", "wb")
output_writer = csv.writer(output_file)
LS_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row2[i]) != 0:
            LS_temp.append(float(row1[i])/float(row2[i]))
        else:
            LS_temp.append("Null")
    output_writer.writerow(LS_temp)
    LS_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("D:/LS.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/W_pos.csv", "wb")
output_writer = csv.writer(output_file)
W_pos_temp = []
for row in input_reader:
    for i in range(num_fac):
        if row[i] != "Null" and float(row[i]) != 0:
            W_pos_temp.append(math.log(float(row[i])))
        else:
            W_pos_temp.append("Null")
    output_writer.writerow(W_pos_temp)
    W_pos_temp = []
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("D:/ProB_absD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/ProB_absD_abs.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/LN.csv", "wb")
output_writer = csv.writer(output_file)
LN_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row2[i]) != 0:
            LN_temp.append(float(row1[i])/float(row2[i]))
        else:
            LN_temp.append("Null")
    output_writer.writerow(LN_temp)
    LN_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("D:/LN.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/W_neg.csv", "wb")
output_writer = csv.writer(output_file)
W_neg_temp = []
for row in input_reader:
    for i in range(num_fac):
        if row[i] != "Null" and float(row[i]) != 0:
            W_neg_temp.append(math.log(float(row[i])))
        else:
            W_neg_temp.append("Null")
    output_writer.writerow(W_neg_temp)
    W_neg_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Calculating contrast
input1_file = open("D:/W_pos.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/W_neg.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/Contrast.csv", "wb")
output_writer = csv.writer(output_file)
contrast_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null":
            contrast_temp.append(float(row1[i])-float(row2[i]))
        else:
            contrast_temp.append("Null")
    output_writer.writerow(contrast_temp)
    contrast_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# Calculating variance and standard deviation of positive and negative weights
input1_file = open("D:/NumBD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/NumBD_abs.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("D:/Var_W_pos.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("D:/StD_W_pos.csv", "wb")
output2_writer = csv.writer(output2_file)
var_w_pos_temp = []
std_w_pos_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row1[i]) != 0 and float(row2[i]) != 0:
            var_w_pos_temp.append((1/float(row1[i]))+(1/float(row2[i])))
            std_w_pos_temp.append(math.sqrt((1/float(row1[i]))+(1/float(row2[i]))))
        else:
            var_w_pos_temp.append("Null")
            std_w_pos_temp.append("Null")
    output1_writer.writerow(var_w_pos_temp)
    output2_writer.writerow(std_w_pos_temp)
    var_w_pos_temp = []
    std_w_pos_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

input1_file = open("D:/NumB_absD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/NumB_absD_abs.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("D:/Var_W_neg.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("D:/StD_W_neg.csv", "wb")
output2_writer = csv.writer(output2_file)
var_w_neg_temp = []
std_w_neg_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row1[i]) != 0 and float(row2[i]) != 0:
            var_w_neg_temp.append((1/float(row1[i]))+(1/float(row2[i])))
            std_w_neg_temp.append(math.sqrt((1/float(row1[i]))+(1/float(row2[i]))))
        else:
            var_w_neg_temp.append("Null")
            std_w_neg_temp.append("Null")
    output1_writer.writerow(var_w_neg_temp)
    output2_writer.writerow(std_w_neg_temp)
    var_w_neg_temp = []
    std_w_neg_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

# Calculating variance and standard deviation of contrasts
input1_file = open("D:/Var_W_pos.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/Var_W_neg.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("D:/Var_Contrast.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("D:/StD_Contrast.csv", "wb")
output2_writer = csv.writer(output2_file)
var_contrast_temp = []
std_contrast_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null":
            var_contrast_temp.append(float(row1[i])+float(row2[i]))
            std_contrast_temp.append(math.sqrt(float(row1[i])+float(row2[i])))
        else:
            var_contrast_temp.append("Null")
            std_contrast_temp.append("Null")
    output1_writer.writerow(var_contrast_temp)
    output2_writer.writerow(std_contrast_temp)
    var_contrast_temp = []
    std_contrast_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

# Calculating studentized contrast
input1_file = open("D:/Contrast.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/StD_Contrast.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/Contrast_Studentized.csv", "wb")
output_writer = csv.writer(output_file)
contrast_stu_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null" and float(row2[i]) != 0:
            contrast_stu_temp.append(float(row1[i])/float(row2[i]))
        else:
            contrast_stu_temp.append("Null")
    output_writer.writerow(contrast_stu_temp)
    contrast_stu_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# Calculating fuzzy contrast
contrast2_temp = []
fuzzyContrast_temp = []
fuzzyContrast = []
for i in range(num_fac):
    df = pandas.read_csv("D:/Contrast.csv", header=None, usecols=[i])
    contrast_temp = df[i].values.tolist()
    for j in range(num_class-1):
        contrast1_temp = (contrast_temp[j*num_class:((j*num_class)+num_class)])
        for k in range(num_class):
            if contrast1_temp[k] != "Null":
                contrast1_temp[k] = float(contrast1_temp[k])
        for m in range(num_class):
            if contrast1_temp[m] != "Null":
                contrast2_temp.append(contrast1_temp[m])
        if len(contrast2_temp) != 1:
            par_s = (2*math.log(99))/(max(contrast2_temp)-min(contrast2_temp))
            par_i = (max(contrast2_temp)+min(contrast2_temp))/2
            for n in range(num_class):
                if contrast1_temp[n] == "Null":
                    fuzzyContrast_temp.append(0.5)
                else:
                    fuzzyContrast_temp.append(1/(1+math.exp(-1*par_s*(float(contrast1_temp[n])-par_i))))
            fuzzyContrast.append(fuzzyContrast_temp)
            contrast1_temp = []
            fuzzyContrast_temp = []
        else:
            for p in range(num_class):
                if contrast1_temp[p] == "Null":
                    fuzzyContrast_temp.append(0.5)
                else:
                    fuzzyContrast_temp.append("Refer to contrast")
            fuzzyContrast.append(fuzzyContrast_temp)
            contrast1_temp = []
            fuzzyContrast_temp = []

output_file = open("D:/Fuzzy Contrast.csv", "wb")
output_writer = csv.writer(output_file)
fuzzyContrast_temp = []
for i in range(num_class-1):
    for j in range(num_class):
        for k in range(num_fac):
            fuzzyContrast_temp.append(fuzzyContrast[((num_class-1)*k)+i][j])
        output_writer.writerow(fuzzyContrast_temp)
        fuzzyContrast_temp = []
del output_file
del output_writer

# Calculating fuzzy weight
input1_file = open("D:/Fuzzy Contrast.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/ProBD.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/ProB_absD.csv")
input3_reader = csv.reader(input3_file)
input4_file = open("D:/ProBD_abs.csv")
input4_reader = csv.reader(input4_file)
input5_file = open("D:/ProB_absD_abs.csv")
input5_reader = csv.reader(input5_file)
output_file = open("D:/Fuzzy Weight.csv", "wb")
output_writer = csv.writer(output_file)
fuzzyWeight_temp = []
for row1, row2, row3, row4, row5 in itertools.izip(input1_reader, input2_reader, input3_reader, input4_reader, input5_reader):
    for i in range(num_fac):
        if row1[i] == "Refer to contrast":
            fuzzyWeight_temp.append("Null")
        else:
            fuzzyWeight_temp.append(math.log(((float(row1[i])*float(row2[i]))+((1-float(row1[i]))*float(row3[i]))) /
                                             ((float(row1[i])*float(row4[i]))+((1-float(row1[i]))*float(row5[i])))))
    output_writer.writerow(fuzzyWeight_temp)
    fuzzyWeight_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del input4_file
del input4_reader
del input5_file
del input5_reader
del output_file
del output_writer
