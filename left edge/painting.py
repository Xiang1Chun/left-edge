import cv2
import numpy as np
from itertools import combinations

class Painter:
    def __init__(self):
        self.diagram = None
        self.color_blue = (255, 0, 0)
        self.color_black = (0, 0, 0)
        self.color_red = (0, 0, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # create canvas
    def getCanvas(self, n_pinsUp, n_tracks):
        width = 150 + n_pinsUp * 30
        height = 100 + n_tracks * 30
        self.diagram = np.ones((height, width, 3), np.uint8) * 255


    def draw(self, pinsUp, pinsLow, tracks):
        self.getCanvas(len(pinsUp), len(tracks))
        spacing = 40

        #draw pin
        for i, pin in enumerate(pinsUp):
            cv2.putText(self.diagram, pin, (20 + i * spacing, 20), self.font, 0.5, self.color_blue, 1)

        for i, pin in enumerate(pinsLow):
            cv2.putText(self.diagram, pin, (20 + i * spacing, 50 + len(tracks)*20), self.font, 0.5, self.color_blue, 1)

        via = 0
        wirelength = 0
        #draw wire
        for track in tracks:
            for j in tracks[track]:
                h_coor = []
                v_coor = []

                # create the coordinates of the wire from pinsUp to track
                for i, pin in enumerate(pinsUp):
                    if pin == j:
                        wirelength += (track+1)
                        x = 25 + i * spacing
                        y = track * spacing // 2 + 35
                        v_coor.append([(x, 23), (x, y)])
                        h_coor.append((x, y))

                # create the coordinates of the wire from pinsLow to track
                for i, pin in enumerate(pinsLow):
                    if pin == j:
                        wirelength += (len(tracks)-track)
                        x = 25 + i * spacing
                        y = track * spacing // 2 + 35
                        low_y = 35 + len(tracks) * 20
                        v_coor.append([(x, low_y), (x, y)])
                        h_coor.append((x, y))

                # calculate coordinates on track
                h_local = {}
                for coordinate in combinations(h_coor, 2):
                    y = coordinate[1][1]
                    if y in h_local:
                        h_local[y] |= set(coordinate)
                    else:
                        h_local[y] = set(coordinate)
                for y in h_local:
                    h_local[y] = sorted(list(h_local[y]))

                # draw horizontal wire
                for x in h_local:
                    if len(h_local[x]) > 1:
                        via += len(h_local[x])
                    for i in range(len(h_local[x])-1):
                        wirelength += (h_local[x][i+1][0] - h_local[x][i][0]) // spacing
                        cv2.line(self.diagram, h_local[x][i], h_local[x][i+1], self.color_red, 1)

                #draw vertical wire
                for coordinate in v_coor:
                    cv2.line(self.diagram, coordinate[1], coordinate[0], self.color_black, 1)

        cv2.putText(self.diagram, 'tracks:' + str(len(tracks)) + '  wirelength:' + str(wirelength) + '  via:' + str(via)
                    , (10, 90 + len(tracks)*20), self.font, 0.5, self.color_black, 1)

    def show(self):
        cv2.imshow("Output", self.diagram)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    pin_track = (['1', '2', '0', '3'], ['1', '0', '2', '3'], {0: ['1', '2', '3']})
    p = Painter()
    p.draw(pin_track[0], pin_track[1], pin_track[2])
    p.show()