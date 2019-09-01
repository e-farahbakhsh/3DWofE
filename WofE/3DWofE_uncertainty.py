# Creating total variance/uncertainty and studentized posterior probability models
# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Fac1, Fac2, ...
# -----------------------------------------------------------------------------------------------------------------
import csv
import itertools
import math

# Threshold value for the target element
threshold = 0.450155049344027
# A list of threshold values for the evidential models with respect to the input csv file
thresholds = [259.936009793948, 1424.6917112257, 73759.3058497416, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
              0.5, 0.5, 0.5, 0.5]
# A list of the variances calculated for the positive weights of the evidential models with respect to the
# input csv file
var_w_pos = [0.000300289945997081, 0.00390523028643939, 0.000953113314073704, 0.0243526300306134,
             0.309562145261069, 1.10843539887808, 0.266431393145319, 0.00752936671358174, 0.00354412099768136,
             0.00528459369117716, 0.000910454827955843, 0.00013605728252983, 0.000105761473267968]
# A list of the variances calculated for the negative weights of the evidential models with respect to the
# input csv file
var_w_neg = [0.000140916346670202, 0.0000982786652817642, 0.000107582462139783,
             0.0000990506894969525, 0.0000970232620425332, 0.000105772386407877, 0.000131755982005783,
             0.0000970679758929667, 0.0000985977549431225, 0.0000975996148877691, 0.000107107809844943,
             0.000324342270126537, 0.00102296302959494]

# Calculating the variance of each voxel in the evidential models
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Input.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance.csv", "wb")
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

# Calculating the total variance/uncertainty of each voxel
input_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Variance.csv")
input_reader = csv.reader(input_file)
output_file = open("D:/PhD-AUT/Thesis/Phase 02_Nochun/WofE/Uncertainty/Total Variance.csv", "wb")
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

# Calculating the studentized posterior probability
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
