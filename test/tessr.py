import heapq
from collections import defaultdict, OrderedDict


class Car:
    def __init__(self, registration_number, color):
        self.registration_number = registration_number
        self.color = color

    def __str__(self):
        return "Car [registration_number=" + self.registration_number + ", color=" + self.color + "]"


class ParkingLot:
    def __init__(self, total_slots):
        self.registration_slot_mapping = dict()
        self.color_registration_mapping = defaultdict(list)
        # we need to maintain the orders of cars while showing 'status'
        self.slot_car_mapping = OrderedDict()

        # initialize all slots as free
        self.available_parking_lots = []
        # Using min heap as this will always give minimun slot number in O(1) time
        for i in range(1, total_slots + 1):
            heapq.heappush(self.available_parking_lots, i)

    def status(self):
        for slot, car in self.slot_car_mapping.items():
            print("Slot no: {} {}".format(slot, car))

    def get_nearest_slot(self):
        return heapq.heappop(self.available_parking_lots) if self.available_parking_lots else None

    def free_slot(self, slot_to_be_freed):
        found = None
        for registration_no, slot in self.registration_slot_mapping.items():
            if slot == slot_to_be_freed:
                found = registration_no

        # Cleanup from all cache
        if found:
            del self.registration_slot_mapping[found]
            car_to_leave = self.slot_car_mapping[slot_to_be_freed]
            self.color_registration_mapping[car_to_leave.color].remove(found)
            del self.slot_car_mapping[slot_to_be_freed]
            print("leave ", slot_to_be_freed)
        else:
            print("slot is not in use")

    def park_car(self, car):
        slot_no = self.get_nearest_slot()
        if slot_no is None:
            print("Sorry, parking lot is full")
            return
        self.slot_car_mapping[slot_no] = car
        self.registration_slot_mapping[car.registration_number] = slot_no
        self.color_registration_mapping[car.color].append(car.registration_number)

    # ● Registration numbers of all cars of a particular colour.
    def get_registration_nos_by_color(self, color):
        return self.color_registration_mapping[color]

    # ● Slot numbers of all slots where a car of a particular colour is parked.
    def get_slot_numbers_by_color(self, color):
        return [self.registration_slot_mapping[reg_no] for reg_no in self.color_registration_mapping[color]]


if __name__ == "__main__":
    parking_lot = ParkingLot(6)
    print(parking_lot.available_parking_lots)

    car = Car("KA-01-HH-1234", "White")
    parking_lot.park_car(car)

    car = Car("KA-01-HH-9999", "White")
    parking_lot.park_car(car)

    car = Car("KA-01-BB-0001", "Black")
    parking_lot.park_car(car)

    car = Car("KA-01-HH-7777", "Red")
    parking_lot.park_car(car)

    car = Car("KA-01-HH-2701", "Blue")
    parking_lot.park_car(car)

    car = Car("KA-01-HH-3141", "Black")
    parking_lot.park_car(car)

    # When no slots are available then
    slot_no = parking_lot.get_nearest_slot()
    print(slot_no)
    slot_no = parking_lot.get_nearest_slot()
    print(slot_no)

    # Leave slot no 4
    slot_no_to_be_freed = 4
    parking_lot.free_slot(slot_no_to_be_freed)

    heapq.heappush(parking_lot.available_parking_lots, 4)

    car = Car("KA-01-P-333", "White")
    parking_lot.park_car(car)

    car = Car("DL-12-AA-9999", "White")
    parking_lot.park_car(car)
    parking_lot.status()
    print(parking_lot.available_parking_lots)
    print(parking_lot.registration_slot_mapping)
    print(parking_lot.color_registration_mapping)

    registration_numbers = parking_lot.get_registration_nos_by_color('White')
    print("White : {}".format(registration_numbers))
    registration_numbers = parking_lot.get_registration_nos_by_color('Red')
    print("Red : {}".format(registration_numbers))
    registration_numbers = parking_lot.get_registration_nos_by_color('Black')
    print("Black : {}".format(registration_numbers))

    slot_nos = parking_lot.get_slot_numbers_by_color('White')
    print("White : {}".format(slot_nos))
    slot_nos = parking_lot.get_slot_numbers_by_color('Red')
    print("Red : {}".format(slot_nos))
    slot_nos = parking_lot.get_slot_numbers_by_color('Black')
    print("Black : {}".format(slot_nos))
    parking_lot.status()
    parking_lot.free_slot(1)
    parking_lot.free_slot(2)
    parking_lot.free_slot(3)
    parking_lot.status()