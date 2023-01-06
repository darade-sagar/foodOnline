from django.db import models
from marketplace.models import FoodItem
from accounts.models import User

# Create your models here.
class Rating(models.Model):
    food_item = models.ForeignKey(FoodItem,on_delete=models.CASCADE,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    rate_value = models.PositiveIntegerField(blank=False)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('food_item', 'user'),)

    def __str__(self):
        return 'Rating for ' + self.food_item.food_title
