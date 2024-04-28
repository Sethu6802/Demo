import numpy as np

import streamlit as st


def pagerank(nodes, edges, damping_factor=0.85, max_iterations=100, tolerance=1e-6):

    num_nodes = len(nodes)

    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    incoming_count = np.zeros(num_nodes)


    for node, incoming_nodes in edges.items():

        node_index = nodes.index(node)

        for incoming_node in incoming_nodes:

            incoming_index = nodes.index(incoming_node)

            adjacency_matrix[node_index, incoming_index] = 1

            incoming_count[incoming_index] += 1


    for j in range(num_nodes):

        if incoming_count[j] != 0:

            adjacency_matrix[:, j] /= incoming_count[j]

    pagerank_scores = np.ones(num_nodes) / num_nodes

    for _ in range(max_iterations):

        new_pagerank_scores = (1 - damping_factor) / num_nodes + damping_factor * np.dot(adjacency_matrix, pagerank_scores)

        if np.linalg.norm(new_pagerank_scores - pagerank_scores, 1) < tolerance:

            break

        pagerank_scores = new_pagerank_scores

    return pagerank_scores


st.title("PageRank Calculator")

select = st.selectbox(label = "Select Type of Pagerank", options = ["Default", "Modified"])

num_nodes = st.number_input("Enter number of nodes:", min_value=1, step=1)

nodes = st.text_input("Enter Name of nodes (separated by space):")

nodes = nodes.split() if nodes else []

if len(nodes) != num_nodes:

    st.warning("Please provide correct number of node names.")


edges = {}

for node in nodes:

    edges[node] = st.text_input(f"Enter incoming nodes to node {node} (separated by space):")

    edges[node] = edges[node].split() if edges[node] else []


def pagerankM(nodes, edges, damping_factor=0.85, relevance_factor=0.1, max_iterations=100, tolerance=1e-6):

    num_nodes = len(nodes)

    adjacency_matrix = np.zeros((num_nodes, num_nodes))

    incoming_count = np.zeros(num_nodes)

    for node, incoming_nodes in edges.items():
        
        node_index = nodes.index(node)

        for incoming_node in incoming_nodes:

            incoming_index = nodes.index(incoming_node)

            adjacency_matrix[node_index, incoming_index] = 1

            incoming_count[incoming_index] += 1


    for j in range(num_nodes):

        if incoming_count[j] != 0:
            
            adjacency_matrix[:, j] /= incoming_count[j]


    pagerank_scores = np.ones(num_nodes) / num_nodes

    for _ in range(max_iterations):

        new_pagerank_scores = (1 - damping_factor) / num_nodes + damping_factor * np.dot(adjacency_matrix, pagerank_scores)
        
        new_pagerank_scores += relevance_factor * np.ones(num_nodes) / num_nodes
        
        if np.linalg.norm(new_pagerank_scores - pagerank_scores, 1) < tolerance:

            break

        pagerank_scores = new_pagerank_scores

    return pagerank_scores



if st.button("Calculate PageRank"):

    st.write("PageRank Scores")

    if select == 'Modified':

        scores = pagerankM(nodes, edges)

        sorted_indices = np.argsort(scores)[::-1]
        
        for i in sorted_indices:

            st.write(f"{nodes[i]}: {(scores[i]*100):.2f}")



    elif select == 'Default':

        scores = pagerank(nodes, edges)
    
        sorted_indices = np.argsort(scores)[::-1]
        
        for i in sorted_indices:

            st.write(f"{nodes[i]}: {(scores[i]*100):.2f}")
