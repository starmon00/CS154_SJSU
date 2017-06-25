#!/usr/bin/env python

from __future__ import division
import argparse
import random


def weight_checker(current_weight, max_weight):
    if current_weight >= max_weight:
        return True
    else:
        return False

def generate_profitRatio(items):
    profitableItems = []
    for item in items:
        if(item[2] == 0):
            profitRatio = (item[4] - item[3])
        else:
            profitRatio = (item[4] - item[3]) / item[2]    #resale value - cost / weight
        
        if profitRatio > 0:
            profitableItems.append((item[0],item[1],item[2],item[3],item[4],profitRatio))
    return profitableItems

def create_constraint_dictionary(constraints):
    constraint_dictionary = {}
    for constraint in constraints:
        for class_num in constraint:
          for unpairable in constraint:
              if (class_num != unpairable):
                  if (class_num not in constraint_dictionary):
                      constraint_dictionary[class_num] = []
                      constraint_dictionary[class_num].append(unpairable)
                  else:
                      if (unpairable not in constraint_dictionary[class_num]):
                          constraint_dictionary[class_num].append(unpairable)
    return constraint_dictionary

def check_weight_cost_constraint(item_weight, item_cost, current_weight,max_weight,total_money):
    if(current_weight + item_weight <= max_weight and total_money - item_cost >= 0):
        return True
    return False


def solve_MDK(P, M, N, C, items, constraints):
    
  max_weight = P
  cash = M
  
  current_weight = 0
  purchase_list = []
  mod_purchase_list = []

  profitableItems = generate_profitRatio(items)
  constraint_dictionary = create_constraint_dictionary(constraints)
  purchase_lists = []


  for i in range(-1, 10):
    count = 0
    purchase_list = []
    while len(profitableItems) > 0:
        item = random.choice(profitableItems)
        profitableItems.remove(item)
        if count > i:
          if(cash == 0 or current_weight == max_weight):
              break

          item_class = item[1]
          item_weight = item[2]
          item_cost = item[3]
          valid_input = True


          if (purchase_list == []):
              if(check_weight_cost_constraint(item_weight, item_cost, current_weight, max_weight, cash)):
                  purchase_list.append(item)
                  current_weight += item_weight
                  cash -= item_cost
          else:
              for purchasing_item in purchase_list:
                  purchasing_item_class = purchasing_item[1]
                  if (purchasing_item_class in constraint_dictionary):
                      if(item_class in constraint_dictionary[purchasing_item_class]):
                        valid_input = False
                        break
              if valid_input:
                  if (check_weight_cost_constraint(item_weight, item_cost, current_weight, max_weight, cash)):
                      purchase_list.append(item)
                      current_weight += item_weight
                      cash -= item_cost
        count+=1
    purchase_lists.append(purchase_list)
  
  max_resale = 0.0
  max_list = []
  for list in purchase_lists:
    curr_resale = 0.0
    for item in list:
      curr_resale+= item[4]
    if curr_resale > max_resale:
      max_resale = curr_resale
      max_list = list



  return max_list
  



def solve(P, M, N, C, items, constraints):

    list_to_filter = items
    final_list_MDK = solve_MDK(P,M,N,C, items, constraints)
    Filtered_items = []
    for item in final_list_MDK:
        filter_class = item[1]
        for itemf in list_to_filter:
            if filter_class == itemf[1]:
                list_to_filter.remove(itemf)

    final_list_class = solve_MDK(P,M,N,C, list_to_filter, constraints)


    MDK_profit = 0
    class_profit = 0
    
    for item in final_list_MDK:
        MDK_profit += item[4]
    for item in final_list_class:
        class_profit += item[4]
    print("MDK: " + str(MDK_profit))
    print("Class: " + str(class_profit))
    print("Most Profit: " + str(max(MDK_profit,class_profit)))
    if max(MDK_profit, class_profit) == MDK_profit:
        return final_list_MDK
    else:
        return final_list_class
    


def read_input(filename):
  """
  P: float (weight)
  M: float (total number of items)
  N: integer (
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      items.append((name, int(cls), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  items_chosen = solve(P, M, N, C, items, constraints)
  write_output(args.output_file, items_chosen)
