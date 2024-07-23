from django.db import models
from django.conf import settings

# 상품 카테고리
class FoodCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

# 상품
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    Capacity = models.FloatField()  # 용량
    calories = models.FloatField()  # 열량
    sodium = models.FloatField()    # 나트륨
    sugars = models.FloatField()    # 당류
    protein = models.FloatField()   # 단백질
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    

# 맞춤 건강 카트
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}님의 맞춤 건강 카트입니다."

# 맞춤 건강 카트 안에 들어갈 상품
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.product_name}를 {self.cart.user.username}님의 카트에 넣었습니다"