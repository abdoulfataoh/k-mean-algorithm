# coding: utf-8

import math
import random
import copy

from rich.console import Console
from rich.table import Table


class KMean:
    _n_clusters: int
    _clusters: list[dict]
    _points: list[list]
    _sample_size: int
    _data: list[tuple]

    def __init__(self, n_clusters: int, data: list[tuple]) -> None:
        self._n_clusters = n_clusters
        self._data = data.copy()
        self._sample_size = len(self._data[0])
        self._points = [{'coordinates': point} for point in self._data]
        self.initialize_clusters()
            
    @staticmethod
    def euclidean_distance(point_1: list, point_2: list) -> float:
        if len(point_1) != len(point_2):
            raise ValueError('Point 1 and Point 2 must have the same dimensions')
        size = len(point_1) or len(point_2)
        sum_squares : float = 0.0
        for i in range(size):
            sum_squares += (point_1[i] - point_2[i]) ** 2
        return math.sqrt(sum_squares)

    def initialize_clusters(self) -> None:
        self._clusters = []
        for i in range(self._n_clusters):
            cluster_coordinates: list = []
            for j in range(self._sample_size):
                cluster_coordinates.append(random.random())
            cluster = {
                'coordinates': cluster_coordinates,
                'name': f'cluster_{i}',
            }
            self._clusters.append(cluster)
            
    def assign_points_to_clusters(self) -> None:
        for point in self._points:
            min_distance: float = float('inf')
            for cluster in self._clusters:
                point_coordinates = point['coordinates']
                cluster_coordinates = cluster['coordinates']
                cluster_point_euclidean_distance = self.euclidean_distance(cluster_coordinates, point_coordinates)
                if cluster_point_euclidean_distance < min_distance:
                    point['cluster'] = cluster['name']
                    min_distance = cluster_point_euclidean_distance
    
    def update_cluster(self) -> None:
        for cluster in self._clusters:
            cluster_name = cluster['name']
            for i in range(self._sample_size):
                i_values = []
                for point in self._points:
                    if cluster_name == point['cluster']:
                        point_coordinates = point['coordinates']
                        i_values.append(point_coordinates[i])
                try:
                    cluster['coordinates'][i] = sum(i_values) / len(i_values)
                except ZeroDivisionError:
                    pass

    def train(self) -> None:
        epoch = 0
        while True:
            epoch += 1
            clusters_copy = copy.deepcopy(self._clusters)
            self.assign_points_to_clusters()
            self.update_cluster()
            if clusters_copy == self._clusters:
                print(f'break after {epoch=}')
                break
    
    def display_clusters(self) -> None:
        clusters_table = Table(title='Clusters Table')

        clusters_table.add_column(f'clusters', justify="right", style="cyan", no_wrap=True)
        for i in range(self._sample_size):
            clusters_table.add_column(f'x_{i}', justify="right", style="cyan", no_wrap=True)
        
        for cluster in self._clusters:
            coordinates = cluster['coordinates']
            coordinates = [str(round(point, 3)) for point in coordinates]
            clusters_table.add_row(cluster['name'], *coordinates)
        
        console = Console()
        console.print(clusters_table)


    def display_points(self) -> None:
        for cluster in self._clusters:
            cluster_name = cluster['name']
            points_table = Table(title=f'{cluster_name}')

            for i in range(self._sample_size):
                points_table.add_column(f'x_{i}', justify="right", style="cyan", no_wrap=True)
            
            for point in self._points:
                if point['cluster'] == cluster_name:
                    coordinates = point['coordinates']
                    coordinates = [str(round(point, 3)) for point in coordinates]
                    points_table.add_row(*coordinates)
            
            console = Console()
            console.print(points_table)
