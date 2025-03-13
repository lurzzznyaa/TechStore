from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(
        max_length=123,
        verbose_name='First Name',
    )
    last_name = models.CharField(
        max_length=123,
        verbose_name='Second Name',
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Phone number'
    )
    avatar = models.ImageField(
        upload_to='media/user_avatar',
        verbose_name='Profile picture',
        blank=True,
        null=True
    )
    role = models.PositiveSmallIntegerField(
        choices=(
            (1, 'User'),
            (2, 'Moderator'),
            (3, 'Accountant'),
        ),
        default=1,
        verbose_name='Role'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    is_admin = models.BooleanField(
        default=False
    )
    is_otp_enabled = models.BooleanField(
        default=False
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class OTP(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    if_used = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
