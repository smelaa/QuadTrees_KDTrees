import numpy as np
class OrthagonalRange:
    def __init__(self, x1,x2,y1,y2):
        self.x1=min(x1,x2)
        self.x2=max(x1,x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
    def is_in(self, range):
        return self.x1>=range.x1 and self.x2<=range.x2 and self.y1>=range.y1 and self.y2<=range.y2
    def intersect(self,range):
        if range.x1>self.x2 or range.x2<self.x1 or range.y1>self.y2 or range.y2<self.y1:
            return False
        return True


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def is_in(self, range: OrthagonalRange):
        return range.x1<=self.x<=range.x2 and range.y1<=self.y<=range.y2

class KDTNode:
    def __init__(self, value, no_points=1):
        self.value=value
        self.no_points=no_points
        self.left=None
        self.right=None

class KDTree:
    def __init__(self, points, range, depth=0):
        if len(points)==0: raise IndexError("KDTree cannot be empty")
        if len(points)==1:
            self.root=KDTNode(points[0])
        else:
            k=len(points)//2
            if depth%2==0:
                part_points=np.partition(points,k, 1)
                new_y=(part_points[k][1]-part_points[k+1][1])/2
                new_range=(range.x1,range.x2,min(range.y1, new_y),max(range.y2,new_y))
            else:
                part_points = np.partition(points, k, 0)
                new_x = (part_points[k][0] - part_points[k + 1][0]) / 2
                new_range = (min(range.x1,new_x), max(range.x2,new_x), range.y1,range.y2)
            self.root=KDTNode(new_range, len(points))
            self.root.left=KDTree(points[:k+1],depth+1)
            self.root.right=KDTree(points[k+1:],depth+1)

    def leaves(self):
        if self.root.no_points == 1:
            return [self.root.value]
        return self.root.left.leaves+self.root.right.leaves

    def search(self, R: OrthagonalRange):
        if self.root.no_points==1:
            if self.root.value.is_in(R):
                return [self.root.value]
            return []
        result=[]
        left=self.root.left
        right=self.root.right
        if left.root.value.is_in(R):
            result=result+left.leaves
        elif left.root.value.intersect(R):
            result=result+left.search(R)
        if right.root.value.is_in(R):
            result=result+right.leaves
        elif right.root.value.intersect(R):
            result=result+right.search(R)
        return result









