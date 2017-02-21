from __future__ import print_function
from ortools.linear_solver import pywraplp
import numpy as np

def main():
  # Instantiate a mixed-integer solver, naming it SolveIntegerProblem.

    graphA = np.zeros((10, 10))
    edge = [[0, 1], [1, 0], [1, 2], [2, 1], [0, 2], [0, 3], [3, 0], [0, 4], [4, 0],
          [4, 3], [3, 4], [2, 3], [3, 2], [2, 9], [9, 2], [5, 4], [5, 3], [3, 5],
          [3, 6], [5, 6], [6, 5], [6, 8], [8, 6], [6, 7], [7, 6], [8, 7], [7, 8],
          [8, 9], [2, 8], [8, 2]]
    for x in edge:
        graphA[x[0]][x[1]] = int(graphA[x[0]][x[1]] + 1)

    L = 25

    distance = np.array([
    [0.0, 3.0, 2.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [3.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 3.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 0.0, 5.0, 0.0, 1.0, 4.0, 3.0, 0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 4.0, 2.0, 0.0, 3.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0, 1.0, 2.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 5.0, 0.0],
    [0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 5.0, 0.0, 4.0],
    [0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

    fuel = np.array([
    [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])

    solver = pywraplp.Solver('SolveIntegerProblem',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)


    A = [["00","01","02","03","04","05","06","07","08","09"],
       ["10", "11", "12", "13", "14","15","16","17","18","19"],
       ["20", "21", "22", "23", "24","25","26","27","28","29"],
       ["30", "31", "32", "33", "34","35","36","37","38","39"],
       ["40", "41", "42", "43", "44","45","46","47","48","49"],
       ["50", "51", "52", "53", "54","55","56","57","58","59"],
       ["60", "61", "62", "63", "64","65","66","67","68","69"],
       ["70", "71", "72", "73", "74","75","76","77","78","79"],
       ["80", "81", "82", "83", "84","85","86","87","88","89"],
       ["90", "91", "92", "93", "94","95","96","97","98","99"]]
    B = [["000","010","020","030","040","050","060","070","080","090"],
       ["100", "110", "120", "130", "140","150","160","170","180","190"],
       ["200", "210", "220", "230", "240","250","260","270","280","290"],
       ["300", "310", "320", "330", "340","350","360","370","380","390"],
       ["400", "410", "420", "430", "440","450","460","470","480","490"],
       ["500", "510", "520", "530", "540","550","560","570","580","590"],
       ["600", "610", "620", "630", "640","650","660","670","680","690"],
       ["700", "710", "720", "730", "740","750","760","770","780","790"],
       ["800", "810", "820", "830", "840","850","860","870","880","890"],
       ["900", "910", "920", "930", "940","950","960","970","980","990"]]


    C = ["0","1","2","3","4","5","6","7","8","9"]
  # x and y are integer non-negative variables.
    for i in range(10):
        C[i] = solver.IntVar(0.0, 1.0, C[i])
        for j in range(10):
            A[i][j] = solver.IntVar(0.0, solver.infinity(),A[i][j])

    for i in range(10):
        for j in range(i + 1, 10):
            B[i][j] = solver.IntVar(0.0, 1.0, B[i][j])

  # x + 7 * y <= 17.5
    for i in range(10):
        for j in range(10):
            c = solver.Constraint(0,100*graphA[i][j])
            c.SetCoefficient(A[i][j], 1)


    for i in range(10):
        for j in  range(i+1,10):
            c1 = solver.Constraint(-0.9999,0)
            c1.SetCoefficient(A[i][j],0.001)
            c1.SetCoefficient(A[j][i],0.001)
            c1.SetCoefficient(B[i][j],-1)

    for i in range(10):
        for j in range(i+1,10):
            c2 = solver.Constraint(0,100)
            c2.SetCoefficient(B[i][j],-1)
            c2.SetCoefficient(C[i],0.5)
            c2.SetCoefficient(C[j],0.5)

    c3 =  solver.Constraint(1, 1)
    for i in range(10):
        c3.SetCoefficient(C[i], 1)
        for j in range(i+1,10):
            c3.SetCoefficient(B[i][j],-1)
  # x <= 3.5
    con = solver.Constraint(1, 1)
    for i in range(10):
        con.SetCoefficient(A[0][i], 1)
        con.SetCoefficient(A[i][0], -1)



    cons = solver.Constraint(-1, 0)
    for i in range(10):
        cons.SetCoefficient(A[i][7], -1)
        cons.SetCoefficient(A[7][i], 1)



    conw = solver.Constraint(0, L)
    for i in range(10):
        for j in range(10):
            conw.SetCoefficient(A[i][j],3*fuel[i][j])


    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[1][i], 1)
        cona.SetCoefficient(A[i][1], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[2][i], 1)
        cona.SetCoefficient(A[i][2], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[3][i], 1)
        cona.SetCoefficient(A[i][3], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[4][i], 1)
        cona.SetCoefficient(A[i][4], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[5][i], 1)
        cona.SetCoefficient(A[i][5], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[6][i], 1)
        cona.SetCoefficient(A[i][6], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[8][i], 1)
        cona.SetCoefficient(A[i][8], -1)

    cona = solver.Constraint(-1, 0)
    for i in range(0, 10):
        cona.SetCoefficient(A[9][i], 1)
        cona.SetCoefficient(A[i][9], -1)

  # Maximize x + 10 * y.
    objective = solver.Objective()
    for i in range(10):
        for j in range(10):
            objective.SetCoefficient(A[i][j],distance[i][j]-3*fuel[i][j])


    objective.SetMaximization()

    """Solve the problem and print the solution."""
    result_status = solver.Solve()
  # The problem has an optimal solution.
    assert result_status == pywraplp.Solver.OPTIMAL

  # The solution looks legit (when using solvers other than
  # GLOP_LINEAR_PROGRAMMING, verifying the solution is highly recommended!).
    assert solver.VerifySolution(1e-7, True)

    print('Number of variables =', solver.NumVariables())
    print('Number of constraints =', solver.NumConstraints())

  # The objective value of the solution.
    print('Optimal objective value = %d' % solver.Objective().Value())
    print()
  # The value of each variable in the solution.

    variable_list = [A[0][0],A[0][1],A[0][2],A[0][3],A[0][4],A[0][5],A[0][6],A[0][7],A[0][8],A[0][9],
                   A[1][0], A[1][1], A[1][2], A[1][3], A[1][4], A[1][5], A[1][6], A[1][7], A[1][8], A[1][9],
                   A[2][0], A[2][1], A[2][2], A[2][3], A[2][4], A[2][5], A[2][6], A[2][7], A[2][8], A[2][9],
                   A[3][0], A[3][1], A[3][2], A[3][3], A[3][4], A[3][5], A[3][6], A[3][7], A[3][8], A[3][9],
                   A[4][0], A[4][1], A[4][2], A[4][3], A[4][4], A[4][5], A[4][6], A[4][7], A[4][8], A[4][9],
                   A[5][0], A[5][1], A[5][2], A[5][3], A[5][4], A[5][5], A[5][6], A[5][7], A[5][8], A[5][9],
                   A[6][0], A[6][1], A[6][2], A[6][3], A[6][4], A[6][5], A[6][6], A[6][7], A[6][8], A[6][9],
                   A[7][0], A[7][1], A[7][2], A[7][3], A[7][4], A[7][5], A[7][6], A[7][7], A[7][8], A[7][9],
                   A[8][0], A[8][1], A[8][2], A[8][3], A[8][4], A[8][5], A[8][6], A[8][7], A[8][8], A[8][9],
                   A[8][0], A[9][1], A[9][2], A[9][3], A[9][4], A[9][5], A[9][6], A[9][7], A[9][8], A[9][9],
                   C[0],C[1],C[2],C[3],C[4],C[5],C[6],C[7],C[8],C[9]]
    for variable in variable_list:
        print('%s = %d' % (variable.name(), variable.solution_value()))


if __name__ == '__main__':
  main()