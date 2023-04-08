from pathlib import Path

import pandas as pd


def read_network(network_file):
    with open(network_file, "r") as f:
        lines = f.readlines()
        idx = lines.index("\n")
        lines = lines[idx + 1 :]
        network = []
        for line in lines:
            line = line.strip()
            user1, user2 = line.split(",")
            user1 = int(user1)
            user2 = int(user2)
            network.append((user1, user2))
    return network


def read_cascades(cascades_file):
    with open(cascades_file, "r") as f:
        lines = f.readlines()
        idx = lines.index("\n")
        lines = lines[idx + 1 :]
        cascades = []
        for line in lines:
            line = line.strip()
            participates = line.split(";")
            cascade = []
            for participate in participates:
                user, time = participate.strip(",")
                user = int(user)
                time = float(time)
                cascade.append((user, time))
            cascades.append(cascade)
    return cascades


def read_dataset(
    dataset_path, cascades_file_name="cascades.txt", network_file_name="network.txt"
):
    dataset_path = Path(dataset_path)
    network_file = dataset_path / network_file_name
    cascades_file = dataset_path / cascades_file_name
    network = read_network(network_file)
    cascades = read_cascades(cascades_file)
    return network, cascades
