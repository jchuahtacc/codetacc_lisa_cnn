#!/bin/bash


for car in $(cat hostnames); do
    echo $car
    sshpass -f autoautopw ssh -o StrictHostKeyChecking=no pi@$car.local "tar zcvf ${car}data.tar.gz /home/student/capture_data"
    sshpass -f autoautopw scp pi@$car.local:${car}data.tar.gz .
done
