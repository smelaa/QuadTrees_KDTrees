class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 

class QTNode:
    def __init__(self, all_points, lower_left, width, height, points, k):
        self.lower_left = lower_left
        self.width = width
        self.height = height
        self.points = points
        self.all_points = all_points
        self.children = []
        self.lines = []
        self.k = k

    def seek_points(self, lower_left, width, height):
        result = []
        for point in self.points:
            if lower_left.x <= point.x <= lower_left.x + width and lower_left.y <= point.y <= lower_left.y + height:
                result.append(point)
        return result
    
    def new_point(self, xadd = 0, yadd = 0):
        return Point(self.lower_left.x+xadd, self.lower_left.y+yadd)

    def divide_node(self):
        
        if len(self.points) > self.k:
            new_width = self.width / 2
            new_height = self.height / 2
            ll = self.new_point() # lower left
            points = self.seek_points(ll, new_width, new_height)
            lower_left_branch = QTNode(self.all_points, ll, new_width, new_height, points, self.k)
            
            lower_left_branch.divide_node()
            
            lr = self.new_point(new_width, 0) # lower right
            points = self.seek_points(lr, new_width, new_height)
            lower_right_branch = QTNode(self.all_points, lr, new_width, new_height, points, self.k)
            
            lower_right_branch.divide_node()
            
            ul = self.new_point(0, new_height) # upper left
            points = self.seek_points(ul, new_width, new_height)
            upper_left_branch = QTNode(self.all_points, ul, new_width, new_height, points, self.k)
            
            upper_left_branch.divide_node()
            
            ur = self.new_point(new_width, new_height) # upper right
            points = self.seek_points(ur, new_width, new_height)
            upper_right_branch = QTNode(self.all_points, ur, new_width, new_height, points, self.k)
            
            upper_right_branch.divide_node()
            
            self.children = [lower_left_branch, lower_right_branch, 
                             upper_left_branch, upper_right_branch]
            
                
    def find(self, rec_lower_left, rec_upper_right, result):
        if len(self.children) == 0: # jest dzieckiem
            for point in self.points:
                if rec_lower_left.x <= point.x <= rec_upper_right.x and rec_lower_left.y <= point.y <= rec_upper_right.y:
                    result.append(point)
            return result
        
        if self.lower_left.x >= rec_lower_left.x and self.lower_left.x + self.width <= rec_upper_right.x \
        and self.lower_left.y >= rec_lower_left.y and self.lower_left.y + self.height <= rec_upper_right.y: # zawiera się w x zawiera się w y
            for point in self.points:
                result.append(point)  
            return result
        
        if self.lower_left.x > rec_upper_right.x or self.lower_left.x + self.width < rec_lower_left.x \
        or self.lower_left.y > rec_upper_right.y or self.lower_left.y + self.height < rec_lower_left.y:
            return result
        
        for child in self.children: # sprawdź dzieci
            child.find(rec_lower_left, rec_upper_right, result)
        return result
        
                    
class QuadTree:
    def __init__(self, points, k):
        self.left = min(points, key=lambda point: point.x) 
        self.right = max(points, key=lambda point: point.x)
        self.down = min(points, key=lambda point: point.y)
        self.up = max(points, key=lambda point: point.y) 
        self.lower_left = Point(self.left.x - 1e-9, self.down.y - 1e-9)
        self.width = self.right.x - self.left.x + 2* 1e-9
        self.height = self.up.y - self.down.y + 2* 1e-9
        self.points = points
        self.k = k
        self.root = QTNode(self.points, self.lower_left, self.width, self.height, self.points, self.k)
        self.root.divide_node()

    
    def find_points(self, rec_lower_left, rec_upper_right):
        result = []
        self.root.find(rec_lower_left, rec_upper_right, result)
        return result