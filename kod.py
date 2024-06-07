import random
import time
import matplotlib.pyplot as plt
from Facility import Facility
from Point import Point
from Operators import Operators

def k_center_algorithm(candidate_facility_number, point_amount, open_p_num_of_facs):
    operator = Operators()

    facs_coordinates = operator.create_distance_matrix(candidate_facility_number, 2)
    points_coordinates = operator.create_distance_matrix(point_amount, 2)
    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points = [Point(i, points_coordinates[i][0], points_coordinates[i][1], 2 * random.random() + 1) for i in range(point_amount)]
    distance_matrix = operator.distance_matrix(facs, points)
    
    # Store opened facilities and other lists, you need to use these arrays.
    opened_facilities = []
    unopened_facilities = facs.copy()
    unassigned_points = []


    # Number of facilities to open
    total_distance = 0
    min_value = float('inf')
    index_of = 0
    previous_min = -1
    max_val = 0

    # Find a huge value to set min_value for comparison
    for y in range(len(facs)):
        total_distance = sum(distance_matrix[y])
        if max_val < total_distance:
            max_val = total_distance
    min_value = max_val + 1

    #Start coding here

    min_max_dist = float('inf')
    best_facility_index = None

    for i in range(candidate_facility_number):
        max_dist = max(distance_matrix[i])
        if max_dist < min_max_dist:
            min_max_dist = max_dist
            best_facility_index = i

    opened_facilities.append(unopened_facilities.pop(best_facility_index))


    while len(opened_facilities) < open_p_num_of_facs:
        min_max_dist = float('inf')
        best_facility_index = None
        for fac in unopened_facilities:
            max_dist = 0
            for point in points:
                max_dist = max([operator.distance_from(fac.x, fac.y, opened_fac.x, opened_fac.y) for opened_fac in opened_facilities])
            if max_dist < min_max_dist:
                min_max_dist = max_dist
                best_facility_index = unopened_facilities.index(fac)

        opened_facilities.append(unopened_facilities.pop(best_facility_index))

    
    for point in points:
        min_dist = float('inf')
        best_facility_id = None
        for fac in opened_facilities:
            dist = operator.distance_from(fac.x, fac.y, point.x, point.y)
            if dist < min_dist:
                min_dist = dist
                best_facility_id = fac.id
        point.assigned_facility_id = best_facility_id

    return opened_facilities, unopened_facilities, points

def local_search_2opt(candidate_facility_number, point_amount, open_p_num_of_facs):
    operator = Operators()

    opened_facilities, unopened_facilities, points = k_center_algorithm(candidate_facility_number, point_amount, open_p_num_of_facs)


    total_distance = sum(operator.distance_from(fac.x, fac.y, point.x, point.y) for fac in opened_facilities[:open_p_num_of_facs] for point in points)


    improvement = True
    count = 0
    while improvement and count < 1000:
        improvement = False
        for i in range(len(opened_facilities)):
            for j in range(i+1, len(opened_facilities)):
                new_opened_facilities = opened_facilities[:]
                new_opened_facilities[i], new_opened_facilities[j] = new_opened_facilities[j], new_opened_facilities[i]
                
                new_distance = 0
                for point in points:
                    min_dist = min(operator.distance_from(fac.x, fac.y, point.x, point.y) for fac in new_opened_facilities[:open_p_num_of_facs])
                    new_distance += min_dist
                
        
                if new_distance < total_distance:
                    total_distance = new_distance
                    opened_facilities = new_opened_facilities
                    improvement = True
                    break
            if improvement:
                break
        count = count + 1 

  
    for point in points:
        min_dist = float('inf')
        best_facility_id = None
        for fac in opened_facilities[:open_p_num_of_facs]:
            dist = operator.distance_from(fac.x, fac.y, point.x, point.y)
            if dist < min_dist:
                min_dist = dist
                best_facility_id = fac.id
        point.assigned_facility_id = best_facility_id

    return opened_facilities, unopened_facilities, points


def performance_test(problem_sizes):
    for i, size in enumerate(problem_sizes):
        point_amount, candidate_facility_number, k = size
        start_time = time.time()
        opened_facilities, unopened_facilities, points = k_center_algorithm(candidate_facility_number, point_amount, k)
        end_time = time.time()
        print(f"GREEDY ALGORITHM: Size: {size}, Execution Time: {end_time - start_time:.4f} seconds")


        plot_facilities_and_points(opened_facilities, unopened_facilities, points, f"greedy_{size}.png")

def performance_test_improvement(problem_sizes):
    for i, size in enumerate(problem_sizes):
        point_amount, candidate_facility_number, k = size
        start_time = time.time()
        opened_facilities, unopened_facilities, points = local_search_2opt(candidate_facility_number, point_amount, k)
        end_time = time.time()
        print(f"IMPROVEMENT ALGORITHM: Size: {size}, Execution Time: {end_time - start_time:.4f} seconds")

        plot_facilities_and_points(opened_facilities, unopened_facilities, points, f"improvement_{size}.png")

def measure_improvement(problem_sizes):
    operator = Operators()
    
    for size in problem_sizes:
        point_amount, candidate_facility_number, k = size
        
      
        opened_facilities_greedy, _, points = k_center_algorithm(candidate_facility_number, point_amount, k)
        total_distance_greedy = sum(operator.distance_from(fac.x, fac.y, point.x, point.y) for fac in opened_facilities_greedy[:k] for point in points)
        
        
        opened_facilities_2opt, _, points = local_search_2opt(candidate_facility_number, point_amount, k)
        total_distance_2opt = sum(operator.distance_from(fac.x, fac.y, point.x, point.y) for fac in opened_facilities_2opt[:k] for point in points)
        
       
        improvement_percentage = ((total_distance_greedy - total_distance_2opt) / total_distance_greedy) * 100
        print(f"Improvement for problem size {size}: {improvement_percentage:.2f}%")


def plot_facilities_and_points(opened_facilities, unopened_facilities, points, filename):
    colors = {}
    color_list = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'pink', 'yellow', 'brown', 'linen']
    for i, fac in enumerate(opened_facilities):
        colors[fac.id] = color_list[i % len(color_list)]

    for fac in unopened_facilities:
        plt.scatter(fac.x, fac.y, c='black', marker='^')

    for fac in opened_facilities:
        plt.scatter(fac.x, fac.y, c=colors[fac.id], marker='^')

    for point in points:
        if point.assigned_facility_id is not None:
            plt.scatter(point.x, point.y, c=colors[point.assigned_facility_id], marker='o')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Facilities and Assigned Points')

    plt.savefig(filename)
    plt.close()

if __name__ == "__main__":
    problem_sizes = [
        (50, 10, 3), (20, 5, 3), (40, 10, 4), (60, 15, 5), (80, 20, 6),
        (100, 25, 7), (150, 30, 8), (200, 35, 9), (250, 40, 10)
    ]

    performance_test(problem_sizes)
    performance_test_improvement(problem_sizes)
    measure_improvement(problem_sizes)
