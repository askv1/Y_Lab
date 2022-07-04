from random import shuffle
from functools import reduce
from itertools import accumulate


def find_route(points, n_init=20):

    path_list = []
    sum_list = []
    dist_list = []

    pair_dist = dict()

    for i in range(len(points)):
        for j in range(len(points)):

            x1 = points[i][0]
            x2 = points[j][0]
            y1 = points[i][1]
            y2 = points[j][1]

            pair_dist[points[i], points[j]] = ((x1-x2)**2 + (y1-y2)**2) ** 0.5

    for k in range(n_init):

        inner_points = points[1:]
        shuffle(inner_points)
        points = points[:1] + inner_points

        route = points[:3] + [points[0]]

        path_dist = []

        for i, p in enumerate(points[3:]):

            path_dist = [
                pair_dist[route[j-1], route[j]] for j in range(1, len(route))]

            point_dist = []

            for j, v in enumerate(route):
                point_dist.append(pair_dist[p, v])

            sums = []

            for j in range(len(path_dist)):

                sums.append(sum(path_dist) - path_dist[j] +
                            point_dist[j] + point_dist[j+1])

            min_ind = sums.index(min(sums)) + 1

            route = route[:min_ind] + [p] + route[min_ind:]

        path_dist = [
            pair_dist[route[j], route[j-1]] for j in range(1, len(route))]

        dist_list.append(path_dist)
        sum_list.append(sum(path_dist))
        path_list.append(route)

    ind = sum_list.index(min(sum_list))
    dist = [[]] + [[x] for x in accumulate(dist_list[ind])]
    route = path_list[ind]

    res = [(x[0], x[1]) for x in zip(route, dist)]

    txt = reduce(lambda a, b: ''.join(str(x) for x in a) + '->' + ''.join(
                    str(x) for x in b), res)

    return txt.replace('[]', '') + ' = ' + str(sum_list[ind])


points = [(0, 2), (2, 5), (5, 2), (6, 6), (8, 3)]

print(find_route(points))
