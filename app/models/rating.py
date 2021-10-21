from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Rating(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings')
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(max_length=1000)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rating'
        unique_together = [['user', 'product']]

    def __str__(self):
        return self.user.name + ' đã bình luận <' + self.comment + '> tại sản phẩm <' + self.product.name + '>'


class RatingResponse(models.Model):
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rating_responses')
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rating_response'

    def __str__(self):
        return self.user.name + ': ' + self.comment
