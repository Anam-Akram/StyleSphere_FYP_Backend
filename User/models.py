from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_tailor = models.BooleanField(default=False )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cnic = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_tailor', 'phone_number', 'cnic', 'gender','image']

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = None
        else:
            # Dynamically set the upload path
            self.image.field.upload_to = self.get_upload_to()
        super(UserAccount, self).save(*args, **kwargs)

    def get_upload_to(self):
        # Define the dynamic path here
        return f'static/profile_pictures/user_{self.id}/'

    def __str__(self):
        return f"Profile Picture uploaded at {self.uploaded_at}"
    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class OnlineUser(models.Model):
	user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

