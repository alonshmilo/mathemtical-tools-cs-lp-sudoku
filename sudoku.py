#Alon Shmilovich
#JCE Jerusalem College of Engineering
#M.Sc Software Engineering


import pulp


def variable(i,j,k):

    return "x_{%d,%d,%d}" % (i,j,k)

class Sudoku:

    def __init__(self, m, n):
        """Ctor for Sudoku object. Will contain m and n for rows and columns"""
        #Initializing m rows and n columns
        self.m=m
        self.n=n
        total = m * n
        totalplus= total+1

        #Defining the problem
        self.s_model = pulp.LpProblem("SudokuProblem", pulp.LpMinimize)

        x_names = [variable(i,j,k)
                   for i in range(1, totalplus)
                   for j in range(1, totalplus)
                   for k in range(1, totalplus)]


        self.x = pulp.LpVariable("%s", x_names, lowBound=0,upBound=1, cat=pulp.LpInteger)

        for i in range(1, totalplus):
            for k in range(1, totalplus):
                self.s_model += sum([self.x[variable(i,j,k)]
                                     for j in range(1,totalplus)]) == 1

        for j in range(1, totalplus):
            for k in range(1, totalplus):
                self.s_model += sum([self.x[variable(i,j,k)]
                                     for i in range(1,totalplus)]) == 1

        for I in range(1, n):
            for J in range(1, m):
                i_min = (I-1) * m + 1
                j_min = (J-1) * n + 1
                block_ivalues = range(i_min, i_min + m)
                block_jvalues = range(j_min, j_min + n)

                for k in range(1, totalplus):
                    self.s_model += sum([self.x[variable(i,j,k)]
                                         for i in block_ivalues
                                         for j in block_jvalues]) == 1
        for i in range(1, totalplus):
            for j in range(1, totalplus):
                self.s_model += sum([self.x[variable(i,j,k)]
                                     for k in range(1, totalplus)]) == 1


    def get_cell_value(self, i, j):

        N = self.m * self.n

        for k in range(1, N+1):
            if self.x[variable(i,j,k)].value() == 1:
                return k
        return None

    def set_cell_value(self, i, j, k):
        if self.s_model.status != pulp.LpStatusNotSolved:
            return RuntimeError("Sudoku has already been solved")

        self.s_model += self.x[variable(i,j,k)] == 1

    def solveProb(self):

        status = self.s_model.solve(pulp.GLPK(msg=0))
        return status == pulp.LpStatusOptimal


