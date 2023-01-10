import routing
import painting

upper = []
lower = []
num = []

with open('input.txt', 'r') as file:
    lines = file.readlines()

    for line in lines:
        values = line.split()
        upper.append(values[0])
        lower.append(values[1])
num = [upper.pop(0), lower.pop(0)]

route = routing.Router(upper, lower)
output = route.getTrack()
paint = painting.Painter()
paint.draw(output[0], output[1], output[2])
paint.show()