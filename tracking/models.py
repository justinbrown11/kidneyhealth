from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Comorbidity(models.Model):
    """
    The Comorbidity model
    \n
    Fields:
    - id
    - comorbid_description
    """
    comorbid_description = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.comorbid_description
    class Meta:
        db_table = "comorbidity"

class Race(models.Model):
    """
    The Race model
    \n
    Fields:
    - id
    - race_description
    """
    race_description = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.race_description
    class Meta:
        db_table = "race"

class Gender(models.Model):
    """
    The Gender model
    \n
    Fields:
    - id
    - gender_description
    """
    gender_description = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.gender_description
    class Meta:
        db_table = "gender"

class Profile(models.Model):
    """
    The User Profile model
    \n
    Fields:
    - user
    - comorbidity
    - race
    - gender
    - phone
    - weight
    - height
    - birth_date
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comorbidity = models.ForeignKey(Comorbidity, on_delete=models.DO_NOTHING)
    race = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=12)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.user.username
    class Meta:
        db_table = "user"

class Lab(models.Model):
    """
    The Lab model
    \n
    Fields:
    - id
    - user
    - lab_date
    - blood_pressure
    - potassium_level
    - phosphorous_level
    - sodium_level
    - creatinine_level
    - albumin_level
    - blood_sugar_level
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lab_date = models.DateField(default=date.today, blank=True)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    potassium_level = models.DecimalField(max_digits=5, decimal_places=2)
    phosphorous_level = models.DecimalField(max_digits=5, decimal_places=2)
    sodium_level = models.DecimalField(max_digits=5, decimal_places=2)
    creatinine_level = models.DecimalField(max_digits=5, decimal_places=2)
    albumin_level = models.DecimalField(max_digits=5, decimal_places=2)
    blood_sugar_level = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.lab_date}, {self.user}"
    class Meta:
        db_table = "lab"

class Food(models.Model):
    """
    The Food model
    \n
    Fields:
    - id
    - food_description
    - brand_name
    - serving_size
    - serving_size_unit
    - protein_g
    - phosphorus_mg
    - potassium_mg
    - sodium_mg
    """
    food_description = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=40, blank=True)
    serving_size = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    serving_size_unit = models.CharField(max_length=2, blank=True)
    protein_g = models.DecimalField(max_digits=6, decimal_places=2)
    phosphorus_mg = models.DecimalField(max_digits=6, decimal_places=2)
    potassium_mg = models.DecimalField(max_digits=6, decimal_places=2)
    sodium_mg = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return self.food_description
    class Meta:
        db_table = "food"

class DailyEntry(models.Model):
    """
    The DailyEntry model
    \n
    Fields:
    - id
    - user
    - entry_date
    - water_intake_liters
    - foods
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField(default=date.today(), blank=True)
    water_intake_liters = models.DecimalField(max_digits=4, decimal_places=2)
    foods = models.ManyToManyField(Food, through='FoodHistory')

    def __str__(self) -> str:
        return f"{self.entry_date}, {self.user}"
    class Meta:
        db_table = "daily_entry"

class FoodHistory(models.Model):
    """
    The FoodHistory model
    \n
    Fields:
    - id
    - user
    - food
    - quantity
    """
    entry = models.ForeignKey(DailyEntry, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self) -> str:
        return super().__str__()
    class Meta:
        db_table = "food_history"