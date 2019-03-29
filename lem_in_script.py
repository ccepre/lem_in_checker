#!/usr/bin/env python
# coding: utf-8

import os
import time 
import subprocess
import sys
import numpy as np

# str_exec = input("nb exec : ")
# verif que la salle existe bien
# verif que chaque fourmis vienne d'une salle valide (connexion existante)
# time (1s) que si execution < 1 s

def check_step(line, nb_line) :
    actions = line.split(" L")
    actions = np.array([action.split("-", 1) for action in actions])
    min_len = min(map(len, actions))
    if (min_len < 2) :
        return "Wrong action format line " + str(nb_line)
    uniques, counts = np.unique(actions[:, 0], return_counts=True)
    nb_occur_ants = dict(zip(uniques, counts))
    uniques, counts = np.unique(actions[:, 1], return_counts=True)
    nb_occur_room = dict(zip(uniques, counts))
    if max(nb_occur_ants.values()) > 1 :
        return "Ant in multiple room line " + str(nb_line)
    if max(nb_occur_room.values()) > 1 :
        return "Multiple ants in a room line " + str(nb_line)
    return None 

def checker(output) :
    output = [line.rstrip("\n") for line in output]
    i = 0
    while i < len(output) :
        if output[i] == "" :
            break
        i += 1
    output_map = output[:i - 1]
    output = output[i + 1 :]
    for i in range(len(output)) :
        if (check_step(output[i], i) == 1) :
            return 1
    return 0

def display_summary(differences) :
    differences = sorted(differences)
    dict_diff = dict.fromkeys(set(differences), 0)
    total = sum(differences)
    for value in list(differences) :
        dict_diff[value] += 1
    print("\n------- SUMMARY ---------")
    print("Results : ", differences)
    print("\nMin : ", min(differences))
    print("Max : ", max(differences))
    print("Moyenne des differences : {} pour {} executions".format(\
            str(total / len(differences)), str(len(differences))))
    print("\nMAP : ")
    for key, value in dict_diff.items() :
        print("\t{} : {}".format(key, value))


if (len(sys.argv) == 2) :
    nbr = int(sys.argv[1])
    gen_arg = input("Entrer un argument pour le generateur.\n\
Par defaut --big-superposition\nArgument : ")
    differences = []
    nb_hard_map = 0
    limit = 15

    if gen_arg == "" : 
        gen_arg = "--big-superposition"
    for i in range(int(nbr)) :
        os.system("./maps/generator " + gen_arg + " > map")
        answer = os.popen("./lem-in < map").readlines()
        map_gen = os.popen("cat map").readlines()
        error_message = checker(answer)
        if error_message :
            os.system("mv map map_error")
            print(error_message + "\nThe map has been registered has map_error")
            break 
        goal_steps = (map_gen[1].split(" "))[-1]
        actual_steps = (answer[-1].split(" "))[-1]
        diff = int(actual_steps) - int(goal_steps)
        differences.append(diff)
        print(answer[0] + map_gen[1][1:-1])
        print("difference : " + str(diff))
        if diff >= limit :
            os.system("mv map map_hard_" + str(nb_hard_map))
            nb_hard_map += 1
        time.sleep(1)
    if error_message == None :
        display_summary(differences)
    os.system("rm map")
