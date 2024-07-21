from django.db import models

class FoodCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    Capacity = models.FloatField()  # 용량
    calories = models.FloatField()  # 열량
    sodium = models.FloatField()    # 나트륨
    sugars = models.FloatField()    # 당류
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name