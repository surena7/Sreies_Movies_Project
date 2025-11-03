from django.db import models





class Subscription(models.Model):
    time = models.CharField(max_length=201 , verbose_name="مدت زمان اشتراک")
    price = models.DecimalField(max_digits=10 , decimal_places=0 , verbose_name="قیمت اشتراک")
    otion1 = models.TextField(verbose_name="توضیحات اشتراک 1", null= True , blank=True)
    otion2 = models.TextField(verbose_name="توضیحات اشتراک 2", null= True , blank=True)
    otion3 = models.TextField(verbose_name="توضیحات اشتراک 3", null= True , blank=True)  
    otion4 = models.TextField(verbose_name="توضیحات اشتراک 4", null= True , blank=True)
    otion5 = models.TextField(verbose_name="توضیحات اشتراک 5", null= True , blank=True) 
    otion6 = models.TextField(verbose_name="توضیحات اشتراک 6", null= True , blank=True)
    otion7 = models.TextField(verbose_name="توضیحات اشتراک 7", null= True , blank=True)
    def __str__(self):
        return self.time