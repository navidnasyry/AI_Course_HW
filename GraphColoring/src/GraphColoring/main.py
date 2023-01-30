from simulator import show_graph
import argparse
import random
import math

# global variabls
GRAPH = {}
NUMBERS_OF_COLORS = 1
EVALIUATION_VALUE = 0
ASSIGN_COLORS = []


def calcute_simulated_annealing(eval, temp = 1000.0, cool = 0.7):
    while temp > 0.1:
        p = math.e ** (( -eval *100 ) / temp)
        # decrease the temperature
        temp = temp * cool
        print(p)
        yield p


# parse input
def parse_input():
    parser = argparse.ArgumentParser(
                    prog = 'GraphColoring',
                    description = 'in this program, you can color the graph with graph-coloring algorithm',
                    epilog = 'Enjoy coloring...:)')

    parser.add_argument('-i', '--inputfile',
                     help= 'write path of input file' )
    parser.add_argument('-o', '--outputfile',
                     help= 'write path of output file')           
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        default= False,
                        help= 'if you want to show level by level coloring, set this flag')
    parser.add_argument('-s', '--simulated_annealing',
                    action='store_true',
                    default= False,
                    help= 'if you want to run algorithm with simulated annealing, set this flag')
    args = parser.parse_args()

    return args.inputfile, args.outputfile, args.debug, args.simulated_annealing

# read data from file
def InputData(file_name):
    with open(file_name, 'r') as f:
        point_num, edge_num = f.readline().split()
        point_num = int(point_num)
        edge_num = int(edge_num)
        graph_dict = {}
        for i in range(edge_num):
            line = f.readline().split()
            if int(line[1]) not in graph_dict.keys():
                graph_dict[int(line[1])] = []
            if int(line[2]) not in graph_dict.keys():
                graph_dict[int(line[2])] = []
            graph_dict[int(line[1])].append(int(line[2]))
            graph_dict[int(line[2])].append(int(line[1]))
            
    return graph_dict



# return number of Coloring confilicts
def EvaluationFunctoin(assign_colors):
    global GRAPH
    counter = 0

    for i in GRAPH:
        for j in GRAPH[i]:
            if assign_colors[i-1] == assign_colors[j-1]:
                counter += 1
    return counter/2


# find all neighbors 
def FindAllNeighbors():
    global ASSIGN_COLORS
    all_neighbors = []
    assign_temp = ASSIGN_COLORS
    all_neighbors.append(ASSIGN_COLORS)
    for i in range(len(ASSIGN_COLORS)):
        assign_temp = list(ASSIGN_COLORS)
        for j in range(1, NUMBERS_OF_COLORS + 1):
            assign_temp[i] = j
            if assign_temp not in all_neighbors:
                all_neighbors.append(assign_temp)

    return all_neighbors



def FindBestExchange(simulation_annealing):
    global EVALIUATION_VALUE
    minimum_neighbor = list(ASSIGN_COLORS)
    minimum_evaluation = EVALIUATION_VALUE
    all_neighbors_without_new = FindAllNeighbors()

    ## if simulation annealing mode ON
    ## we select randomlly on of the neighbors that maybe 
    ## not the best neighbor
    if simulation_annealing:
        if random.random() > next(calcute_simulated_annealing(minimum_evaluation)):
            simulation_annealing_neighbor = all_neighbors_without_new[random.randint(0,len(all_neighbors_without_new)-1)]
            simulation_annealing_eval = EvaluationFunctoin(simulation_annealing_neighbor)
            return (simulation_annealing_eval, simulation_annealing_neighbor)
    

    for neighbor in all_neighbors_without_new: 
        new_evaluation = EvaluationFunctoin(neighbor)
        if  new_evaluation < minimum_evaluation:
            minimum_evaluation = new_evaluation
            minimum_neighbor = list(neighbor)

    if minimum_evaluation == EVALIUATION_VALUE:
        global NUMBERS_OF_COLORS
        NUMBERS_OF_COLORS += 1
        all_neighbors_with_new = FindAllNeighbors()

        for neighbor in all_neighbors_with_new: 
            new_evaluation = EvaluationFunctoin(neighbor)
            if  new_evaluation < minimum_evaluation:
                minimum_evaluation = new_evaluation
                minimum_neighbor = list(neighbor)


    return (minimum_evaluation, minimum_neighbor)



def PrintOutputToFile(assign_coloring, output_file):
    number_of_colors = max(assign_coloring)
    with open(output_file, 'w') as f:
        f.write(str(number_of_colors) + "\n")
        for i in range(len(assign_coloring)):
            f.write(str(i+1) + " " + str(assign_coloring[i]) + "\n")



def main():
    global GRAPH
    global ASSIGN_COLORS
    global EVALIUATION_VALUE
    input_file, output_file, debug, simulation_annealing = parse_input()
    GRAPH = InputData(input_file)
    ASSIGN_COLORS = len(GRAPH) * [1]
    EVALIUATION_VALUE = EvaluationFunctoin(ASSIGN_COLORS)

    while(EVALIUATION_VALUE != 0):
        EVALIUATION_VALUE, ASSIGN_COLORS = FindBestExchange(simulation_annealing)
        if debug:
            show_graph(GRAPH, ASSIGN_COLORS)
        if debug:
            print(ASSIGN_COLORS)
            print(EVALIUATION_VALUE)
    
    print(ASSIGN_COLORS)
    PrintOutputToFile(ASSIGN_COLORS, output_file)
    show_graph(GRAPH, ASSIGN_COLORS)

    



if __name__ == "__main__":
    main()

   




