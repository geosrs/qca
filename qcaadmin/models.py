from django.db import models

class InitialCondition(models.Model):
    title = models.CharField(max_length=400)
    data = models.TextField()
    length = models.IntegerField()

    def __str__(self):
        return self.title + " ("+str(self.length)+" sites)"

class SimResult(models.Model):
    V = models.CharField(max_length=10) #local gate
    R = models.IntegerField() #ECA Rule: 6, 102, 150, etc
    # possibilities: 204, 201, 198, 195, 156, 153, 150, 147, 108, 105, 102, 99, 60, 57, 54, 51
    # interesting:
    IC = models.ForeignKey(InitialCondition)
    MODE_CHOICES = (
        (True, "Sweep"),
        (False, "Block"),
    )
    mode = models.BooleanField(choices=MODE_CHOICES) #True: Sweep, False: Block
    T = models.IntegerField()
    location = models.CharField(max_length=500)
    completed = models.BooleanField()

    def __str__(self):
        string = "Block"
        if self.mode: string = "Sweep"
        return self.V + " - " + str(self.R) + " - " + string + " - " + str(self.IC)
