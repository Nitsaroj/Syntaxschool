from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=1)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')

    def __str__(self):
        return self.user.username


class Coin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_coins = models.PositiveIntegerField(default=0)
    spend_coins = models.PositiveIntegerField(default=0)
    reward_coins = models.PositiveIntegerField(default=0)

    def update_total_coins(self):
        """ Update total coins to reflect spend and reward coins balance. """
        self.total_coins = self.spend_coins + self.reward_coins
        self.save()

    def add_reward_coins(self, amount):
        """ Add reward coins and update total. """
        self.reward_coins += amount
        self.update_total_coins()

    def spend_coin_amount(self, amount):
        """ Spend coins from reward balance and add to spend coins if enough balance exists. """
        if self.reward_coins >= amount:
            self.reward_coins -= amount
            self.spend_coins += amount
            self.update_total_coins()
            return True
        return False  # Not enough reward coins

    def __str__(self):
        return f"{self.user.username} - Total: {self.total_coins}, Spend: {self.spend_coins}, Reward: {self.reward_coins}"

class CoinHistory(models.Model):
    COIN_TYPES = (
        ('reward', 'Reward'),
        ('spend', 'Spend')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_type = models.CharField(max_length=10, choices=COIN_TYPES)
    amount = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.coin_type} {self.amount} coins"