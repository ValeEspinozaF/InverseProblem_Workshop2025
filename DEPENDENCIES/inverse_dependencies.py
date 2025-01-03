import numpy as np

def lsqr_solution(G, d, epsilon):
    '''Calculates the damped least squares solution with damping coefficient epsilon'''
    
    _, M = G.shape
    I = np.identity(M)
    
    # Solve A = G.T * G + epsilon^2 * I
    A = np.dot(G.T, G) + epsilon**2 * I
    
    # Solve m_est = A-1 * G.T * d_obs
    A_inv = np.linalg.inv(A)
    return np.dot( np.dot(A_inv, G.T), d )


def residual(d, G, m):
    '''Calculates the squared norm of the residual'''
    
    # Solve ||G * m_est|| ^2
    d_est = np.dot(G, m)
    return np.linalg.norm(d - d_est)**2


def find_optimal_epsilon(G, d, epsilon_values, noise_norm):
    '''Finds the optimal damping coefficient epsilon'''
    
    residuals = []
    
    for epsilon in epsilon_values:
        m_est = lsqr_solution(G, d, epsilon)
        residuals.append(np.abs( residual(d, G, m_est) - noise_norm**2 ))

    return epsilon_values[np.argmin(residuals)]