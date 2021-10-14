import heapq
from collections import defaultdict, OrderedDict


class Car:
    def __init__(self, registration_number, color):
        self.registration_number = registration_number
        self.color = color

    def __str__(self):
        return "Car [registration_number=" + self.registration_number + ", color=" + self.color + "]"


class ParkingLot:
    def __init__(self):
        self.registration_slot_mapping = dict()
        self.color_registration_mapping = defaultdict(list)
        # we need to maintain the orders of cars while showing 'status'
        self.slot_car_mapping = OrderedDict()
        # initialize all slots as free
        self.available_parking_lots = []

    def create_parking_lot(self, total_slots):
        # Using min heap as this will always give minimum slot number in O(1) time
        print("Created a parking lot with {} slots".format(total_slots))
        for i in range(1, total_slots + 1):
            heapq.heappush(self.available_parking_lots, i)
        return True

    def status(self):
        print("Slot No.  Registration No  Colour")
        for slot, car in self.slot_car_mapping.items():
            print("{}         {}    {}".format(slot, car.registration_number, car.color))
        return True

    def get_nearest_slot(self):
        return heapq.heappop(self.available_parking_lots) if self.available_parking_lots else None

    def leave(self, slot_to_be_freed):
        found = None
        for registration_no, slot in self.registration_slot_mapping.items():
            if slot == slot_to_be_freed:
                found = registration_no

        # Cleanup from all cache
        if found:
            heapq.heappush(self.available_parking_lots, slot_to_be_freed)
            del self.registration_slot_mapping[found]
            car_to_leave = self.slot_car_mapping[slot_to_be_freed]
            self.color_registration_mapping[car_to_leave.color].remove(found)
            del self.slot_car_mapping[slot_to_be_freed]
            print("Slot number {} is free".format(slot_to_be_freed))
            return True

        else:
            print("slot is not in use")
            return False

    def park(self, car):
        slot_no = self.get_nearest_slot()
        if slot_no is None:
            print("Sorry, parking lot is full")
            return
        print("Allocated slot number: {}".format(slot_no))
        self.slot_car_mapping[slot_no] = car
        self.registration_slot_mapping[car.registration_number] = slot_no
        self.color_registration_mapping[car.color].append(car.registration_number)
        return slot_no

    # Registration numbers of all cars of a particular colour
    def registration_numbers_for_cars_with_colour(self, color):
        registration_numbers = self.color_registration_mapping[color]
        print(", ".join(registration_numbers))
        return self.color_registration_mapping[color]

    # Slot numbers of all slots where a car of a particular colour is parked
    def slot_numbers_for_cars_with_colour(self, color):
        registration_numbers = self.color_registration_mapping[color]
        slots = [self.registration_slot_mapping[reg_no] for reg_no in registration_numbers]
        print(", ".join(map(str, slots)))
        return slots

    def slot_number_for_registration_number(self, registration_number):
        slot_number = None
        if registration_number in self.registration_slot_mapping:
            slot_number = self.registration_slot_mapping[registration_number]
            print(slot_number)
            return slot_number
        else:
            print("Not found")
            return slot_number
        #from parking_lot import ParkingLot, Car

parking_lot = ParkingLot()

cars = [
    Car('KA-01-HH-1234', 'White'),
    Car('KA-01-HH-9999', 'White'),
    Car('KA-01-BB-0001', 'Black'),
    Car('KA-01-HH-7777', 'Red'),
    Car('KA-01-HH-2701', 'Blue'),
    Car('KA-01-HH-3141', 'Black'),
]

assert parking_lot.create_parking_lot(6) is True

for i in range(0, len(cars)):
    assert parking_lot.park(cars[i]) == i + 1

assert parking_lot.leave(4) is True
assert parking_lot.status() is True

assert len(parking_lot.available_parking_lots) == 1
assert parking_lot.park(Car('KA-01-P-333', 'White')) == 4
print("Sorry, parking lot is full")
assert parking_lot.registration_numbers_for_cars_with_colour('White') == ['KA-01-HH-1234', 'KA-01-HH-9999',
                                                                          'KA-01-P-333']
assert parking_lot.slot_numbers_for_cars_with_colour('White') == [1, 2, 4]
assert parking_lot.slot_number_for_registration_number('KA-01-HH-3141') == 6
assert parking_lot.slot_number_for_registration_number('MH-04-AY-1111') is None

import fileinput
import sys

#from parking_lot import ParkingLot, Car

parking_lot = ParkingLot()

def process(command_params):
    command_with_params = command_params.strip().split(' ')
    # print(command_with_params)
    command = command_with_params[0]

    if command == 'create_parking_lot':
        assert len(command_with_params) == 2, "create_parking_lot needs no of slots as well"
        assert command_with_params[1].isdigit() is True, "param should be 'integer type'"
        parking_lot.create_parking_lot(int(command_with_params[1]))

    elif command == 'park':
        assert len(command_with_params) == 3, "park needs registration number and color as well"
        car = Car(command_with_params[1], command_with_params[2])
        parking_lot.park(car)

    elif command == 'leave':
        assert len(command_with_params) == 2, "leave needs slot number as well"
        assert command_with_params[1].isdigit() is True, "slot number should be 'integer type'"

        parking_lot.leave(int(command_with_params[1]))
    elif command == 'status':
        parking_lot.status()

    elif command == 'registration_numbers_for_cars_with_colour':
        assert len(command_with_params) == 2, "registration_numbers_for_cars_with_colour needs color as well"
        parking_lot.registration_numbers_for_cars_with_colour(command_with_params[1])

    elif command == 'slot_numbers_for_cars_with_colour':
        assert len(command_with_params) == 2, "slot_numbers_for_cars_with_colour needs color as well"
        parking_lot.slot_numbers_for_cars_with_colour(command_with_params[1])

    elif command == 'slot_number_for_registration_number':
        assert len(command_with_params) == 2, "slot_number_for_registration_number needs registration_number as well"
        parking_lot.slot_number_for_registration_number(command_with_params[1])

    elif command == 'exit':
        exit(0)
    else:
        raise Exception("Wrong command")


        if len(sys.argv) == 1:
            while True:
                line = input()
                process(line)

        else:
            for line in fileinput.input():
                process(line)
