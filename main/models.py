# Import the necessary modules for creating models
from django.db import models
# Import the User model from Django's built-in authentication system
from django.contrib.auth.models import User

# Define the ProductionPlan model class
class ProductionPlan(models.Model):
    # Primary key field for the ProductionPlan model, automatically incremented
    id = models.BigAutoField(primary_key=True)
    # CharField to store the name of the production plan with a maximum length of 200 characters
    name = models.CharField(max_length=200)  # Plan Name
    # ForeignKey to associate the production plan with a user, deletes the plan if the user is deleted
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # IntegerField to store the length of the production plan
    length = models.IntegerField()  # Plan Length
    # BooleanField to indicate whether input has been made for the plan, defaults to False
    filled = models.BooleanField(default=False)  # Input Made?

    # Input Fields
    # IntegerFields to store the demand for each month, defaulting to 0
    demand1 = models.IntegerField(default=0)  # Demand for Month 1
    demand2 = models.IntegerField(default=0)  # Demand for Month 2
    demand3 = models.IntegerField(default=0)  # Demand for Month 3
    demand4 = models.IntegerField(default=0)  # Demand for Month 4
    demand5 = models.IntegerField(default=0)  # Demand for Month 5
    demand6 = models.IntegerField(default=0)  # Demand for Month 6
    demand7 = models.IntegerField(default=0)  # Demand for Month 7
    demand8 = models.IntegerField(default=0)  # Demand for Month 8
    demand9 = models.IntegerField(default=0)  # Demand for Month 9
    demand10 = models.IntegerField(default=0)  # Demand for Month 10
    demand11 = models.IntegerField(default=0)  # Demand for Month 11
    demand12 = models.IntegerField(default=0)  # Demand for Month 12

     
    # Dates fields
    start_date = models.DateField(default='2025-01-01')   # Starting date of the production plan
    end_date = models.DateField(null=True, blank=True)  # Optional ending date of the production plan
     # Add any other specific monthly date fields if necessary, e.g.,
    month1_date = models.DateField(null=True, blank=True)  # Date for Month 1
    month2_date = models.DateField(null=True, blank=True)  # Date for Month 2
    month3_date = models.DateField(null=True, blank=True)
    month4_date = models.DateField(null=True, blank=True)
    month5_date = models.DateField(null=True, blank=True)
    month6_date = models.DateField(null=True, blank=True)
    month7_date = models.DateField(null=True, blank=True)
    month8_date = models.DateField(null=True, blank=True)
    month9_date = models.DateField(null=True, blank=True)
    month10_date = models.DateField(null=True, blank=True)
    month11_date = models.DateField(null=True, blank=True)
    month12_date = models.DateField(null=True, blank=True)
    
    # IntegerField to store the number of permanent workers, defaulting to 0
    numPermanent = models.IntegerField(default=0)  # Number of Permanent Worker(s)
    # IntegerField to store the production rate of a permanent worker, defaulting to 0
    prodPermanent = models.IntegerField(default=0)  # Production of a Permanent Worker
    # IntegerField to store the production rate of a temporary worker, defaulting to 0
    prodTemporary = models.IntegerField(default=0)  # Production of a Temporary Worker
    # DecimalField to store the hiring cost of a temporary worker, max digits 19 and 2 decimal places, defaulting to 0
    costHiring = models.DecimalField(max_digits=19, decimal_places=2, default=0)  # Temporary Worker Hiring Cost
    # DecimalField to store the firing cost of a temporary worker, max digits 19 and 2 decimal places, defaulting to 0
    costFiring = models.DecimalField(max_digits=19, decimal_places=2, default=0)  # Temporary Worker Firing Cost
    # DecimalField to store the monthly holding cost per unit, max digits 19 and 2 decimal places, defaulting to 0
    costHoldingUnit = models.DecimalField(max_digits=19, decimal_places=2, default=0)  # Monthly Holding Cost per Unit
    # IntegerField to store the initial inventory level, defaulting to 0
    inventoryInitial = models.IntegerField(default=0)  # Initial Inventory Level
    # IntegerField to store the final inventory level at the end of month 12, defaulting to 0
    inventoryFinal = models.IntegerField(default=0)  # Final Inventory Level / Ending Inventory for Month 12

    # Optimized Output Fields
    # IntegerFields to store the ending inventory for each month, defaulting to 0
    inventoryMonth1 = models.IntegerField(default=0)  # Ending Inventory for Month 1
    inventoryMonth2 = models.IntegerField(default=0)  # Ending Inventory for Month 2
    inventoryMonth3 = models.IntegerField(default=0)  # Ending Inventory for Month 3
    inventoryMonth4 = models.IntegerField(default=0)  # Ending Inventory for Month 4
    inventoryMonth5 = models.IntegerField(default=0)  # Ending Inventory for Month 5
    inventoryMonth6 = models.IntegerField(default=0)  # Ending Inventory for Month 6
    inventoryMonth7 = models.IntegerField(default=0)  # Ending Inventory for Month 7
    inventoryMonth8 = models.IntegerField(default=0)  # Ending Inventory for Month 8
    inventoryMonth9 = models.IntegerField(default=0)  # Ending Inventory for Month 9
    inventoryMonth10 = models.IntegerField(default=0)  # Ending Inventory for Month 10
    inventoryMonth11 = models.IntegerField(default=0)  # Ending Inventory for Month 11
    # IntegerFields to store the number of temporary workers hired for each month, defaulting to 0
    hiredTemporary1 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 1
    hiredTemporary2 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 2
    hiredTemporary3 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 3
    hiredTemporary4 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 4
    hiredTemporary5 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 5
    hiredTemporary6 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 6
    hiredTemporary7 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 7
    hiredTemporary8 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 8
    hiredTemporary9 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 9
    hiredTemporary10 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 10
    hiredTemporary11 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 11
    hiredTemporary12 = models.IntegerField(default=0)  # Number of Temporary Worker Hired for Month 12
    # IntegerFields to store the number of temporary workers fired for each month, defaulting to 0
    firedTemporary1 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 1
    firedTemporary2 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 2
    firedTemporary3 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 3
    firedTemporary4 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 4
    firedTemporary5 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 5
    firedTemporary6 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 6
    firedTemporary7 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 7
    firedTemporary8 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 8
    firedTemporary9 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 9
    firedTemporary10 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 10
    firedTemporary11 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 11
    firedTemporary12 = models.IntegerField(default=0)  # Number of Temporary Worker Fired for Month 12
    # IntegerFields to store the number of temporary workers for each month, defaulting to 0
    numberTemporary1 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 1
    numberTemporary2 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 2
    numberTemporary3 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 3
    numberTemporary4 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 4
    numberTemporary5 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 5
    numberTemporary6 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 6
    numberTemporary7 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 7
    numberTemporary8 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 8
    numberTemporary9 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 9
    numberTemporary10 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 10
    numberTemporary11 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 11
    numberTemporary12 = models.IntegerField(default=0)  # Number of Temporary Worker for Month 12
    # DecimalField to store the optimized cost for multi-period planning, max digits 19 and 2 decimal places, defaulting to 0
    optimalCost = models.DecimalField(max_digits=19, decimal_places=2, default=0)  # Optimized Cost for Multi-Period Planning
