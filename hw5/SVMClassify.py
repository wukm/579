#!/usr/bin/env python3
"""
SVMClassify.py

use a support vector machine to create a classification scheme 

X -> matrix of training points
     each row represents a training point

y -> class labels for each data point

C -> parameter. higher values will be more accurate.
     for a 'hard-margin' pass C = numpy.inf (i.e. infinity)
"""

import numpy
from scipy.linalg import norm
from PROJECT import project

def svm_classify(X, y, C, tol=.001, dt=.001):
    """
    input X, y, C
    returns γ
   
    NOTE
    for hard margin just pass C = numpy.inf
    gradient descent w/ log functions
    """

    # please get to the bottom of the dimensionality issues from before
    #if len(y.shape) == 1:
    #    numpy.expand_dims(y, axis=0)

    gamma = numpy.zeros((X.shape[0], 1))

    dt, TOL, itmax = dt, tol, 20000
    it = 1

    while True:
        
        it += 1

        p = gradient(gamma, X, y)
        dt = line_search(dt, p, gamma, X, y, C)

        gamma_new = project(gamma - dt*p, y, C)

        q = (gamma_new - gamma) / dt

        if (norm(q) < TOL):
            break
        elif (it > itmax):
            break
        else:
            gamma = gamma_new

    return gamma_new

def gradient(gamma, X, y):
    """
    grad(E(γ)) = X(X^T)γ - y
    """
    # do it in two steps, might save memory?
    p = X.T.dot(gamma)
    p = X.dot(p) - y

    return p

def line_search(dt, p, gamma, X, y, C):
    """
    returns dt
    """
    # see class notes
    dt = 2.0 * dt
    
    # initial energy and initial gamma do not change throughout
    E = _energy(gamma, X, y, C)

    while True:
        gamma_new = project(gamma - dt*p, y, C)

        E_new = _energy(gamma_new, X, y, C)

        if E >= E_new + .001 * (gamma - gamma_new).T.dot(gamma - gamma_new):
            return dt
        else:
            dt = dt/2  # take a smaller timestep and try again

def _energy(gamma, X, y, C):
    """ 
    E(γ) = ½ <γ, X(X^T)γ> - <γ, y>
    """
    # build first term over multiple steps. idk if this is really more memory
    # efficent, but that was what was recommended in gradient. try it out?
    first = (X.T).dot(gamma)
    first = X.dot(first)
    first = gamma.T.dot(first) / 2

    second = gamma.T.dot(y) 
    
    return first - second
