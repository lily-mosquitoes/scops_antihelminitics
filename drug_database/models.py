from django.db import models


class ActiveComponent(models.Model):

    active_component = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.active_component


class Company(models.Model):

    class Meta:
        verbose_name_plural = "companies"

    company = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.company


class Product(models.Model):

    product_name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    active_component = models.ManyToManyField('ActiveComponent')

    def __str__(self):
        return self.product_name


class DrugUse(models.Model):

    class Meta:
        verbose_name = "drug's mode of use"
        verbose_name_plural = "drugs' mode of use"

    mode_of_use = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.mode_of_use


class SheepDrugType(models.Model):

    # group needs to be able to be NULL so group can be optional on SheepDrug
    group = models.CharField(max_length=50, null=True)
    label = models.CharField(max_length=10, blank=True)
    colour = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if self.label == '' or self.colour == '':
            return self.group
        else:
            return f"{self.group} - {self.label} ({self.colour})"


class SheepDrug(models.Model):

    type = models.ForeignKey(SheepDrugType, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mode_of_use = models.ForeignKey(DrugUse, on_delete=models.CASCADE)
    trace_elements = models.CharField(max_length=50, blank=True)
    meat_withdrawl_period = models.IntegerField()
    target_pathogens = models.ManyToManyField('SheepPathogen')

    def __str__(self):
        return f"{self.product} ({self.mode_of_use})"


class SheepPathogen(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
