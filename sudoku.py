#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
""" 

import sys
import copy
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"
domain_board = { ROW[r] + COL[c]: [1, 2, 3, 4, 5, 6, 7, 8, 9] for r in range(9) for c in range(9)}

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            try:
                ordered_vals.append(str(board[r + c]))
            except TypeError:
                continue
    return ''.join(ordered_vals)

#Constraint: no row should have same value
def removeRowValue(dom_board, cell, val):
    #Takes a board, cell('A1-I9'), value(0-9) and returns a board updating the domains
    test = copy.deepcopy(dom_board)
    for i in range(9):
        dom_cell = cell[0] + COL[i]
        if cell != dom_cell:
            try:
                test[dom_cell].remove(val)
            except ValueError:
                continue
    return test

#Constraint: no column should have same value
def removeColValue(dom_board, cell, val):
    #Takes a board, cell('A1-I9'), value(0-9) and returns a board updating the domains
    test = copy.deepcopy(dom_board)
    for i in range(9):
        dom_cell = ROW[i] + cell[1]
        if cell != dom_cell:
            try:
                test[dom_cell].remove(val)
            except ValueError:
                continue
    return test

#Constraint: no 3x3 square should have same value
def removeSquareValue(dom_board, cell, val):
    #Takes a board, cell('A1-I9'), value(0-9) and returns a board updating the domains
    test = copy.deepcopy(dom_board)
    pos = ROW.find(cell[0])
    startRow = int(pos/3) * 3
    startCol = int((int(cell[1])-1)/3) * 3
    for i in range(startRow, startRow+3):
        for j in range(startCol, startCol+3):
            dom_cell = ROW[i] + COL[j]
            if cell != dom_cell:
                try:
                    test[dom_cell].remove(val)
                except ValueError:
                    continue
    return test
    
#update the domain board based on the initial board dictionary
def initializeDomain(board, dom_board):
    for key in board.keys():
        if board[key] != 0:
            dom_board = removeRowValue(dom_board, key, board[key])
            dom_board = removeColValue(dom_board, key, board[key])
            dom_board = removeSquareValue(dom_board, key, board[key])
            dom_board[key] = [board[key]]
    return dom_board

#reset the domain board
def resetDomain():
    ans = { ROW[r] + COL[c]: [1, 2, 3, 4, 5, 6, 7, 8, 9] for r in range(9) for c in range(9)}
    return ans

def goalTest(board):
    for key in board.keys():
        if board[key] == 0:
            return False
    return True

def domainTruthTest(dom_board):
    for key in dom_board.keys():
        if len(dom_board[key]) == 0:
            return False
    return True

def backtracking(board, db):
    """Takes a board and returns solved board."""
    #goal test, return solved_board if sudoku is solved
    if goalTest(board) is True:
        solved_board = board
        return solved_board
    least = 10
    mrv_cell = ""
    #find the cell with the minimum remaining values in domain list
    for key in db.keys():
        size = len(db[key])
        if ((size == 1) and (board[key] == 0)):
            least = size
            mrv_cell = key
            break
        elif ((size < least) and (board[key] == 0)):
            least = size
            mrv_cell = key
            
    #loop through the domain values of MRV cell
    for val in db[mrv_cell]:
        board[mrv_cell] = val
        #inferences, constraint propogation
        inference_db = removeRowValue(db, mrv_cell, board[mrv_cell])
        inference_db = removeColValue(inference_db, mrv_cell, board[mrv_cell])
        inference_db = removeSquareValue(inference_db, mrv_cell, board[mrv_cell])
        #if inferences not equal to failure
        #add inferences to assignment
        if domainTruthTest(inference_db) is True:
            result = backtracking(board, inference_db)
            if result is not None:
                solved_board = result
                return solved_board
        board[mrv_cell] = 0
        #since variable assignment did not work remove inferences from assignment
    return None 
        
if __name__ == '__main__':        
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       

        domain_board = initializeDomain(board, domain_board)
        solved_board = backtracking(board, domain_board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        minTime = 100
        maxTime = 0
        boardsSolved = 0
        totalTime = 0
        ansTimes = []
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            if len(line) < 9:
                continue
            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            domain_board = resetDomain()
            domain_board = initializeDomain(board, domain_board)
            # Solve with backtracking
            start = time.time()
            solved_board = backtracking(board, domain_board)
            end = time.time()
            boardsSolved = boardsSolved + 1
            ans_time = end - start
            ansTimes.append(ans_time)
            totalTime = totalTime + ans_time
            if ans_time < minTime:
                minTime = ans_time
            if ans_time > maxTime:
                maxTime = ans_time
            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)
            
            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
        mean = statistics.mean(ansTimes)
        stdev = statistics.stdev(ansTimes)

        readme_filename = 'README.txt'
        readmefile = open(readme_filename, "w")

        l1 = "Number of boards solved: " + str(boardsSolved)
        readmefile.write(l1+"\n")
        readmefile.write("Running Time Statistics:"+"\n")
        l2 = "Min: " + str(minTime) + " seconds"
        readmefile.write(l2+"\n")
        l3 = "Max: " + str(maxTime) + " seconds"
        readmefile.write(l3+"\n")
        l4 = "Mean: " + str(mean) + " seconds"
        readmefile.write(l4+"\n")
        l5 = "Standard Deviation: " + str(stdev) + " seconds"
        readmefile.write(l5+"\n")
