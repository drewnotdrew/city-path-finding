from heapq import heappop, heappush
from itertools import count
import networkx as nx
import osmnx as ox

from networkx.algorithms.shortest_paths.weighted import _weight_function

# Copied this from the source. Put it here so it makes more sense to modify it.
@nx._dispatch(edge_attrs="weight", preserve_node_attrs="heuristic")
def my_astar_path(G, source, target, heuristic=None, weight="weight"):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    if heuristic is None:
        # The default heuristic is h=0 - same as Dijkstra's algorithm
        def heuristic(u, v):
            return 0

    push = heappush
    pop = heappop
    weight = _weight_function(G, weight)

    G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)

    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guaranteed unique for all nodes in the graph.
    c = count()
    queue = [(0, next(c), source, 0, None)]

    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    explored_stack = []

    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path, explored_stack

        if curnode in explored:
            # Do not override the parent of starting node
            if explored[curnode] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent
        explored_stack.append(explored.copy())

        for neighbor, w in G_succ[curnode].items():
            cost = weight(curnode, neighbor, w)
            if cost is None:
                continue
            ncost = dist + cost
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                # if qcost <= ncost, a less costly path from the
                # neighbor to the source was already determined.
                # Therefore, we won't attempt to push this neighbor
                # to the queue
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")

# Mostly copied from astar function. Takes a node in the explored dictionary
# and walks backwards to build its path.
def build_path(explored, node):
    path = [node]
    node = explored[node]
    while node is not None:
        try:
            path.append(node)
            node = explored[node]
        except:
            break
    path.reverse()
    return path

# Gets all terminal nodes in a given explored dictionary, builds their paths
# and returns them in a list.
def get_paths(explored):
    terminal = set(explored.keys()) - set(explored.values())

    return [build_path(explored, t) for t in terminal]

# Copied example shortest-path code
G = ox.graph_from_place("Piedmont, California, USA", network_type="drive")
G = ox.speed.add_edge_speeds(G)
G = ox.speed.add_edge_travel_times(G)

# Plot parameters
orig_long = -122.245846
orig_lat = 37.828903
dest_long = -122.215006
dest_lat = 37.812303
orig = ox.distance.nearest_nodes(G, X=orig_long, Y=orig_lat)
dest = ox.distance.nearest_nodes(G, X=dest_long, Y=dest_lat)
padding_percent = 0.02
plot_padding = padding_percent*max(abs(orig_long - dest_long), abs(orig_lat - dest_lat))
bb_north = max(orig_lat, dest_lat) + plot_padding
bb_east = max(orig_long, dest_long) + plot_padding
bb_south = min(orig_lat, dest_lat) - plot_padding
bb_west = min(orig_long, dest_long) - plot_padding
plot_bounding = (bb_north, bb_south, bb_east, bb_west)


def plot_step_diff(explored_stack, index):
    """
    Given an the explored stack of a path finding algorithm and an index, plot and export newly explored nodes
    """
    explored_current = explored_stack[index]
    explored_step_next = explored_stack[index + 1]
    difference = {key: value for key, value in explored_step_next.items() if key not in explored_current or explored_current[key] != value}
    difference_route = get_paths(difference)[0]
    path_step, ax = ox.plot_graph_route(G, difference_route, orig_dest_size=0, node_size=0, edge_linewidth=0, save=True, filepath=f"out/out{index}.svg", show=False, bbox=plot_bounding)


route, explored_stack = my_astar_path(G, orig, dest, weight="travel_time")

# Plot and export the background graph and the shortest path
fig, ax = ox.plot_graph_route(G, route, node_size=0, show=False)
main_map, ax = ox.plot_graph(G, node_size=0, save=True, filepath='out/map.svg', show=False, bbox=plot_bounding)
shortest_path, ax = ox.plot_graph_route(G, route, orig_dest_size=0, node_size=0, edge_linewidth=0, save=True, filepath='out/route.svg', show=False, bbox=plot_bounding)
print(len(explored_stack))
plot_step_diff(explored_stack, 200)

# # Find the difference between two iterations 
# explored_2 = explored_stack[1]
# explored = explored_stack[2]
# difference = {key: value for key, value in explored.items() if key not in explored_2 or explored_2[key] != value}
# difference_route = get_paths(difference)[0]
# # print(difference_route)
# path_step, ax = ox.plot_graph_route(G, difference_route, orig_dest_size=0, node_size=0, edge_alpha=0, save=True, filepath='out/path_step.svg', show=False)