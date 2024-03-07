import os.path
import pickle

from AS_topology_generator import AutonomousSystem, InternetExchangePoint


def print_AS_config(list_of_ASes, list_of_IXPs):
    with open('AS_config.txt', 'w', newline='\n') as file:
        for entry in list_of_ASes:
            if entry.as_id == 1:
                string = str(entry.as_id) + "\tAS\tConfig\tl3_routers_krill.txt\tl3_links.txt\tempty.txt\tempty.txt\tempty.txt\n"
            else:
                string = str(entry.as_id) + "\tAS\tConfig\tl3_routers.txt\tl3_links.txt\tempty.txt\tempty.txt\tempty.txt\n"
            file.write(string)
        for entry in list_of_IXPs:
            string = str(80 + entry.ixp_id) + "\tIXP\tConfig\tN/A\tN/A\tN/A\tN/A\tN/A\n"
            file.write(string)


def get_ixp_connections(AS, IXP):
    connections = []
    for link in IXP.ixp_connections:
        if link != AS:
            connections.append(str(link.as_id))
    return ",".join(connections)


def print_aslevel_links(list_of_ASes):
    with open('aslevel_links.txt', 'w', newline='\n') as file:
        completed = []
        for entry in list_of_ASes:
            completed.append(entry)
            for customer in entry.customers:
                if customer not in completed:
                    string = str(entry.as_id) + "\tPROV\tProvider\t" + str(
                        customer.as_id) + "\tCUST\tCustomer\t100000\t2.5ms\t179." + str(entry.as_id) + "." + str(
                        customer.as_id) + ".0/24\n"
                    file.write(string)
            for peer in entry.peers:
                if peer not in completed:
                    string = str(entry.as_id) + "\tPEER\tPeer\t" + str(
                        peer.as_id) + "\tPEER\tPeer\t100000\t2.5ms\t179." + str(entry.as_id) + "." + str(
                        peer.as_id) + ".0/24\n"
                    file.write(string)
            for ixp in entry.ixps:
                string = str(entry.as_id) + "\tPEER\tPeer\t" + str(
                    80 + ixp.ixp_id) + "\tNone\tPeer\t100000\t2.5ms\t" + get_ixp_connections(entry, ixp) + "\n"
                file.write(string)


def get_smaller_connection(AS1, AS2):
    if AS1.as_id < AS2.as_id:
        return str(AS1.as_id) + "." + str(AS2.as_id) + "."
    else:
        return str(AS2.as_id) + "." + str(AS1.as_id) + "."


def print_aslevel_links_students(list_of_ASes, list_of_IXPs):
    with open('aslevel_links_students.txt', 'w', newline='\n') as file:
        for entry in list_of_ASes:
            for customer in entry.customers:
                string = str(entry.as_id) + "\tPROV\tProvider\t" + str(
                    customer.as_id) + "\tCUST\tCustomer\t179." + str(entry.as_id) + "." + str(
                    customer.as_id) + "." + str(entry.as_id) + "/24\n"
                file.write(string)
            for provider in entry.providers:
                string = str(entry.as_id) + "\tCUST\tCustomer\t" + str(
                    provider.as_id) + "\tPROV\tProvider\t179." + str(provider.as_id) + "." + str(
                    entry.as_id) + "." + str(entry.as_id) + "/24\n"
                file.write(string)
            for peer in entry.peers:
                string = str(entry.as_id) + "\tPEER\tPeer\t" + str(
                    peer.as_id) + "\tPEER\tPeer\t179." + get_smaller_connection(entry, peer) + str(
                    entry.as_id) + "/24\n"
                file.write(string)
            for ixp in entry.ixps:
                string = str(entry.as_id) + "\tPEER\tPeer\t" + str(
                    80 + ixp.ixp_id) + "\tNone\tPeer\t180." + str(80 + ixp.ixp_id) + ".0." + str(
                    entry.as_id) + "/24\n"
                file.write(string)

        for ixp in list_of_IXPs:
            for connection in ixp.ixp_connections:
                string = str(80 + ixp.ixp_id) + "\tNone\tPeer\t" + str(connection.as_id) + "\tPEER\tPeer\t180." + str(
                    80 + ixp.ixp_id) + ".0." + str(80 + ixp.ixp_id) + "/24\n"
                file.write(string)


def print_l3_routers():
    with open('l3_routers.txt', 'w', newline='\n') as file:
        file.write("PEER\tDNS\thost:miniinterneteth/d_host\tvtysh\n")
        file.write("PROV\tMATRIX_TARGET\troutinator:miniinterneteth/d_routinator\tvtysh\n")
        file.write("CUST\tMATRIX\thost:miniinterneteth/d_host\tvtysh\n")


def print_l3_routers_krill():
    with open('l3_routers_krill.txt', 'w', newline='\n') as file:
        file.write("PEER\tDNS\tkrill:miniinterneteth/d_host\tvtysh\n")
        file.write("PROV\tMATRIX_TARGET\troutinator:miniinterneteth/d_routinator\tvtysh\n")
        file.write("CUST\tMATRIX\thost:miniinterneteth/d_host\tvtysh\n")


def print_l3_links():
    with open('l3_links.txt', 'w', newline='\n') as file:
        file.write("PEER\tPROV\t100000\t10ms\n")
        file.write("PEER\tCUST\t100000\t10ms\n")
        file.write("PROV\tCUST\t100000\t10ms\n")


if __name__ == "__main__":
    as_file_name = 'list_of_ASes_50.pkl'
    ixp_file_name = 'list_of_IXPs_50.pkl'
    ASes = []
    IXPs = []
    if os.path.exists(as_file_name) and os.path.exists(ixp_file_name):
        with open(as_file_name, 'rb') as as_file:
            ASes = pickle.load(as_file)
            print(f'Loaded {len(ASes)} ASes')
        with open(ixp_file_name, 'rb') as ixp_file:
            IXPs = pickle.load(ixp_file)
            print(f'Loaded {len(IXPs)} IXPs')
        print_AS_config(ASes, IXPs)
        print_aslevel_links(ASes)
        print_aslevel_links_students(ASes, IXPs)
        print_l3_routers()
        print_l3_routers_krill()
        print_l3_links()
