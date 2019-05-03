# -*- coding: utf-8 -*-
"""part3_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r7wx-xko_NHZWhLT0LrX8cGMJdG0DC33

**Exporting libraries**
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pickle
import pandas as pd
import pickle
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import Counter, defaultdict
from operator import itemgetter

drop_list = []

"""**Loading Necessary Functions**"""

def pickleLoad(filename):
    with open(filename, "rb") as f:
        filetype = pickle.load(f)
    return filetype

def pickleUnload(filename,filetype):
    with open(filename, "wb") as f:
        pickle.dump(filetype, f)

def one_hot(df, cols):
    for each in cols:
        try:
            one_hot = pd.get_dummies(df[each], prefix=each,drop_first=True)
            df = df.join(one_hot)
        except:
            continue
    df.drop(cols, axis=1,inplace=True)
    return df

def k_mean_distance(data, cx, cy, i_centroid, cluster_labels):
    distances = [np.sqrt((x-cx)**2+(y-cy)**2) for (x, y) in data[cluster_labels == i_centroid]]
    return np.mean(distances)

"""**Reading the data file**"""

df = pd.read_csv('population.csv')
df

"""**Replacing the missing values**"""

df.replace(" ?", np.nan, inplace=True)
df

"""**Displaying columns and % of null values in them**"""

print (df.isnull().mean())

"""**Deleting columns with more than 40% of null values**"""

df = df[df.columns[df.isnull().mean() < 0.4]]
df

"""**Visualising Histograms from columns**"""

i = 0
for title in list(df):
    plt.subplots_adjust(left=0.07, bottom=0.23, right=0.95, top=0.95, wspace=None, hspace=None)
    df[title].value_counts().plot(figsize=(20,10),kind='bar')
    plot_title = str(title)
    plt.title(plot_title)
#     plt.savefig("p3_data/graphs/50k/"+str(i)+"_"+plot_title)
    i+=1

"""**Removing Features with 75% same values**"""

data_size = int(df['GRINST'].size*0.75)
for title in list(df):
    try:
        if (df[title].value_counts()[0] > data_size):
            drop_list.append(title)
    except:
        continue
df.drop(drop_list, axis=1,inplace=True)

"""**Converting Numerical features to 8 bin**"""

for y in df.columns:
    if df[y].dtype == np.int64:
        df[y] = pd.cut(df[y],8)

"""**Converting all the features type to categorical**"""

for title in list(df):
    df[title] = df[title].astype('category',copy=False)

"""**Shape and Type of Categories**"""

print (df.shape)
print (df.dtypes)

"""**Replace Missing Values with column's mode**"""

for column in df.columns:
    df[column].replace(np.nan,df[column].mode()[0], inplace=True)

"""**One hot encoding**"""

df = one_hot(df, list(df))
column_name = list(df)

"""**Graph Plot Cumulative Variance vs Number of Components**"""

pca = PCA().fit(df)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.show()

"""**Fitting PCA with n=75**"""

pca = PCA(n_components=75)
pca.fit(df)
df_n = pca.transform(df)

"""**Amount of variance each PC has**"""

print((pca.explained_variance_ratio_))

"""**Mapping weights to 1st,2nd,3rd principal component**"""

for i in range(3):
    print ("**** Principal Component - {} ****".format(i+1))
    A = abs(pca.components_[i])
    ranks = np.argsort(A)
    for a in ranks:
        print ("{} - {}".format(column_name[a],A[a]))
    print ("\n\n")

"""**K mean clustering distance**"""

Sum_of_squared_distances = []
K = range(10,24)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(df_n)
    Sum_of_squared_distances.append(km.inertia_)
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

"""**K mean clustering with n = 22**"""

#K mean clustering with n = 22
clusters = 22
kmeans = KMeans(n_clusters=clusters).fit(df_n)
plt.figure('K-means with {} clusters'.format(clusters))
plt.scatter(df_n[:, 0], df_n[:, 1],c=kmeans.labels_)
plt.show()

"""**Calculates % of data points in each cluster**"""

count = 0
proportions = []
cluster_count = Counter(kmeans.labels_)
for a in cluster_count.items():
    count += a[1]
for a in cluster_count.items():
    proportions.append([a[0],round((float(a[1])/float(count))*100.0,2)])
print (sorted(proportions, key=itemgetter(0)))

"""**Comparison with Clusters formed in population.csv vs more_than_50k**


1. [0, 6.0] - [0, 4.16] ***(Similar)***
2. [1, 3.34] - [1, 7.32] ***(Over represented in more_than_50k)***
3. [2, 8.27] - [2, 4.16] ***(Over represented in general pop.)***
4. [3, 11.2] - [3, 7.32] ***(Similar)***
5. [4, 4.89] - [4, 6.03] ***(Similar)***
6. [5, 3.84] - [5, 2.63] ***(Similar)***
7. [6, 1.72] - [6, 3.3] ***(Similar)***
8. [7, 4.83] - [7, 3.66] ***(Similar)***
9. [8, 3.89] - [8, 4.8] ***(Similar)***
10. [9, 4.89] - [9, 4.22]  ***(Similar)***
11. [10, 1.6] - [10, 2.4] ***(Similar)***
12. [11, 2.68] - [11, 4.41] ***(Similar)***
13. [12, 2.92] - [12, 6.7] ***(Over represented in more_than_50k)***
14. [13, 3.71] - [13, 4.94] ***(Similar)***
15. [14, 12.56] - [14, 2.79] ***(Over represented in general pop.)***
16. [15, 3.31] - [15, 4.3] ***(Similar)***
17. [16, 2.78] - [16, 3.44] ***(Similar)***
18. [17, 4.54] - [17, 5.5] ***(Similar)***
19. [18, 3.34] - [18, 9.22] ***(Over represented in more_than_50k)***
20. [19, 2.25] - [19, 2.12] ***(Similar)***
21. [20, 2.53] - [20, 3.69] ***(Similar)***
22. [21, 4.9]] - [21, 2.88] ***(Similar)***
"""