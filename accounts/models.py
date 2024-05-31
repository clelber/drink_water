from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()

    def __str__(self):
        return self.name


class Consumption(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.person.name} - {self.amount} ml on {self.date}'
