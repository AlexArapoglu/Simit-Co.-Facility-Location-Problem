import math
import random

class Operators:
    def create_distance_matrix(self, row_length, column_length):
        result = [[0 for _ in range(column_length)] for _ in range(row_length)]
        for i in range(row_length):
            for j in range(column_length):
                if j == 0:
                    result[i][j] = (random.random() / 10) + 41.02
                else:
                    result[i][j] = random.random() + 28.2
        return result

    def print_2d(self, array):
        for row in array:
            print(','.join(str(element) for element in row))

    def distance_from(self, lat1, lng1, lat2, lng2):
        earth_radius = 3958.75  # miles (or 6371.0 kilometers)
        d_lat = math.radians(lat2 - lat1)
        d_lng = math.radians(lng2 - lng1)
        sin_d_lat = math.sin(d_lat / 2)
        sin_d_lng = math.sin(d_lng / 2)
        a = math.pow(sin_d_lat, 2) + math.pow(sin_d_lng, 2) * math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = earth_radius * c
        return dist

    def distance_matrix(self, facilities, points):
        dist_mat = []
        for fac in facilities:
            row = [self.distance_from(fac.x, fac.y, point.x, point.y) for point in points]
            dist_mat.append(row)
        return dist_mat

    def find_min_index(self, dist_mat):
        result = [0, 0]
        min_val = dist_mat[0][0]
        for i, row in enumerate(dist_mat):
            for j, val in enumerate(row):
                if val < min_val:
                    min_val = val
                    result = [i, j]
        return result