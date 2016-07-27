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
    genders = models.CharField(max_length=256)
    telephone = models.CharField(max_length=256)
    fax = models.CharField(max_length=256)
    capacity = models.SmallIntegerField()
    following = models.CharField(max_length=256)
    management = models.CharField(max_length=256)
    other_names = models.CharField(max_length=256)
    mosque_type = models.CharField(max_length=256)
    charity_no = models.PositiveIntegerField()
    accuracy = models.CharField(max_length=1)
    railways = models.ManyToManyField('railway')
    additional_notes = models.TextField()
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


class Railway(models.Model):
    """Railway Model."""

    class Meta:
        """Meta McMetaface."""

        verbose_name = "Railway"
        verbose_name_plural = "Railways"

    station_name = models.CharField(max_length=256)

    def __str__(self):
        """Return station name."""
        return self.station_name
