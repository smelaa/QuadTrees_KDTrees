class KDTNode:
    def __init__(self, value, no_points=1):
        self.value = value
        self.no_points = no_points
        self.left = None
        self.right = None

class OrthagonalRange:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    def intersect(self, obj: KDTNode):
        if obj.no_points == 1:
            return True
        ran = obj.value
        if ran.x1 > self.x2 or ran.x2 < self.x1 or ran.y1 > self.y2 or ran.y2 < self.y1:
            return False
        return True

    def contain(self, obj: KDTNode):
        if obj.no_points == 1:
            x = obj.value[0]
            y = obj.value[1]
            return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
        ran = obj.value
        return self.x1 <= ran.x1 and self.x2 >= ran.x2 and self.y1 <= ran.y1 and self.y2 >= ran.y2

    def to_list(self):
        return [[(self.x1, self.y1), (self.x1, self.y2)], [(self.x2, self.y1), (self.x2, self.y2)],
                [(self.x1, self.y1), (self.x2, self.y1)], [(self.x1, self.y2), (self.x2, self.y2)]]


class KDTree:
    def __init__(self, points, ran, depth=0):
        if len(points) == 0: raise IndexError("KDTree cannot be empty")
        if len(points) == 1:
            self.root = KDTNode(points[0])
        else:
            if ran == None:
                ran = OrthagonalRange(min(P, key=lambda point: point[0])[0], max(P, key=lambda point: point[0])[0],
                                      min(P, key=lambda point: point[1])[1], max(P, key=lambda point: point[1])[1])
            k = len(points) // 2 - 1
            if depth % 2 == 0:
                points.sort(key=lambda point: point[1])
                new_y = (points[k][1] + points[k + 1][1]) / 2
                left_range = OrthagonalRange(ran.x1, ran.x2, ran.y1, new_y)
                right_range = OrthagonalRange(ran.x1, ran.x2, new_y, ran.y2)
            else:
                points.sort(key=lambda point: point[0])
                new_x = (points[k][0] + points[k + 1][0]) / 2
                left_range = OrthagonalRange(ran.x1, new_x, ran.y1, ran.y2)
                right_range = OrthagonalRange(new_x, ran.x2, ran.y1, ran.y2)
            self.root = KDTNode(ran, len(points))
            self.root.left = KDTree(points[:k + 1], left_range, depth + 1)
            self.root.right = KDTree(points[k + 1:], right_range, depth + 1)

    def leaves(self):
        if self.root.no_points == 1:
            return [self.root.value]
        return self.root.left.leaves() + self.root.right.leaves()

    def search(self, R: OrthagonalRange):
        if self.root.no_points == 1:
            if R.contain(self.root):
                return [self.root.value]
            return []
        result = []
        left = self.root.left
        right = self.root.right
        if R.contain(left.root):
            result = result + left.leaves()
        elif R.intersect(left.root):
            result = result + left.search(R)
        if R.contain(right.root):
            result = result + right.leaves()
        elif R.intersect(right.root):
            result = result + right.search(R)
        return result