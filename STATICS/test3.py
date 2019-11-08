import numpy as np
import math as ma
import  pygame

rect_list = []
r1=pygame.Rect((178,131,320,295))
r2=pygame.Rect((279,461,151,171))
rect_list.append(r1)
rect_list.append(r2)
a1=r1.colliderect(r2)
a2=r1.collidelistall(rect_list)
print(a2)
print(a1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Returns true if two rectangles(l1, r1)


# and (l2, r2) overlap
def doOverlap(l1, r1, l2, r2):
    # If one rectangle is on left side of other
    if (l1.x > r2.x or l2.x > r1.x):
        return False

    # If one rectangle is above other
    if (l1.y < r2.y or l2.y < r1.y):
        return False

    return True


# Driver Code
if __name__ == "__main__":
    l1 = Point(178, 131)
    r1 = Point(178+320, 131+295)
    l2 = Point(279, 461)
    r2 = Point(279+151, 461+171)

    if (doOverlap(l1, r1, l2, r2)):
        print("Rectangles Overlap")
    else:
        print("Rectangles Don't Overlap")

        # This code is contributed by Vivek Kumar Singh