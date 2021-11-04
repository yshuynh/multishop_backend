from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from app.utils.constants import USER_ROLE


class Rating(models.Model):
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='ratings')
    is_solved = models.BooleanField(default=True)

    class Meta:
        db_table = 'rating'
        unique_together = [['user', 'product']]

    def __str__(self):
        return f'<ID:{self.id}><{self.user.name}><{self.comment}>'


class RatingResponse(models.Model):
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rating_responses')
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rating_response'

    def __str__(self):
        return f'<ID:{self.id}><{self.user.name}><{self.comment}>'

    def save(self, *args, **kwargs):
        print('saving...')
        if self.user.role == USER_ROLE.ADMIN:
            self.rating.is_solved = True
            self.rating.save()
        else:
            self.rating.is_solved = False
            self.rating.save()
        super(RatingResponse, self).save(**kwargs)
