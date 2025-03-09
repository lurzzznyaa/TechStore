from django.db import models

class OrderStatisEnum(models.TextChoices):
    IN_PROCESSING = ('in_processing', 'В обработке')
    DECLINED = ('declined', 'Отклонено')
    ACCEPTED = ('accepted', 'Принято')

