##By Gemma Tamagnini and Brian Sullivan
##NURTURE 2026 Umass Lowell
##08/06/2026
##
## AutoDewar is a liquid nitrogen fill protocol for HPGE detector dewars. 
## It utilizes a Raspberry pi 5, an optoisolated relay board,
## an MCP3008 ADC ,and a sensor board with two thermistor inputs to \
## sense LN2 flow in the manifold. When the sensor voltage drops below
## the set thresholds, the pi sends a signal to the relays to open or
## close the valves. Cycles are run every 1.5 seconds in the feedback loop.
##
##http://github.com/bsullit/AutoDewar

from gpiozero import MCP3008, OutputDevice
import time
import csv

#definitions
sensor1 = MCP3008(channel=1) #first sensor, used in stage 2 # reads voltage on first pin of ADC
sensor2 = MCP3008(channel=0) #second sensor, used in stage 3
vref = 3.3 #reference voltage for ADC, maximum output voltage (volts)
valve1 = OutputDevice(23) #relay in GPIO 23, active high #when on, valve is open
valve2 = OutputDevice(24) #relay in GPIO 24, active high
valve3 = OutputDevice(25) #relay in GPIO 25, active high
relay_power= OutputDevice(16) #transistor base pin, output HIGH to turn relay board on
threshold_s1 = 1.55 #thresholdold voltage drop for thermistor 1 to be considered "cold" (volts)
threshold_s2 = 1.45 #thresholdold voltage drop for thermistor 2 to be considered "cold" (volts)
max_time = 600 #maximum time elapsed for fill run (seconds)
wait_time = 30 #time to wait for liquid nitrogen to stop being expelled from the tube after valve 3 opens(seconds)
start_time = time.monotonic() #initializes timer at the beginning of the program
num_samples = 15 #number of samples taken, then averaged for sensor reading
sample_delay = 0.1 #delay between each sample reading taken
coldCounter = []

def drain(): #to drain lines of liquid nitrogen at  the end of fill process, or in the case of error
    valve1.off()
    valve2.on()
    valve3.off()
    print("draining...")
    time.sleep(wait_time) #wait for manifold to drain
    valve1.off()
    valve2.off()
    valve3.off()
    relay_power.off() #turns power off to the relay board
    print("all valves closed.")

def time_check(): #function for every clock check #if reaches time_max, fill process ends drain function happens, program ends
    elapsed_time = time.monotonic() - start_time #finds time since fill began (seconds)
    if elapsed_time > max_time:
        raise TimeoutError()
    else:
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
       
def sensor_samples(sensor):
    readings = []
    for _ in range(num_samples):
        readings.append(sensor.value * vref)
        time.sleep(sample_delay)
    return sum(readings)/len(readings)

def isCold(voltage, counter, threshold):#Verify line is cooled by counting how many consecutive cycles were at or below threshold 
    if (voltage <= threshold ):
        counter.append(True);
    else :#start count over if voltage is over threshold 
        counter = []

def read_sensor(sensor, num_sensor, threshold):#write voltage values to a csv file
    coldCounter = []
    filename = f"sensor_{num_sensor}_voltage.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Voltage"])
        while True:
            voltage = sensor_samples(sensor)
            print(f"Sensor {num_sensor}: {voltage:.2f}V")
            writer.writerow([voltage])
            file.flush()
            time_check()
            isCold(sensor.value*vref, coldCounter,threshold)
            if voltage < threshold and len(coldCounter) == 20:
                print(f"sensor {num_sensor} cold")
                break
            time.sleep(1)

def stage1(): #open valves 1 and 2
    print("stage 1 began...")
    relay_power.on()
    valve1.on()
    valve2.on()
    print("stage 1 complete")
   
def stage2(): #wait for sensor 1 to get cold, then close valve 2 and open valve 3
    print("stage 2 began...")
    read_sensor(sensor1, 1, threshold_s1)
    valve2.off()
    valve3.on()
    print("stage 2 complete")
   
def stage3(): #wait for line to clear liquid, then wait for sensor 2 to get cold, then close valve 3
    print("stage 3 began...")
    print("waiting for line to clear liquid...")
    time.sleep(wait_time) #wait for liquid to stop overflowing initially
    coldCounter= []#reset counter
    read_sensor(sensor2, 2, threshold_s2)
    valve1.off()
    valve2.on()
    valve3.on()
    print("stage 3 complete")
   
def off():
    valve1.off()
    valve2.off()
    valve3.off()
    relay_power.off()
   
def fillprocess():  
    print("fill process began...")
    global start_time
    start_time = time.monotonic() #writes a new start time each time the program is run so only that run will be timed
    stage1()
    stage2()
    stage3()
    drain()
    print("fill process complete. all valves closed.")

def main():
#     global coldCounter = []
    while True:
        choice = input("Run? (y/n): ").lower()
        if choice == "y":
            print("running...")
            try:
                fillprocess()
            except KeyboardInterrupt: #if we press ctrl c, fill ends and drain function happens
                drain()
                print("an error occured. fill process not complete.")
            except TimeoutError:
                drain()
                print("timed out: fill not complete")
            finally:
                off()
        elif choice == "n":
            print("not running...")
        else:
            print("please enter y or n")
   
if __name__ == "__main__":
    main()