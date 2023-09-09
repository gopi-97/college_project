
from django.db import models


class Users(models.Model):
    types=[
        ('Beginner','Beginner'),
        ('SmallScale','SmallScale'),
        ('LargeScale','LargeScale')
    ]
    username=models.CharField(max_length=100)
    userid=models.CharField(max_length=12,primary_key=True)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=20,choices=types)


    def __str__(self) -> str:
        return self.userid