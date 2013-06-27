from mathsupp import *


def make_polygon(points):
    return monotone_chain(points)


def leftmost_point(points):
    """ find the leftmost point """
    lm = points[0]
    index = 0
    for n in range(1, len(points)):
        p = points[n]
        if p[0] == lm[0]:
            if p[1] < lm[1]:
                lm = p
                index = n
        elif p[0] < lm[0]:
            lm = p
            index = n

    return lm, index


def more_to_left(i, j, q):
    """ is i more to the left than j, relative to q """
    
    vi, vj, vq = Vector2d(i), Vector2d(j), Vector2d(q)
    v1, v2 = vq - vi, vq - vj
    normal = v2.get_normal()

    result = dot_product(v1, normal)

    if result == 0:
        if v1.squared_length() > v2.squared_length():
            return True
    if result > 0:
        return True
    
    return False


def jarvis_march(points_list):
    """ the jarvis march algorithm for tracing a polygon """
    
    points = list((i[0], i[1]) for i in points_list)

    p2 = []
    pointOnHull, index = leftmost_point(points)

    while True:
        p2.append(pointOnHull)

        endpoint = points[0]
        index = 0
        for j in range(1, len(points)):
            if points[j] != pointOnHull and more_to_left(points[j], endpoint, pointOnHull):
                endpoint = points[j]
                index = j

        pointOnHull = endpoint
        if endpoint == p2[0]:
            break

        points.pop(index)
    
    return p2

#!!code below from wikipedia;

# 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
# Returns a positive value, if OAB makes a counter-clockwise turn,
# negative for clockwise turn, and zero if the points are collinear.
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    
def monotone_chain(points):
    """Computes the convex hull of a set of 2D points.
 
    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """
 
    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))
 
    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points
 
    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
 
    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
 
    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]


 
def ccw(v1, v2, v3):
    p1, p2, p3 = Vector2d(v1), Vector2d(v2), Vector2d(v3)
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)


"""
def graham_scan(points):
    N = len(points)
    let points[N+1] = the array of points
    swap points[1] with the point with the lowest y-coordinate
    sort points by polar angle with points[1]

    # We want points[0] to be a sentinel point that will stop the loop.
    let points[0] = points[N]

    # M will denote the number of points on the convex hull.
    let M = 1
    for i = 2 to N:
        # Find next valid point on convex hull.
        while ccw(points[M-1], points[M], points[i]) <= 0:
              if M > 1:
                      M -= 1
              # All points are collinear
              else if i == N:
                      break
              else
                      i += 1

        # Update M and swap points[i] to the correct place.
        M += 1
        swap points[M] with points[i]
"""

#!!end of wikipedia code

if __name__ == "__main__":
    #benchmarking
    from time import clock

    points = [(-10, -10), (-10, 790), (90, 790), (90, -10), \
              (-20, -20), (-20, 780), (80, 780), (80, -20), \
              (-10, -40), (-10, 760), (90, 760), (90, -40), \
              (0, -20), (0, 780), (100, 780), (100, -20)]

    runs = 10000

    a1 = clock()
    for i in range(runs):
        jarvis_march(points)
    a2 = clock()

    b1 = clock()
    for i in range(runs):
        monotone_chain(points)
    b2 = clock()

    print("jarvis march took", a2-a1, "secs")
    print("andrews monotone chain took", b2-b1, "secs")
    print("to do", runs, "for the set of points:")
    print(points)
