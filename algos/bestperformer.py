import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class BestPerformer:
    def find_perfomrer(self, data):

        X = np.nan_to_num(data[:, [1, 2]])
        scaler = StandardScaler()
        cluster_dataset = scaler.fit_transform(X)

        costs = []
        for i in range(1, 20):
            k_means = KMeans(init="k-means++", n_clusters=i, n_init=12)
            k_means.fit(cluster_dataset)
            labels = k_means.labels_
            costs.append(k_means.inertia_)
        # labels

        k_means = KMeans(init="k-means++", n_clusters=6, n_init=12)
        k_means.fit(cluster_dataset)
        labels = k_means.labels_

        data["Labels"] = labels

        plt.plot(range(1, 20), costs)
        plt.xlabel("Number of clusters")
        plt.ylabel("costs")

        print(data)
