
import unittest
import numpy

from ode import LorenzEquation, ODESolver


class TestLorenzEquation(unittest.TestCase):
    def setUp(self):
        self.ode = LorenzEquation()
        self.solver = ODESolver(ode=self.ode)
        self.solver.initial_state = [10.,50.,50.]
        self.solver.t = numpy.linspace(0, 10, 1001)

    def test_eval(self):
        dX = self.ode.eval(self.solver.initial_state, 0.0)
        self.assertAlmostEqual(dX[0], 400)
        self.assertAlmostEqual(dX[1], -270)
        self.assertAlmostEqual(dX[2], 1100/3.)

    def test_solve(self):
        soln = self.solver.solution[1,:]
        self.assertAlmostEqual(soln[0], 13.65484958)
        self.assertAlmostEqual(soln[1], 46.64090341)
        self.assertAlmostEqual(soln[2], 54.35797299)

if __name__ == '__main__':
    unittest.main()
