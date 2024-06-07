# Simit Co. Facility Location Problem 
### Alexander Arapoğlu 
#
SimitCo, a pastry company, aims to open a certain amount of bakery facilities around Istanbul. Company engineer has found several candidate locations for the facilities and pointed out customers, however, they hesitated to give this long-term decision by themselves. At this point, they have reached you to create a good-performing heuristic. After analyzing the situation, you’ve concluded that this is a Facility Location Problem. SimitCo has signed long-term contracts with each customer, so customer data is considered as deterministic.

This project aims to solve the Facility Location Problem for Simit Co. using a combination of a k-Center Greedy Algorithm and a 2-opt Local Search improvement heuristic. Code in `kod.py` file calculates execution times and plots a graph of facility locations for both k-center Greedy Algorithm and Improvement Heuristics which are saved in the `Plots` folder of this Repository. Also, it calculates the improvement percentage achieved by improvement heuristics for each problem size.

## Changes and Additions

Every change was made in `kod.py` file other files were left the same way.

**1. `main()` Function Changed:** 

As we wanted to run our k-Center Algorithm for every problem size we needed to add input parameters for main function. Secondly, for our convenience while coding to not mix our main algorithm and improvement algorithm we decided to change `main()` functions name to `k_center_algorithm()`. We used `candidate_facility_number`, `point_amount`, and `open_p_num_of_facs` paremeters for defining `k_center_algorithm()` function.

**2. `plot_facilities_and_points()` Function Changed:**

Initially `plt.show()` was used in the function to view plots created by the algorithm. However, it shows the plot for each problem size separately and interrupts the running process of the code. Instead, we decided to use `plt.savefig(filename)` and `plot.close()` code lines while adding `filename` variable into the parameters of `plot_facilities_and_points()` function. This usage enables us to save all plots with file names indicating the current problem size and algorithm used with the help of f-String notation while not interrupting the running process of the code. 

**3. `performance_test()` and `performance_test_improvement()` Functions Created:**

`performance_test()` and `performance_test_improvement()` functions were created for execution time calculation and plotting the graphs for each problem size. These two functions are essentially same they just call different algorithm functions. `performance_test()` calls `k_center_algorithm()` function and `performance_test_improvement()` calls `local_search_2opt()` function. The main logic is initiating a for loop to iterate for every problem size while measuring execution time with `time` library which is imported. While calling `k_center_algorithm()` or `local_search_2opt()` for execution time measurements functions also take returned values of algorithm functions and use these values to plot graphs for each problem size.

**3. `measure_,improvement()` Function Created:**

To measure the improvement percentage of improvement algorşthm we created `measure_improvement()` function. This function calculates the total distance of both k-Center Algorithm and 2opt Local Search Algorithm and subtracts them to find the percentage of improvement. 

## How Does `k_center_algorithm()` Function Works?

**Initialization of the Algorithm**

- Random coordinates for candidate facilities and points are generated using the `create_distance_matrix` function from the `Operators` class.

- Facility and Point objects are created based on the generated coordinates using the `Facility` and `Point` classes.


- The distance matrix representing the distances between facilities and points is calculated using the `distance_matrix` method from the `Operators` class.

**Step 1: Locating the First Facility**

- The algorithm starts by initializing variables to track the minimum maximum distance and the index of the best facility.

- It then iterates over all candidate facilities to find the facility with the minimum maximum distance to any already opened facility

- Within each iteration, the code calculates the maximum distance from the current candidate facility to all points. If this maximum distance is less than the current minimum maximum distance, the index of the current facility is updated as the best facility index.

- Once the best facility is identified, it is appended to the list of opened facilities, and removed from the list of unopened facilities

**Step 2: Locating Remaining Facilities**

- Then we use a while loop which continues until the desired number of **k** facilities is reached.

- Within each iteration, the code calculates the maximum distance from the current unopened facility to any already opened facility. This is done using a list comprehension and the max function.

- The unopened facility with the minimum maximum distance is identified and selected for inclusion among the opened facilities.

**Step 3: Assigning Points to the Nearest Open Facility**

- After selecting the facilities, points are assigned to the nearest opened facility based on the calculated distances. This is accomplished through another for loop. Within this loop for each point, the loop iterates through all opened facilities to determine the nearest one based on the calculated distances.

- The point is then assigned to the nearest opened facility by updating its `assigned_facility_id` attribute.

- After finalizing the algorithm `openned_facilities`, `unopenned_facilities` and `points` variables are returned to be used in plotting the graphs.


## How Does `local_search_2opt()` Function Works?:

- The `local_search_2opt()` function further improves the solution obtained from the greedy algorithm using the 2-opt method alike heuristic which we called 2opt Local Search.

- It starts by obtaining an initial solution using the `k_center_algorithm()` function and calculates the total distance of the initial solution.

- The loop continues until no further improvement is possible or a maximum number of iterations of 1000 is reached.

- For each pair of opened facilities, the loop swaps their positions and calculates the total distance of the new solution.

- If the total distance of the new solution is lower than the previous best distance, the swap is accepted, and the solution is updated. Otherwise, the swap is reverted.

- The loop terminates when no further improvement is possible or the maximum number of iterations is reached.

- After finalizing the algorithm `openned_facilities`, `unopenned_facilities` and `points` variables are returned to be used in plotting the graphs.



## Questions 

**1.Which type of Facility Location problem is this? Why?**

There are two reasons why this problem is a **p-center problem**:

1. Simit Co. has long term contracts with each of their customers,  which implies a commitment to serve all customers efficiently. This means that we need to **minimize the max distance of each customer**.

2. Second reason lies in the nature of the product which Simit Co. produces. As Simit Co. is a pastry company the products they produce are things such as bread, bun, bagel, börek or simit which can get cold fast and needed to be consumed and delivered fast and hot. Hence, we need to **minimize the max distance of each customer**.


**2.How does the execution time change when problem size is increased? Report it by running the same algorithm for given problem sizes (customer amount-candidate facility amount-k amount):**

***20-5-3 / 40-10-4 / 60-15-5 / 80-20-6 / 100-25-7 / 150-30-8 / 200-35-9 / 250-40-10***

1. **Execution Time Analysis of K-Center Algorithm**
- Execution time increases as problem size (customer amount, candidate facility amount, k amount) increases. We observed the following execution times:
     - (50, 10, 3)  : 0.0020 seconds
     - (20, 5, 3)   : 0.0005 seconds
     - (40, 10, 4)  : 0.0025 seconds
     - (60, 15, 5)  : 0.0136 seconds
     - (80, 20, 6)  : 0.0251 seconds
     - (100, 25, 7) : 0.0587 seconds
     - (150, 30, 8) : 0.1492 seconds
     - (200, 35, 9) : 0.2851 seconds
     - (250, 40, 10): 0.4805 seconds

2. **Execution Time Analysis of 2-opt Local Search Improvement Agorithm**
- Execution time increases as problem size (customer amount, candidate facility amount, k amount) increases. We observed the following execution times:
     - (50, 10, 3)  : 0.0040 seconds
     - (20, 5, 3)   : 0.0010 seconds
     - (40, 10, 4)  : 0.0040 seconds
     - (60, 15, 5)  : 0.0150 seconds
     - (80, 20, 6)  : 0.0363 seconds
     - (100, 25, 7) : 0.0778 seconds
     - (150, 30, 8) : 0.1866 seconds
     - (200, 35, 9) : 0.3818 seconds
     - (250, 40, 10): 0.6481 seconds
   

**3.How much improvement does your algorithm make compared to the initial algorithm?**
- The improvement algorithm, which we choose as 2-opt Local Search, shows varying levels of improvement compared to the initial greedy algorithm. We see negative improvement in some problem sizes. This can be due to initial solution being close or equal to optimal. As a conclusion we can say that we see relatively great improvement rates in general. The improvement percentages are as follows:
     - For problem size (50, 10, 3)  : 23.69%
     - For problem size (20, 5, 3)   : -34.13%
     - For problem size (40, 10, 4)  : 6.39%
     - For problem size (60, 15, 5)  : -4.70%
     - For problem size (80, 20, 6)  : -0.08%
     - For problem size (100, 25, 7) : 4.67%
     - For problem size (150, 30, 8) : -7.97%
     - For problem size (200, 35, 9) : 3.55%
     - For problem size (250, 40, 10): 2.37%
