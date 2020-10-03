from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# # STUDENT
# class Student(models.Model):
#     """ a representation of the student """
    
#     name = models.CharField(max_length=100)
#     roll_num = models.IntegerField()
#     mess_id = models.IntegerField()

#     def __str__(self):
#         """ return a string representation of the model """
#         return self.name


# MESS EXTRAS
class  MessExtra(models.Model):
    """ a representaion of sides (mess extras) the mess is offering """

    name = models.CharField(max_length=100)
    price = models.FloatField()
    # distription will later be updated to include an image
    discription = models.CharField(max_length=200)
    quantity = models.IntegerField()

    def __str__(self):
        """ return a string representation of the model """
        return self.name


# ORDER (this represents the sides(extras) a students chooses to have)
class Order(models.Model):
    """ a representaion of the students chosen extras """

    student = models.ForeignKey(User,on_delete=models.CASCADE)
    extras_type = models.ForeignKey(MessExtra, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    # def __str__(self):
    #     """ return a string representation of the model """
    #     return self.

class Record(models.Model):
    """ a model for a the record """
    student_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    food_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.CharField(max_length=200)
    amount = models.IntegerField()

    def __str__(self):
        """ return a string representation """
        return self.order_id

 