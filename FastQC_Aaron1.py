# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 12:16:51 2021

@author: ajr88
"""

import os
import subprocess
import sys
import argparse


print("Enter outfile name")
directoryanme = input()
outdir = os.mkdir(directoryanme)
print("Enter location of FastQC")
FastQC= [] 
FastQC.append(input())
print("Enter input file location")
FastQC.append(input())
print("Enter outfile name")
FastQC.append('-o') 
FastQC.append(directoryanme) 
subprocess.call(FastQC)
