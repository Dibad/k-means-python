# import matplotlib.pyplot as plt
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans as KMeansSK

from instance_loader import InstanceLoader
from kmeans import KMeans


def main():
    X = InstanceLoader.load_txt("res/prob1.txt")

    # -- Print result for my KMeans implementation
    kmeans = KMeans(n_clusters=3, n_init=100)
    print("Personal KMeans implementation:")
    output_kmeans(kmeans, X)
    plot_kmeans(
        kmeans,
        X,
        f"Personal KMeans implementation. Iterations before convergence: "
        f"{kmeans.n_iter_}",
    )

    # -- Print result for sklearn KMeans implementation
    skmeans = KMeansSK(n_clusters=3, n_init=100)
    print("SKLearn KMeans implementation:")
    output_kmeans(skmeans, X)
    plot_kmeans(
        kmeans,
        X,
        f"SKLearn KMeans implementation. Iterations before convergence: "
        f"{skmeans.n_iter_}",
    )

    dimension = X.shape[1]
    if dimension > 3:
        print(f"The dimension {dimension} is too high. Can't be represented")
    else:
        plt.show()


def output_kmeans(kmeans, X):
    # Fit the model
    start = time.clock()
    kmeans.fit(X)
    end = time.clock() - start

    # Print result
    print(f"\tCentroids:\n{kmeans.cluster_centers_}")
    print(f"\tLabels:\n{kmeans.labels_}")
    print(f"\tNº iter: {kmeans.n_iter_}")
    print(f"\tExecution time: {end}")
    print("\n")


def plot_kmeans(kmeans, X, title):
    fig = plt.figure()
    fig.suptitle(title)

    dimension = X.shape[1]
    if dimension == 2:
        ax = fig.add_subplot(111)
        ax.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
        ax.scatter(
            kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=130,
            marker="x",
        )
    elif dimension == 3:
        ax = fig.add_subplot(111, projection=Axes3D.name)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=kmeans.labels_)
        ax.scatter(
            kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            kmeans.cluster_centers_[:, 2],
            s=130,
            marker="x",
        )


if __name__ == "__main__":
    main()
