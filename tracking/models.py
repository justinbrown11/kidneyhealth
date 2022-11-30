from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Comorbidity(models.Model):
    comorbid_description = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.comorbid_description
    class Meta:
        db_table = "comorbidity"

class Race(models.Model):
    race_description = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.race_description
    class Meta:
        db_table = "race"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comorbidity_ID = models.ForeignKey(Comorbidity, on_delete=models.DO_NOTHING)
    race_ID = models.ForeignKey(Race, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=2)
    phone = models.CharField(max_length=12)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.user.username
    class Meta:
        db_table = "user"

class Lab(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    lab_date = models.DateField(default=date.today, blank=True)
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    potassium_level = models.DecimalField(max_digits=5, decimal_places=2)
    phosphorous_level = models.DecimalField(max_digits=5, decimal_places=2)
    sodium_level = models.DecimalField(max_digits=5, decimal_places=2)
    creatinine_level = models.DecimalField(max_digits=5, decimal_places=2)
    albumin_level = models.DecimalField(max_digits=5, decimal_places=2)
    blood_sugar_level = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.date
    class Meta:
        db_table = "lab"

class DailyEntry(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField(default=date.today, blank=True)

    def __str__(self) -> str:
        return self.entry_date
    class Meta:
        db_table = "daily_entry"

class MealType(models.Model):
    meal_type_description = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.meal_type_description
    class Meta:
        db_table = "meal_type"

class Meal(models.Model):
    entry_ID = models.ForeignKey(DailyEntry, on_delete=models.CASCADE)
    meal_type_ID = models.ForeignKey(MealType, on_delete=models.DO_NOTHING)
    meal_number = models.IntegerField()

    def __str__(self) -> str:
        return super().__str__()
    class Meta:
        db_table = "meal"

class Food(models.Model):
    food_ID = models.BigIntegerField(primary_key=True)
    food_description = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.food_description
    class Meta:
        db_table = "food"

class FoodHistory(models.Model):
    meal_ID = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_ID = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=2, decimal_places=2)

    def __str__(self) -> str:
        return super().__str__()

    class Meta:
        db_table = "food_history"
        unique_together = (('meal_ID', 'food_ID'))