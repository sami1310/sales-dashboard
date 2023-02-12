from django.db import models

# Create your models here.

# category model for storing categories of the sales data
class Category(models.Model):
    category_name = models.CharField(max_length=40)
    
    #will rerturn category name in the admin panel 
    def __str__(self):
        return self.category_name
    
# region model for storing regions of the sales data
class Region(models.Model):
    region_name = models.CharField(max_length=20)
    
    #will rerturn region name in the admin panel 
    def __str__(self):
        return self.region_name

# Time period model for storing periods of the sales data
class Month(models.Model):
    month_name = models.CharField(max_length=20)
    
    #will rerturn month name in the admin panel 
    def __str__(self):
        return self.month_name

class SalesData(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    sales = models.PositiveIntegerField()

    #will rerturn selected fields in the admin panel
    def __str__(self):
        return self.category.category_name + ' - ' + self.region.region_name + ' - ' + self.month.month_name + ' - ' + str(self.sales)
    