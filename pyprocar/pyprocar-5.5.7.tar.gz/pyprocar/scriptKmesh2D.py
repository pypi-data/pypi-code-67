import numpy as np
from .splash import welcome


def generate2dkmesh(x1, y1, x2, y2, z, nkx, nky):
    """
	This module generates a KPOINTS mesh file for 2D plotting.
	"""
    welcome()

    kx = np.linspace(x1, x2, nkx)
    ky = np.linspace(y1, y2, nky)
    wf = open("Kgrid.dat", "w")
    wf.write("Generated by PyProcar\n")
    wf.write("%d\n" % (nkx * nky))
    wf.write("Reciprocal\n")
    for ikx in kx:
        for iky in ky:
            wf.write(
                " {: >12.7f}   {: >12.7f}   {: >12.7f}   {: >12.7f}\n".format(
                    ikx, iky, z, 1.0
                )
            )
    wf.close()
