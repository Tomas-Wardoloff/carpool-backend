from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Vehicle, CustomUser


class TestVehicleModel(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            email="example@user.com", password="password"
        )
        self.vehicle = Vehicle.objects.create(
            license_plate="ABC123", brand="Ford", model="Fiesta", owner=self.owner
        )

    def test_create_vehicle(self):
        self.assertEqual(self.vehicle.license_plate, "ABC123")
        self.assertEqual(self.vehicle.brand, "Ford")
        self.assertEqual(self.vehicle.model, "Fiesta")
        self.assertEqual(self.vehicle.owner, self.owner)

    def test_license_plate_is_required(self):
        with self.assertRaises(ValidationError):
            Vehicle.objects.create(brand="Ford", model="Fiesta", owner=self.owner)

    def test_license_plate_format(self):
        pass

    def test_license_plate_unique(self):
        pass

    def test_brand_is_required(self):
        with self.assertRaises(ValidationError):
            Vehicle.objects.create(
                license_plate="ABC123", model="Fiesta", owner=self.owner
            )

    def test_model_is_required(self):
        with self.assertRaises(ValidationError):
            Vehicle.objects.create(
                license_plate="ABC123", brand="Ford", owner=self.owner
            )

    def test_owner_is_required(self):
        with self.assertRaises(ValidationError):
            Vehicle.objects.create(license_plate="ABC123", brand="Ford", model="Fiesta")

    def test_access_owner_from_vehicle(self):
        self.assertEqual(self.vehicle.owner, self.owner)

    def teset_owner_is_deleted_with_vehicle(self):
        pass

    def test_vehicle_multiple_owners(self):
        pass

    def test_update_vehicle_owner(self):
        owner2 = CustomUser.objects.create_user(
            email="example2@user.com", password="password"
        )
        self.vehicle.owner = owner2
        self.vehicle.save()
        self.assertEqual(self.vehicle.owner, owner2)

    def test_brand_is_title_cased(self):
        self.assertEqual(self.vehicle.brand, "Ford")

    def test_model_is_title_cased(self):
        self.assertEqual(self.vehicle.model, "Fiesta")

    def test_str_method(self):
        self.assertEqual(str(self.vehicle), "Ford Fiesta ABC123")
