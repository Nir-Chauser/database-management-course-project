from django.db import models

class Owners(models.Model):
    ownerid = models.IntegerField(db_column='ownerID', primary_key=True)
    oname = models.CharField(db_column='oName', max_length=50, blank=True, null=True)
    residencecity = models.CharField(db_column='residenceCity', max_length=50, blank=True, null=True)
    bdate = models.DateField(db_column='bDate', blank=True, null=True)

    class Meta:
        db_table = 'Owners'
        managed = False

class Apartments(models.Model):
    aid = models.IntegerField(db_column='aID', primary_key=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    roomsnum = models.IntegerField(db_column='roomsNum', blank=True, null=True)
    ownerid = models.ForeignKey(Owners, on_delete=models.DO_NOTHING, db_column='ownerID')

    class Meta:
        db_table = 'Apartments'
        managed = False

class Rentals(models.Model):
    renterid = models.IntegerField(db_column='renterID')
    ryear = models.IntegerField(db_column='rYear')
    aid = models.ForeignKey(Apartments, on_delete=models.DO_NOTHING, db_column='aID')
    cost = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Rentals'
        unique_together = (('renterid', 'ryear'),)
        managed = False
