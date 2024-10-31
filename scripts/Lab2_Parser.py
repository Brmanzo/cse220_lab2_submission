#!/usr/bin/env python
import sys
import os
import re


# Class that represents the attributes of interest for each .out file
class MemoryStatInputParser:
    def __init__(self, input_lines):
        IPC_Line = 7 - 1
        DCache_Miss_line = 1456 - 1
        DCache_Hit_line = 1492  - 1
        DCache_Miss_Cap_Line = 14355 - 1
        DCache_Miss_Comp_Line = 14358 - 1
        DCache_Miss_Conf_Line = 14361 - 1

        # Goes to specified line in file, numbers stored in a list
        # Desired numbers appended assigned to object parameters
        self.ipc = re.findall(r'\d+', input_lines[IPC_Line])[0] + "." + re.findall(r'\d+', input_lines[IPC_Line])[1]
        print(str(self.ipc))
        DCACHE_MISS_count = re.findall(r'\d+', input_lines[DCache_Miss_line])[0]
        DCACHE_HIT_count = re.findall(r'\d+', input_lines[DCache_Hit_line])[0]

        DCACHE_CAP_count = re.findall(r'\d+', input_lines[DCache_Miss_Cap_Line])[0]
        DCACHE_COMP_count = re.findall(r'\d+', input_lines[DCache_Miss_Comp_Line])[0]
        DCACHE_CONF_count = re.findall(r'\d+', input_lines[DCache_Miss_Conf_Line])[0]

        self.dcache_miss_ratio = int(DCACHE_MISS_count) / (int(DCACHE_MISS_count) + int(DCACHE_HIT_count))
        self.dcache_cap_ratio = int(DCACHE_CAP_count) / (int(DCACHE_MISS_count) + int(DCACHE_HIT_count))
        self.dcache_comp_ratio = int(DCACHE_COMP_count) / (int(DCACHE_MISS_count) + int(DCACHE_HIT_count))
        self.dcache_conf_ratio = int(DCACHE_CONF_count) / (int(DCACHE_MISS_count) + int(DCACHE_HIT_count))
rootdir = os.path.dirname(os.path.realpath(__file__))

# data array initialized to hold a tensor for each file in directory
data = [""] * ((len(os.listdir(rootdir)) - 1)*7)
index = 1
data[index] = "IPC, DCache Miss Ratio\n"
index = index + 1
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith("memory.stat.0.csv"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                mem_parsed_input =  MemoryStatInputParser(lines)
                data[index] = str(mem_parsed_input.ipc) + ", " \
                            + str(mem_parsed_input.dcache_miss_ratio) + ", " \
                            + str(mem_parsed_input.dcache_cap_ratio) + ", " \
                            + str(mem_parsed_input.dcache_comp_ratio) + ", " \
                            + str(mem_parsed_input.dcache_conf_ratio) \
                            + "\n"
                #print(data[index])
                index += 1
# The second argument is the name of the new file
with open(sys.argv[1], 'w') as data_file:
    # read a list of lines into data
    data_file.writelines(data)
