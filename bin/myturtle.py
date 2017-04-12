import os
import csv
import turtle
from datetime import datetime
import re

# helper functions
def log(stage, msg):
    print(str(datetime.datetime.now()).split('.')[0] + " : " + stage + " : " + msg)

mainDataDir = os.path.dirname(os.path.abspath(__file__)) + '/../data'

lines = []

with open(mainDataDir + '/data_turtle/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    # skip the header
    next(reader)

    for line in reader:
        lines.append(line)

timespan = []
steering = []
speed = []

p = re.compile('IMG/center_\d\d(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)\.jpg')

lastTimeDict = None
lastSteering = None
lastSpeed = None

for line in lines:

    # getting the data
    m = p.match(line[0])

    timestring = m.group(3)+'/'+m.group(2)+'/'+m.group(1)+' '+m.group(4)+':'+m.group(5)+':'+m.group(6)+'.'+m.group(7)
    timeobject = datetime.strptime(timestring, '%d/%m/%y %H:%M:%S.%f')

    if lastTimeDict == None:
        lastTimeDict = {'day': int(m.group(3)), 'hour': int(m.group(4)), 'min': int(m.group(5)), 'sec': int(m.group(6)), 'milli': int(m.group(7))}
        lastSteering = float(line[3]) * 25.
        lastSpeed = float(line[6])
        continue
    
    nowDict = {'day': int(m.group(3)), 'hour': int(m.group(4)), 'min': int(m.group(5)), 'sec': int(m.group(6)), 'milli': int(m.group(7))}

    # det timespan between last time point and now
    if nowDict['milli'] > lastTimeDict['milli']:
        timespan.append(nowDict['milli'] - lastTimeDict['milli'])
    else:
        timespan.append(lastTimeDict['milli'] - nowDict['milli'])

    # det last steering and speed
    steering.append(lastSteering)
    speed.append(lastSpeed)

    # remember the new data for the next step
    lastTimeDict = {'day': int(m.group(3)), 'hour': int(m.group(4)), 'min': int(m.group(5)), 'sec': int(m.group(6)), 'milli': int(m.group(7))}
    lastSteering = float(line[3]) * 25.
    lastSpeed = float(line[6])

turtle.speed(1)

# draw the car
# 1cm = 1 turtle step
# 1m  = 100 turtle steps
# 1km = 100000 turtle steps
# 1mi = 160934.4 turtle steps

# 1 sec = 1000 milli
# 1 min = 60000 milli
# 1 h = 3600000 milli

for i in range(len(timespan)):
    print(timespan[i], ":", steering[i], ":", speed[i])

    if steering[i] == 0:
        turtleSteps = timespan[i] * 0.044704 * speed[i]
        print('forward ', turtleSteps)
        turtle.forward(turtleSteps)
    elif steering[i] < 0:
        radius = steering[i] * -1 * 2.
        turtleSteps = timespan[i] * speed[i]
        print('circle ', radius, turtleSteps)
        turtle.circle(radius, turtleSteps)
    elif steering[i] > 0:
        radius = steering[i] * 2.
        turtleSteps = timespan[i] * speed[i]
        print('circle ', radius, turtleSteps)
        turtle.circle(radius, turtleSteps)
   
print('min speed:', min(speed))
print('max speed:', max(speed))
print('min-max steering:', str(min(steering))+' <-> '+str(max(steering)))
