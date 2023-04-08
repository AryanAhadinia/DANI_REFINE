import numpy as np
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


def _co_occurrence(cascades, n):
    users_cascades = [set() for _ in range(n)]
    for cascade in cascades:
        for user, _ in cascade:
            users_cascades[user].add(cascade)
    co_occurrence_matrix = np.zeros((n, n))
    for u in range(n):
        for v in range(u + 1, n):
            co_occurrence_matrix[u, v] = co_occurrence_matrix[v, u] = len(
                users_cascades[u].intersection(users_cascades[v])
            )
    for u in range(n):
        normalizer_term = len(users_cascades[u])
        co_occurrence_matrix[u, :] /= normalizer_term if normalizer_term != 0 else 1
    return co_occurrence_matrix


def _reaction_time_matrix(cascades, n):
    r_inv = np.zeros((n, n))
    for c, cascade in enumerate(cascades):
        cascade_times = np.zeros(n)
        for user, time in cascade:
            cascade_times[user] = time
        matrix_of_differences = np.abs(np.subtract.outer(cascade_times, cascade_times))
        mask = cascade_times == 0
        matrix_of_differences[mask, :] = np.inf
        matrix_of_differences[:, mask] = np.inf
        r_inv_cascade = np.exp(-matrix_of_differences)
        r_inv += r_inv_cascade
    normalizer_term = np.sum(aggregated, axis=1)[:, np.newaxis]
    normalizer_term[normalizer_term == 0] = 1
    aggregated /= normalizer_term
    return aggregated


def _dimension_reduction(X, r):
    X = csr_matrix(X)
    svd = TruncatedSVD(n_components=r, random_state=42)
    X = svd.fit_transform(X)
    return X


def interaction_pattern(cascades, n, r):
    reaction_time = _reaction_time_matrix(cascades, n)
    co_occurrence = _co_occurrence(cascades, n)
    I = np.multiply(co_occurrence, reaction_time)
    I_r = _dimension_reduction(I, r)
    return I_r
