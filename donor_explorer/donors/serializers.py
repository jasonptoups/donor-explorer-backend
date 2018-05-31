from rest_framework import serializers
from .models import SavedDonor
from django.contrib.auth.models import User


class SavedDonorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SavedDonor
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'city',
                  'state',
                  'employer',
                  'occupation',
                  'average_donation',
                  'max_donation',
                  'mode_donation',
                  'total_donations',
                  'percent_dem',
                  'committees',
                  'user',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pk', 'donors',)


class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password',)
