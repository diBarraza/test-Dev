from datetime import date

from django.db.models.fields import NullBooleanField

import pytest

from adventure import models


@pytest.fixture
def car():
    return models.VehicleType(max_capacity=4)


@pytest.fixture
def van():
    return models.VehicleType(max_capacity=6)


@pytest.fixture
def tesla(car):
    return models.Vehicle(
        name="Tesla", passengers=3, vehicle_type=car, number_plate="AA-12-34"
    )


class TestVehicle:
    def test_capacity_greater_than_passengers(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=2)
        assert vehicle.can_start()

    def test_vehicle_overload(self, car):
        vehicle = models.Vehicle(vehicle_type=car, passengers=10)
        assert not vehicle.can_start()

    def get_distribution(self,vehicle):
        matrix = []
        rows = 0
        count = 0
        #definition large matrix
        if vehicle.passengers//2 == 0:
            rows = vehicle.passengers/2
        else:
            rows = (vehicle.passengers+1)/2
        rows = int(rows)
        for i in range(rows):
            matrix.append([])
            for j in range (2):
                if count > vehicle.passengers-1 :
                    matrix[i].append(False)
                else:
                    matrix[i].append(True)
                    count = count + 1

        return matrix

    def test_vehicle_distribution(self, car, van):
        # TODO: implement a method called "get_distribution" that returns a matrix filled of booleans
        # with the "standard distribution" in a vehicle, from top to bottom and left to right.
        # A Vehicle can have "n" rows with a maximum of 2 passengers per row.
        # The rows number depends on the vehicle max capacity.
        #
        # e.g: for 3 passengers
        # [
        #     [ True, True],
        #     [ True, False],
        # ]
        # for 5 passengers
        # [
        #     [ True, True],
        #     [ True, True],
        #     [ True, False],
        # ]
        
        vehicle = models.Vehicle(vehicle_type=car, passengers=3)
        distribution_expected = [[True, True], [True, False]]
        assert self.get_distribution(vehicle) == distribution_expected

        vehicle = models.Vehicle(vehicle_type=van, passengers=5)
        distribution_expected = [[True, True], [True, True], [True, False]]
        assert self.get_distribution(vehicle) == distribution_expected


    

    def validate_number_plate(self , string):
        try:
            vec = string.split('-')
        except:
            return False
        vec_numbers = ["0","1","2","3","4","5","6","7","8","9"]
        if len(vec) != 3:
            return False
        else:
            #comprobation
            minVec1 = list(vec[0])
            minVec2 = list(vec[1])
            minVec3 = list(vec[2])
            if minVec1[0] in vec_numbers or minVec1[1] in vec_numbers :
                return False
            else:
                if minVec2[0] not in vec_numbers or minVec2[1] not in vec_numbers :
                    return False
                else:
                    if minVec3[0] not in vec_numbers or minVec3[1] not in vec_numbers :
                        return False
        return True
        

    
    def test_valid_number_plate(self):
        # TODO: implement a function called "validate_number_plate"
        # a valid number plate consists of three pairs of alphanumeric chars separated by hyphen
        # the first pair must be letters and the rest must be numbers
        # e.g: AA-12-34
        assert self.validate_number_plate("AA-12-34") == True
        assert self.validate_number_plate("AA-BB-34") == False
        assert self.validate_number_plate("12-34-56") == False
        assert self.validate_number_plate("AA1234") == False
        assert self.validate_number_plate("AA 12 34") == False



class TestJourney:
    def is_finished(self,journey):
        if journey.start == journey.end:
            return True
        else:
            return False
    # TODO: implement "is_finished" method
    # a finished journey depends on the end value
    def test_is_finished(self, tesla):
        journey = models.Journey(start=date.today(), end=date.today(), vehicle=tesla)
        assert self.is_finished(journey) is True

    def test_is_not_finished(self, tesla):
        journey = models.Journey(start=date.today(), vehicle=tesla)
        assert self.is_finished(journey) is not True
