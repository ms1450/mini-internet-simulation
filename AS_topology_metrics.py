import csv
import re


# Get List of IXPs
def get_ixp_nodes(topology_file):
    connections = []
    # Read the edge data
    with open(topology_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            if row[1] == "IXP":
                numbers = re.findall(r'\d+', row[0])
                connections.append(int(numbers[0]) if numbers else None)
    return connections


# Extract Network Data (Subnet, Next_Hop, and Path) from the filepath
def extract_network_data(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    raw_data = []
    for line in lines:
        if line[0] == 'V':
            values = line[4:].split(' ')
            cleaned = [value.strip() for value in values if value.strip()]
            raw_data.append(cleaned)

    current_network = ""  # To keep track of network
    data = []
    AS_number = ''
    for data_value in raw_data:
        path = []
        if '/' in data_value[0]:
            current_network = data_value[0]
            subnet = data_value[0]
        else:
            subnet = current_network
        if '/' not in data_value[0]:
            next_hop = data_value[0]
        else:
            next_hop = data_value[1]
        if next_hop != '0.0.0.0':
            reversed_value = data_value[::-1]
            start_index = len(data_value) - reversed_value.index('0', reversed_value.index('i') + 1) - 1
            path = data_value[start_index + 1: len(data_value) - 1]
        else:
            AS_number = current_network.split('.', 1)[0]
        data.append([subnet, next_hop, path])
    return AS_number, data


# Parse Links File Metrics
def topology_metrics(links_file):
    connections = []
    # Read the edge data
    with open(links_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            pair = tuple(sorted(((row[2]), (row[3]))))
            numeric_pair = tuple(sorted(
                (int(''.join(i for i in row[2] if i.isdigit())), int(''.join(i for i in row[3] if i.isdigit())))))
            connections.append(numeric_pair)
        return connections


# Form connections from network data
def form_network_connections(AS, network_data):
    connections = []
    for values in network_data:
        if len(values[2]) == 1:
            pair = tuple(sorted((int(AS), int(values[2][0]))))
            if pair not in connections:
                connections.append(pair)
        elif len(values[2]) > 1:
            first_pair = tuple(sorted((int(AS), int(values[2][0]))))
            if first_pair not in connections:
                connections.append(first_pair)
            for i in range(len(values[2]) - 1):
                next_pair = tuple(sorted((int(values[2][i]), int(values[2][i + 1]))))
                if next_pair not in connections:
                    connections.append(next_pair)
    return connections


# Print Topology Metrics
def get_non_ixp_metrics(connections, IXPs):
    count = 0
    for connection in connections:  # connection is a tuple like (1, 2)
        # Check if neither end of the connection is an IXP
        if not any(node in IXPs for node in connection):
            count += 1
    return count


if __name__ == '__main__':
    node_files = 'Topology_Nodes_50.csv'
    link_files = 'Topology_Links_50.csv'
    ipbgp_file = 'Sample BGP.txt'
    print("[+]\tReading topology...")
    ixp_nodes = get_ixp_nodes(node_files)
    links = topology_metrics(link_files)
    print("[+]\t\tTotal Links: ", len(links))
    print("[+]\t\tNon IXP Links: ", get_non_ixp_metrics(links, ixp_nodes))
    print("[+]\tExtracting IP BGP File...")
    AS, network_data = extract_network_data(ipbgp_file)
    print("[+]\t\tAS: ", AS)
    print("[+]\t\tFile Name: ", ipbgp_file)
    print("[+]\t\tFile Network Entries: ", len(network_data))
    print("[+]\tForming Network Connections...")
    ipbgp_connections = form_network_connections(AS, network_data)
    print("[+]\t\tTotal Links: ", len(ipbgp_connections))
    print("[+]\t\tNon IXP Links: ", get_non_ixp_metrics(ipbgp_connections, ixp_nodes))




