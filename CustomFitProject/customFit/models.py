from django.db import models
from django.conf import settings

class FoodCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    calories = models.FloatField()  # 열량
    sodium = models.FloatField()    # 나트륨
    sugars = models.FloatField()    # 당류
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


#CustomFit Health Cart 약칭으로 Cart라 하겠음
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}님의 맞춤 건강 카드"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.product_name}를 {self.Cart.user.username}님의 맞춤 건강 카드에 넣었습니다"