from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    state = models.TextField()

    def __str__(self):
        return f'@{self.username} | {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class NewsLetter(models.Model):
    letter = models.CharField(max_length=4096)

    def __str__(self):
        return self.letter[:20] + '...'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class SubcategoryCategory(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subcategory.name} - {self.category.name}'

    class Meta:
        verbose_name = 'Подкатегория-категория'
        verbose_name_plural = 'Подкатегории-категории'


class Goods(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=64)
    caption = models.CharField(max_length=950, blank=True)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class SubcategoryGoods(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subcategory.name} - {self.goods.name}'

    class Meta:
        verbose_name = 'Подкатегория-товар'
        verbose_name_plural = 'Подкатегории-товары'


class UserBucket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'@{self.user.username} - {self.goods.name} - {self.amount}'

    class Meta:
        verbose_name = 'Пользователь - предмет - количество'
        verbose_name_plural = 'Пользователь - предмет - количество'


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=4096, blank=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос - ответ'
        verbose_name_plural = 'Вопрос - ответ'
