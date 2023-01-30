import pandas
from pprint import pprint
from copy import deepcopy


def help():
    index_map = {
        0 : "اراک" ,
        1 : "اردبیل" ,
        2 : "ارومیه" ,
        3 : "اصفهان" ,
        4 : "اهواز" ,
        5 : "ایلام" ,
        6 : "بجنورد" ,
        7 : "بندرعباس" ,
        8 : "بوشهر" ,
        9 : "بیرجند" ,
        10 : "تبریز" ,
        11 : "تهران" ,
        12 : "خرماباد" ,
        13 : "رشت" ,
        14 : "زاهدان" ,
        15 : "زنجان" ,
        16 : "ساری" ,
        17 : "سمنان" ,
        18 : "سنندج" ,
        19 : "شهرکرد" ,
        20 : "شیراز" ,
        21 : "قزوین" ,
        22 : "قم" ,
        23 : "کرج" ,
        24 : "کرمان" ,
        25 : "کرمانشاه" ,
        26 : "گرگان" ,
        27 : "مشهد" ,
        28 : "همدان" ,
        29 : "یاسوج" ,
        30 : "یزد" ,
    }
    pprint(index_map)

def readExcel(file_name):
    excel_data_df = pandas.read_excel(file_name)

    file_data = excel_data_df.to_dict(orient='records');
    excel_list = []
    for i in range(4, 35):
        excel_list.append(list(file_data[i].values())[2:])

    return excel_list

def get_input():
    s, d = input().split()
    return int(s), int(d)

def decode_index(index_list):
    index_map = {
        0 : "اراک" ,
        1 : "اردبیل" ,
        2 : "ارومیه" ,
        3 : "اصفهان" ,
        4 : "اهواز" ,
        5 : "ایلام" ,
        6 : "بجنورد" ,
        7 : "بندرعباس" ,
        8 : "بوشهر" ,
        9 : "بیرجند" ,
        10 : "تبریز" ,
        11 : "تهران" ,
        12 : "خرماباد" ,
        13 : "رشت" ,
        14 : "زاهدان" ,
        15 : "زنجان" ,
        16 : "ساری" ,
        17 : "سمنان" ,
        18 : "سنندج" ,
        19 : "شهرکرد" ,
        20 : "شیراز" ,
        21 : "قزوین" ,
        22 : "قم" ,
        23 : "کرج" ,
        24 : "کرمان" ,
        25 : "کرمانشاه" ,
        26 : "گرگان" ,
        27 : "مشهد" ,
        28 : "همدان" ,
        29 : "یاسوج" ,
        30 : "یزد" ,
    }

    city_list = []
    for i in index_list:
        city_list.append(index_map[i])
    return city_list




class AStar:
    def __init__(self, neighbor_matrix, line_distance_matrix, real_distance_matrix, start_index, destination_index):
        self.neighbor_matrix = neighbor_matrix
        self.line_distance_matrix = line_distance_matrix
        self.real_distance_matrix = real_distance_matrix
        self.reached_indexes = []
        self.g = 0
        self.destination_index = destination_index
        self.start_index = start_index

    def cal_f(self, current_index, next_index):
        h = self.line_distance_matrix[next_index][self.destination_index] # calcute h parameter of next point
        g = self.g + self.real_distance_matrix[current_index][next_index] # calcute g parameter of next point
        f = g + h
        return f, g

    def cal_next_neighbors(self, current_index):
        neighbors_indexes = []
        for i in range(len(self.neighbor_matrix[current_index])):
            if self.neighbor_matrix[current_index][i] == 1 and i not in self.reached_indexes:
                neighbors_indexes.append(i)
        return neighbors_indexes


    def find_best_neighbor(self, current_index):
        all_neighbors = self.cal_next_neighbors(current_index)
        min_f = float('inf')
        for ind in all_neighbors:
            new_f, new_g = self.cal_f(current_index, ind)
            if min_f > new_f:
                min_f = new_f
                best_ind = ind
                final_g = new_g

        self.g = final_g
        return best_ind, min_f

    def solve(self):
        current_index = self.start_index
        self.reached_indexes.append(current_index)
        best_f = 0
        while(current_index != self.destination_index):
            best_ind, best_f = self.find_best_neighbor(current_index)
            self.reached_indexes.append(best_ind)
            current_index = best_ind
        minimum_distance = best_f # actully in final loop, best_f is same as minimum_distance
        return minimum_distance


class BFS:
    def __init__(self, neighbor_matrix, real_distance_matrix, start_index, destination_index):
        self.neighbor_matrix = neighbor_matrix
        self.real_distance_matrix = real_distance_matrix
        self.all_routes = []
        self.reached_indexes = []
        self.destination_index = destination_index
        self.start_index = start_index


    def cal_next_neighbors(self, current_index):
        neighbors_indexes = []
        for i in range(len(self.neighbor_matrix[current_index])):
            if self.neighbor_matrix[current_index][i] == 1 and i not in self.reached_indexes:
                neighbors_indexes.append(i)
        return neighbors_indexes

    def cal_all_distance(self, index_list):
        if len(index_list) <= 1:
            return 0
        all_distance = 0
        for i in range(len(index_list)-1):
            all_distance += self.real_distance_matrix[index_list[i]][index_list[i+1]]
        return all_distance

    def solve(self):
        current_index = self.start_index
        self.all_routes.append([current_index])
        if current_index == self.destination_index:
            return [current_index]
        while True:
            height_nodes = deepcopy(self.all_routes)
            for route in height_nodes:
                curr = route[-1]
                self.reached_indexes.append(curr)
                frontier = self.cal_next_neighbors(curr)
                #add all new routes to all_routes
                if len(frontier) != 0: 
                    base_route = deepcopy(route)
                    self.all_routes.remove(route)
                    for n in frontier:
                        new_route = deepcopy(base_route)
                        new_route.append(n)
                        self.all_routes.append(new_route)
                        if n == self.destination_index:
                            self.goal_list = new_route
                            return new_route
              

            

 




def main():
    
    help()
    print("\nEnter source_id and distance_id with this format:")
    print("source_id distance_id\n")
    source_id, distance_id = get_input()


    line_distance_matrix = readExcel("ProvinceCentersStraightLineDistances.xlsx")
    real_distance_matrix = readExcel("ProvinceCenterDistances.xlsx")
    neighbor_matrix = readExcel("ProvinceCentersNeighbours.xlsx")





    # Solve with A*
    print("\nSolve with A* :")
    a_star = AStar(neighbor_matrix, 
                    line_distance_matrix,
                    real_distance_matrix,
                    source_id,
                    distance_id
                    )
    min_distance = a_star.solve()
    print(a_star.reached_indexes)
    print(decode_index(a_star.reached_indexes))
    print(min_distance)
    
    print("\n\n")

    # Solve with Bearst First Search
    print("Solve with BFS : ")
    bfs = BFS(neighbor_matrix, 
                    real_distance_matrix,
                    source_id,
                    distance_id
                    )
    bfs_route = bfs.solve()
    print(bfs_route)
    print(decode_index(bfs_route))
    print(bfs.cal_all_distance(bfs_route))

    












if __name__ == "__main__":
    main()