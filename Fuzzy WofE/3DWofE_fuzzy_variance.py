# Determining the variance resulting from the membership function
# ----------------------------------------------------------------
import csv
import itertools

# NumT: total number of voxels
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Input.csv")
input_reader = csv.reader(input_file)
NumT = 0
for row in input_reader:
    NumT += 1
del input_file
del input_reader
NumT = float(NumT)

# NumD: number of known mineralization-bearing voxels
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Input.csv")
input_reader = csv.reader(input_file)
threshold = 0.4
NumD = 0
for row in input_reader:
    if float(row[3]) > threshold:
        NumD += 1
del input_file
del input_reader
NumD = float(NumD)

# P(D)
ProD = NumD/NumT

# Number of factors
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Input.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    num_fac = len(row)-4
    break
del input_file
del input_reader

# P(B)
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumB.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB.csv", "wb")
output_writer = csv.writer(output_file)
ProB_temp = []
for row in input_reader:
    for i in range(num_fac):
        ProB_temp.append(float(row[i])/NumT)
    output_writer.writerow(ProB_temp)
    ProB_temp = []
del input_file
del input_reader
del output_file
del output_writer

# P(B_abs)
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumB.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProB_abs_temp = []
for row in input_reader:
    for i in range(num_fac):
        ProB_abs_temp.append(1-(float(row[i])/NumT))
    output_writer.writerow(ProB_abs_temp)
    ProB_abs_temp = []
del input_file
del input_reader
del output_file
del output_writer

# P(D|B)
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumBD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB.csv", "wb")
output_writer = csv.writer(output_file)
ProDB_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        ProDB_temp.append(float(row2[i])/float(row1[i]))
    output_writer.writerow(ProDB_temp)
    ProDB_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# (P(D|B_abs)
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/NumB_absD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProDB_abs_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        ProDB_abs_temp.append(float(row2[i])/(NumT-float(row1[i])))
    output_writer.writerow(ProDB_abs_temp)
    ProDB_abs_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# Var[P(D)]
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB_abs.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB.csv")
input3_reader = csv.reader(input3_file)
input4_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB_abs.csv")
input4_reader = csv.reader(input4_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD.csv", "wb")
output_writer = csv.writer(output_file)
Var_ProD_temp = []
for row1, row2, row3, row4 in itertools.izip(input1_reader, input2_reader, input3_reader, input4_reader):
    for i in range(num_fac):
        Var_ProD_temp.append(((float(row3[i])-ProD)**2)*(float(row1[i]))+((float(row4[i])-ProD)**2)*(float(row2[i])))
    output_writer.writerow(Var_ProD_temp)
    Var_ProD_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del input4_file
del input4_reader
del output_file
del output_writer

# The variance because of mis-assigned evidence from B to B_abs or from B_abs to B
# Var[P(D)]_B to B_abs
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB_abs.csv")
input3_reader = csv.reader(input3_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD_B.csv", "wb")
output_writer = csv.writer(output_file)
Var_ProD_B_temp = []
for row1, row2, row3 in itertools.izip(input1_reader, input2_reader, input3_reader):
    for i in range(num_fac):
        Var_ProD_B_temp.append(((float(row3[i])-float(row2[i]))**2)*(float(row1[i])))
    output_writer.writerow(Var_ProD_B_temp)
    Var_ProD_B_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del output_file
del output_writer

# Var[P(D)]_B_abs to B
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB_abs.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProDB_abs.csv")
input3_reader = csv.reader(input3_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD_B_abs.csv", "wb")
output_writer = csv.writer(output_file)
Var_ProD_B_abs_temp = []
for row1, row2, row3 in itertools.izip(input1_reader, input2_reader, input3_reader):
    for i in range(num_fac):
        Var_ProD_B_abs_temp.append(((float(row2[i])-float(row3[i]))**2)*(float(row1[i])))
    output_writer.writerow(Var_ProD_B_abs_temp)
    Var_ProD_B_abs_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del output_file
del output_writer

# Pro(Fuzzy Contrast)_B
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/ProB_abs.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Fuzzy Contrast.csv")
input3_reader = csv.reader(input3_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Pro_FC_B.csv", "wb")
output_writer = csv.writer(output_file)
Pro_FC_B_temp = []
for row1, row2, row3 in itertools.izip(input1_reader, input2_reader, input3_reader):
    for i in range(num_fac):
        Pro_FC_B_temp.append((float(row3[i])*float(row1[i]))+((1-float(row3[i]))*float(row2[i])))
    output_writer.writerow(Pro_FC_B_temp)
    Pro_FC_B_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del output_file
del output_writer

# Var[P(D)]_Fuzzy Contrast_B
input1_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Fuzzy Contrast.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Pro_FC_B.csv")
input2_reader = csv.reader(input2_file)
input3_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD.csv")
input3_reader = csv.reader(input3_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Variance/Var_ProD_FC_B.csv", "wb")
output_writer = csv.writer(output_file)
Var_ProD_FC_temp = []
for row1, row2, row3 in itertools.izip(input1_reader, input2_reader, input3_reader):
    for i in range(num_fac):
        Var_ProD_FC_temp.append(((2*float(row1[i])*(1-float(row1[i])))/float(row2[i]))*float(row3[i]))
    output_writer.writerow(Var_ProD_FC_temp)
    Var_ProD_FC_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del input3_file
del input3_reader
del output_file
del output_writer
