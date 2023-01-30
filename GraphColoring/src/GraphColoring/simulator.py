import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def create_df_connections(node_connections_dict, assign_colors):
    labels_list = [str(i+1) for i in range(len(node_connections_dict))]
    from_nodes= []
    to_nodes = []
    for node_inex in node_connections_dict.keys():
        for dist in node_connections_dict[node_inex]:
            from_nodes.append(str(node_inex))
            to_nodes.append(str(dist))
    df = pd.DataFrame({ 'from':from_nodes, 'to':to_nodes})
    carac = pd.DataFrame({ 'node':labels_list, 'groups':[str(i) for i in assign_colors]})
    return df, carac



def show_graph(input_dict, assign_color_list):
    df, carac = create_df_connections(input_dict, assign_color_list)
    # creating our graph :)
    
    G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())
    # add new label groups for each node color
    carac= carac.set_index('node')
    carac=carac.reindex(G.nodes())
    carac['groups']=pd.Categorical(carac['groups'])
    # Create and draw the graph:
    nx.draw(G, with_labels=True, node_color=carac['groups'].cat.codes, cmap=plt.cm.Set1, node_size=500)
    plt.show()

