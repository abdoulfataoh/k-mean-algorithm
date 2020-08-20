from model import KMean


data = [
    (2, 3),
    (3, 3),
    (6, 8),
    (8, 8),
    (3, 5),
    (7, 9)
]

model = KMean(n_clusters=2, data=data)
model.train()
model.display_clusters()
model.display_points()
