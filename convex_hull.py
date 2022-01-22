import matplotlib.pyplot as plt
from typing import List, Tuple, Union


Point = Tuple[Union[int, float], Union[int, float]]
polar_angle = float


def compare(x: polar_angle, y: polar_angle):
    """Compares the polar angles of two points."""
    if x > y:
        return 1
    elif x < y:
        return -1
    else:
        return 0


def orientation(p: Point, q: Point, r: Point) -> Union[int, float]:
    """Returns the polar angle of a candidate for the next side of the convex hull."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])


def distance(p: Point, q: Point) -> float:
    """Returns distance between two Points."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy


def slope(p: Point, q: Point) -> float:
    """Returns the slope of the line going through points p and q."""
    return (p[1] - q[1]) / (p[0] - q[0]) if p[0] != q[0] else float('inf')


def jarvis_march(points: List[Point]):
    """Jarvis march algorithm.

    Implementation details:
    https://en.wikipedia.org/wiki/Gift_wrapping_algorithm

    """
    left_most_point = points[0]
    for point in points[1:]:
        if point[0] < left_most_point[0] or (point[0] == left_most_point[0] and point[1] < left_most_point[1]):
            left_most_point = point
    hull_points = [left_most_point]
    for p in hull_points:
        q = p
        for r in points:
            t = compare(orientation(p, q, r), 0)
            if t == 1 or t == 0 and distance(p, r) > distance(p, q):
                q = r
        if q != hull_points[0]:
            hull_points.append(q)
    return hull_points


def graham_scan(points: List[Point]):
    """Graham scam algorithm.

    Implementations details:
    https://en.wikipedia.org/wiki/Graham_scan

    """
    left_most_point = points[0]
    for point in points[1:]:
        if point[0] < left_most_point[0] or (point[0] == left_most_point[0] and point[1] < left_most_point[1]):
            left_most_point = point
    points.pop(points.index(left_most_point))

    points.sort(key=lambda p: (slope(p, left_most_point), -p[1], p[0]))

    hull_points = [left_most_point]
    for p in points:
        hull_points.append(p)
        while len(hull_points) > 2 and orientation(hull_points[-3], hull_points[-2], hull_points[-1]) < 0:
            hull_points.pop(-2)

    return hull_points


if __name__ == '__main__':
    # sample use case
    jarvis_points = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    jarvis_hull = jarvis_march(jarvis_points)
    print('Jarvis march test:')
    print('hull points: ', jarvis_hull)
    # add first point again to close the hull plot
    jarvis_hull += [jarvis_hull[0]]
    graham_points = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
    graham_hull = graham_scan(graham_points[:])
    print('Grahan scan test:')
    print('hull points: ', graham_hull)
    graham_hull += [graham_hull[0]]

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    for point in jarvis_points:
        ax[0].scatter(point[0], point[1], color='r', zorder=5)
    for start_vertex, end_vertex in zip(jarvis_hull[:-1], jarvis_hull[1:]):
        ax[0].plot([start_vertex[0], end_vertex[0]], [start_vertex[1], end_vertex[1]], color='b')
    ax[0].set_title('Jarvis march convex hull')

    for point in graham_points:
        ax[1].scatter(point[0], point[1], color='r', zorder=5)
    for start_vertex, end_vertex in zip(graham_hull[:-1], graham_hull[1:]):
        ax[1].plot([start_vertex[0], end_vertex[0]], [start_vertex[1], end_vertex[1]], color='b')
    ax[1].set_title('Graham scan convex hull')
    plt.show()

