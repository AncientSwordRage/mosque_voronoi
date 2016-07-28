from django.db import models  # NOQA

# Create your models here.


class Mosque(models.Model):
    """Holds a mosque from mosque directory."""

    class Meta:
        """Meta McMetaface."""

        verbose_name = "Mosque"
        verbose_name_plural = "Mosques"
    mdpk = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    address = models.ForeignKey('address')
    gender_allowed = models.CharField(max_length=256)
    telephone = models.CharField(max_length=256)
    fax = models.CharField(max_length=256)
    capacity = models.SmallIntegerField()
    following = models.CharField(max_length=256)
    management = models.CharField(max_length=256)
    other_names = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    charity_no = models.PositiveIntegerField()
    data_accuracy = models.CharField(max_length=1)
    additional_notes = models.CharField(max_length=256)
    rating = models.SmallIntegerField()

    def __str__(self):
        """Return name of mosque."""
        return "{name} ({address})".format(name=self.name,
                                           address=self.address)


class Address(models.Model):
    """Address model."""

    class Meta:
        """Meta McMetaface."""

        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    address_line = models.CharField(max_length=256)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        """Return address without post code."""
        return self.address_line
