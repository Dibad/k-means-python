import argparse
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans as KMeansSK
from tabulate import tabulate

from .instance_loader import InstanceLoader
from .kmeans import KMeans
from .kmeans_math import KMeansMath


def main(args):
    # Load the dataset from the file/predefined dataset
    X = InstanceLoader.load_dataset(args.dataset)
    print(f"Datased loaded.\n{X}")

    # Create a KMeans instance using the arguments passed through the console
    kmeans = KMeans(
        n_clusters=args.n_clusters,
        init=args.init,
        n_init=args.n_init,
        n_jobs=args.n_jobs,
    )

    if args.run_verbose:
        kmeans_run_verbose(X, kmeans)

    elif args.fit_verbose:
        kmeans_fit_verbose(X, kmeans)

    else:
        skmeans = KMeansSK(
            n_clusters=args.n_clusters, n_init=args.n_init, n_jobs=args.n_jobs
        )
        compare_kmeans(X, kmeans, skmeans)


def kmeans_run_verbose(X, kmeans):

    results = kmeans.run_full_output(X)

    headers = ["Centroids", "Labels", "Iteration", "SSE", "CPU"]
    print(tabulate(results, headers=headers))

    kmeans_animation(X, results)

    plt.show()


def kmeans_fit_verbose(X, kmeans):

    results = kmeans.fit_full_output(X)

    headers = ["Centroids", "Labels", "Iteration", "SSE", "CPU"]
    print(tabulate(results, headers=headers))

    kmeans_animation(X, results)

    plt.show()


def compare_kmeans(X, kmeans, skmeans):
    # -- Print result for the KMeans implementation
    print("Personal KMeans implementation:")
    output_kmeans(kmeans, X)
    plot_kmeans(
        plt.figure(),
        X,
        kmeans.cluster_centers_,
        kmeans.labels_,
        f"Personal KMeans implementation.\n"
        f"Iterations before convergence: {kmeans.n_iter_}. "
        f"SSE: {KMeansMath.sse(X, kmeans.cluster_centers_, kmeans.labels_).round(4)}",
    )

    # -- Print result for the sklearn KMeans implementation
    print("SKLearn KMeans implementation:")
    output_kmeans(skmeans, X)
    plot_kmeans(
        plt.figure(),
        X,
        skmeans.cluster_centers_,
        skmeans.labels_,
        f"SKLearn KMeans implementation.\n"
        f" Iterations before convergence: {skmeans.n_iter_}.  "
        f"SSE: {KMeansMath.sse(X, skmeans.cluster_centers_, skmeans.labels_).round(4)}",
    )

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


def plot_kmeans(fig, X, centroids, labels, title):
    fig.suptitle(title)

    dimension = X.shape[1]
    if dimension == 2:
        ax = fig.add_subplot(111)
        ax.scatter(X[:, 0], X[:, 1], c=labels)
        ax.scatter(centroids[:, 0], centroids[:, 1], s=130, marker="x")

    elif dimension >= 3:
        ax = fig.add_subplot(111, projection=Axes3D.name)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels)
        ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], s=130, marker="x")


def kmeans_animation(X, data):
    fig = plt.figure()

    def update_plot(i):
        fig.clear()
        plot_kmeans(fig, X, data[i][0], data[i][1], f"Iteration {i}. SSE: {data[i][3]}")

    _ = animation.FuncAnimation(
        fig, update_plot, interval=400, frames=len(data), repeat=True
    )

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="KMeans implementation, compared with SKLearn implementation"
    )
    parser.add_argument(
        "dataset",
        metavar="dataset",
        type=str,
        help="Path to the .txt file with the dataset to load, or one of the predefined "
        "datasets: (iris, blobs).",
    )
    parser.add_argument(
        "--init",
        help="(random|kpp) Method used for determine the first clusters",
        default="k-means-++",
        type=str,
    )
    parser.add_argument(
        "--n-clusters", help="Number of clusters to find", default=3, type=int
    )
    parser.add_argument(
        "--n-init",
        help="Number of times to execute KMeans before returning a cluster",
        default=15,
        type=int,
    )
    parser.add_argument(
        "--n-jobs",
        help="Number of process to execute in parallel with KMeans instances",
        default=8,
        type=int,
    )
    parser.add_argument(
        "--run-verbose",
        help="Verbose output of only one KMeans run with the loaded dataset.",
        action="store_true",
    )
    parser.add_argument(
        "--fit-verbose",
        help="Verbose output of all the KMeans runs generated while seraching the"
        "lowest SSE",
        action="store_true",
    )

    main(parser.parse_args())
