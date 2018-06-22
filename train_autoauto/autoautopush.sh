#!/bin/bash

for car in $(cat hostnames); do
    echo $car
    sshpass -f autoautopw ssh -o StrictHostKeyChecking=no pi@$car.local "sudo rm /home/student/\"$1\""
    sshpass -f autoautopw scp "$1" pi@$car.local:/home/student
    sshpass -f autoautopw ssh -o StrictHostKeyChecking=no pi@$car.local "sudo chown -R student:student /home/student/\"$1\""
done
