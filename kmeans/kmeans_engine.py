import numpy as np

from kmeans_math import KMeansMath


class KMeansEngine:
    def __init__(self, n_clusters: int, n_init: int, max_iter: int, tol: float):
        self.n_clusters_: int = n_clusters
        self.n_init_: int = n_init
        self.max_iter_: int = max_iter
        self.tol_: float = tol

        # Default method to find initial centroids is random choice
        self.calc_initial_centroids = KMeansMath.random_centroids

        # Default method to find distance is euclidean distance
        self.calc_distance = KMeansMath.euclidean_distance

    def run(self, X):
        """
        Yield the centroids, labels and nº iteration
        """
        # Initialize empty centroids and labels
        centroids = self.calc_initial_centroids(X, self.n_clusters_)
        labels = np.empty(shape=(X.shape[0],), dtype=int)

        for i in range(1, self.max_iter_):
            # Execute the next iteration
            new_centroids, new_labels = self.__iter(X, centroids, labels)

            yield (new_centroids, new_labels, i)

            if self.__is_optimal(centroids, new_centroids):
                break
            else:
                centroids, labels = new_centroids, new_labels

    def __iter(self, X, centroids, labels):
        for i, point in enumerate(X):
            # Calculate the distance from the point to all the centroids
            distances = [self.calc_distance(point, centroid) for centroid in centroids]

            # The label is the index of the closest centroid
            label = distances.index(min(distances))
            # Update the labels array
            labels[i] = label

        centroids = KMeansMath.recalculate_centroids(X, centroids, labels)

        return centroids, labels

    def __is_optimal(self, old_centroids, new_centroids):
        for i in range(0, old_centroids.shape[0]):
            if np.sum(np.absolute(old_centroids[i] - new_centroids[i])) > self.tol_:
                return False

        return True