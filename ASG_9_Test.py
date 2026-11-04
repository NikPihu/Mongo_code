print("Developed by: Nikunj Tangle")
print("Submitted to: Vaishali Ingale Mam")


# import
# load
# preprocessing
# train test split
# formula
# elbow method
# train k means
# plot clusters
# k means for full dataset
# dendogram
# agglomerative clusters
# compare


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage,dendrogram
from scipy.spatial.distance import cdist


df= pd.read_csv("Iris.csv")
print(df.head())


species=df["Species"]
X=df.drop(columns=["Id", "Species"])

scalar=StandardScaler()
X_scaled=scalar.fit_transform(X)


X_train,X_test=train_test_split(
    X_scaled,
    test_size=0.2,
    random_state=42
)


def wcss(X, labels):
    total = 0
    for c in set(labels):
        pts = X[labels == c]            # points in cluster c
        centre = pts.mean(axis=0)       # cluster centre
        total += ((pts - centre) ** 2).sum()
    return total


def dunn(X, labels):
    groups = [X[labels == c] for c in set(labels)]

    # smallest distance between two different clusters
    min_gap = min(cdist(groups[i], groups[j]).min()
                  for i in range(len(groups))
                  for j in range(i + 1, len(groups)))

    # largest distance inside one cluster
    max_size = max(cdist(g, g).max() for g in groups)

    return min_gap / max_size


wcss_values=[]
for k in range(1,11):
    km=KMeans(n_clusters=k,random_state=42,n_init=10)
    km.fit(X_train)
    wcss_values.append(km.inertia_)

plt.plot(range(1,11),wcss_values,marker="o",label="WCSS")
plt.legend()
plt.show()


kmeans=KMeans(n_clusters=3,random_state=42,n_init=10)
kmeans.fit(X_train)

train_labels=kmeans.predict(X_train)
test_labels=kmeans.predict(X_test)

plt.scatter(X_train[:,2],X_train[:,3],c=train_labels,label="Train")
plt.scatter(X_test[:,2],X_test[:,3],c=test_labels,marker="x",label="Test")
plt.scatter(kmeans.cluster_centers_[:,2],kmeans.cluster_centers_[:,3],c="red",marker="*",s=300,label="Centres")
plt.legend()
plt.show()


km_full=KMeans(n_clusters=3,random_state=42,n_init=10)
km_labels=km_full.fit_predict(X_scaled)


Z=linkage(X_scaled,method="ward")
plt.figure(figsize=(10,5))

dendrogram(Z,truncate_mode="lastp",p=20)
plt.axhline(y=10,color="red",linestyle="--")
plt.show()


hc=AgglomerativeClustering(n_clusters=3,linkage="ward")
hc_labels=hc.fit_predict(X_scaled)

plt.scatter(X_scaled[:,2],X_scaled[:,3],c=hc_labels)
plt.show()


results = []
for name, labels in [("K-Means", km_labels), ("Hierarchical", hc_labels)]:
    results.append({
        "Model": name,
        "WCSS": wcss(X_scaled, labels),
        "Dunn": dunn(X_scaled, labels),
    })

results_df = pd.DataFrame(results).set_index("Model")
print(results_df.round(4))

ax = results_df.plot(kind="bar", subplots=True, layout=(1, 2), figsize=(10, 4), rot=0, legend=False)
for a in ax.flatten():
    for bars in a.containers:
        a.bar_label(bars, fmt="%.3f")
plt.tight_layout()
plt.show()


results = []
for name, labels in [("K-Means", km_labels), ("Hierarchical", hc_labels)]:
    results.append({
        "Model": name,
        "WCSS": wcss(X_scaled, labels),
        "Dunn": dunn(X_scaled, labels),
    })

results_df = pd.DataFrame(results).set_index("Model")
print(results_df.round(4))

results_df.plot(kind="bar",subplots=True,layout=(1, 2), figsize=(10, 4), rot=0, legend=False)
plt.tight_layout()
plt.show()
