from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Курс", help_text="Укажите курс"
    )
    preview = models.ImageField(
        upload_to="materials/courses/prewiew",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание курса",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Урок", help_text="Укажите урок"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Укажите описание курса",
    )
    preview = models.ImageField(
        upload_to="materials/lessons/prewiew",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    video_link = models.CharField(
        max_length=300, verbose_name="Ссылка на видео", blank=True, null=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
