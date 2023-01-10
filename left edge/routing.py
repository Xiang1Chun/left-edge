class Router:

    def __init__(self, pinsUp, pinsLow):
        self.pinsUp, self.pinsLow = pinsUp, pinsLow
        self.HCG = self.getHCG(self.pinsUp, self.pinsLow)
        self.VCG = self.getVCG(self.pinsUp, self.pinsLow)
        self.order = self.getOrder(self.pinsUp, self.pinsLow)

    def getHCG(self, pinsUp, pinsLow):
        # create pins_local
        h_local = {}
        for i in range(len(pinsUp)):
            if pinsUp[i] != '0':
                if pinsUp[i] not in h_local:
                    h_local[pinsUp[i]] = []
                h_local[pinsUp[i]].append(i)
            if pinsLow[i] != '0':
                if pinsLow[i] not in h_local:
                    h_local[pinsLow[i]] = []
                h_local[pinsLow[i]].append(i)

        # construct HCG
        HCG = {}
        for i in h_local:
            if i not in HCG:
                HCG[i] = []
        for i in h_local:
            watermark = h_local[i][-1]
            for j in h_local:
                if str(j) not in HCG[i]:
                    if h_local[j][0] <= watermark <= h_local[j][-1] and i != j:
                        HCG[i].append(j)
                        HCG[j].append(i)
        return HCG


    def getVCG(self, pinsUp, pinsLow):
        VCG = []
        # construct all edge
        for i in range(len(pinsUp)):
            if pinsUp[i] != '0' and pinsLow[i] != '0':
                if (pinsUp[i], pinsLow[i]) not in VCG:
                    VCG.append((pinsUp[i], pinsLow[i]))

        # remove self edge
        remove = []
        for edge in VCG:
            if edge[0] == edge[1]:
                remove.append(edge)
        for edge in remove:
            VCG.remove(edge)
        return VCG


    def getOrder(self, pinsUp, pinsLow):
        order = []
        length = 0
        # construct 1st node
        for i in range(len(pinsUp)):
            if pinsUp[i] not in order  and pinsUp[i] != '0':
                order.append(pinsUp[i])
                break
            elif pinsLow[i] not in order and pinsLow[i] != '0':
                order.append(pinsUp[i])
                break

        # according to HCG ,construct order
        temp = 0
        while len(order) != length:
            length = len(order)
            for i in range(len(pinsUp)):
                j = len(order)
                if pinsUp[i] not in order and pinsUp[i] != '0':
                    if temp == 0 and pinsUp[i] not in self.HCG[order[j-1]] or temp == 1:
                        order.append(pinsUp[i])
                        temp = 0

                if pinsLow[i] not in order and pinsLow[i] != '0':
                    if temp == 0 and pinsLow[i] not in self.HCG[order[j-1]] or temp == 1:
                        order.append(pinsLow[i])
                        temp = 0
            temp = 1
        return order

    def getTrack(self):
        tracks = {}
        vertical = {}
        for i in range(len(self.pinsUp)):
            tracks[i] = []
            vertical[i] = []

        completed = []
        while True:
            act = 0
            # determine active order
            for pin in self.order:
                if pin not in [edge[1] for edge in self.VCG]:
                    if pin not in completed:
                        act = pin
                        break
            if act == 0:
                break

            # find track
            for track in range(len(tracks)):
                conflict = False
                for j in list(set(tracks[track] + vertical[track])):
                    if j in self.HCG[act]:
                        conflict = True
                vertical[track].append(act)
                if not conflict:
                    tracks[track].append(act)
                    vertical[track].remove(act)
                    break

            # remove current from VCG
            updated_VCG = []
            for edge in self.VCG:
                if edge[0] != act:
                    updated_VCG.append(edge)
            self.VCG = updated_VCG
            completed.append(act)

        # remove unassigned tracks
        remove = []
        for track in tracks:
            if not tracks[track]:
                remove.append(track)
        for track in remove:
            tracks.pop(track)
        return self.pinsUp, self.pinsLow, tracks

if __name__ == "__main__":
    #A = ['1', '1', '1', '2', '2', '5', '6', '3', '0', '4', '0']
    #B = ['2', '5', '0', '5', '5', '3', '3', '0', '6', '0', '4']
    A = ['1', '0', '0', '0', '4', '2', '0', '3', '0', '4', '0', '6']
    B = ['0', '2', '1', '3', '0', '0', '5', '0', '6', '0', '5', '0']
    r = Router(pinsUp = A, pinsLow = B)
    r.getTrack()