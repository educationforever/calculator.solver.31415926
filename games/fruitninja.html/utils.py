"""
Utility classes and functions for the game
"""
import math

class CollisionDetector:
    @staticmethod
    def point_to_line_distance(x, y, x1, y1, x2, y2):
        """
        Calculate the distance from a point (x,y) to a line segment defined by (x1,y1) and (x2,y2)
        """
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            return math.sqrt(A * A + B * B)
        
        param = dot / len_sq
        
        if param < 0:
            xx = x1
            yy = y1
        elif param > 1:
            xx = x2
            yy = y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D
        
        dx = x - xx
        dy = y - yy
        
        return math.sqrt(dx * dx + dy * dy)
