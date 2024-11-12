from django.shortcuts import render, redirect  # Import functions for rendering templates and handling redirects.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Import pagination classes.
from django.http import HttpResponse, HttpResponseRedirect  # Import HTTP response classes.
from main import models  # Import models from the main app.
from django.contrib.auth.decorators import login_required  # Import decorator for requiring login.
from django.contrib.auth import logout  # Import logout function.
from pulp import *  # Import PuLP library for optimization.
from .forms import *  # Import all forms from the current directory.
from .models import ProductionPlan  # Import ProductionPlan model from the current directory.
import xlwt  # Import xlwt for creating Excel files.
from io import BytesIO  # Import BytesIO for in-memory byte streams.
from django.conf import settings  # Import settings from Django configuration.
from django.contrib import messages  # Import messages for displaying notifications.
import plotly.graph_objects as go  # Import Plotly for creating graphs.
from django.core.mail import send_mail  # Import send_mail function for sending emails.
import requests

def index(request):    
    if request.method == "POST":  # Check if the request method is POST.
        if request.user.is_authenticated:  # Check if the user is authenticated.
            inputName = str(request.POST.get('name'))  # Get the input name from the POST request.
            inputMonthRange = int(request.POST.get('length'))  # Get the input month range from the POST request.
            queryCheck = ProductionPlan.objects.filter(name=inputName).exists()  # Check if a ProductionPlan with the same name exists.
            while queryCheck == True:  # If a plan with the same name exists, append '_copy' until a unique name is found.
                inputName = inputName+'_copy'
                queryCheck = ProductionPlan.objects.filter(name=inputName).exists()
            ProductionPlan.objects.create(name=inputName, username=request.user, length=inputMonthRange)  # Create a new ProductionPlan.
            return redirect('get-plan-list')  # Redirect to the plan list page.
        else:
            return redirect('login')  # Redirect to the login page if the user is not authenticated.
    return render(request, 'main/index.html')  # Render the index page.

@login_required(login_url='/login/')  # Require login to access this view.
def get_plan_list(request):
    searchColumn = request.GET.get("column")  # Get the search column from the GET request.
    searchWord = request.GET.get("search")  # Get the search word from the GET request.
    if searchColumn == "name" and searchWord:  # Filter plans by name if the search column is 'name'.
        planList = ProductionPlan.objects.filter(username=request.user, name__icontains=searchWord).order_by('length')
    elif searchColumn == "length" and searchWord:  # Filter plans by length if the search column is 'length'.
        planList = ProductionPlan.objects.filter(username=request.user, length=searchWord).order_by('length')
    else:  # If no search parameters are provided, return all plans for the user.
        planList = ProductionPlan.objects.filter(username=request.user).order_by('length')
    paginator = Paginator(planList, 5)  # Show 5 plans per page.

    page_number = request.GET.get("page")  # Get the page number from the GET request.
    try:
        page_obj = paginator.get_page(page_number)  # Get the desired page object.
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # If the page number is not an integer, show the first page.
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # If the page is empty, show the last page.
    print(page_obj)
    return render(request, "main/planList.html", {'page_obj': page_obj})  # Render the plan list page with pagination.

def about(request):
    return render(request, "main/about.html")  # Render the about page.

def logout_view(request):
    logout(request)  # Log the user out.
    return redirect('home')  # Redirect to the login page.

@login_required(login_url='/login/')  # Require login to access this view.
def delete_plan(request, plan_ID):
    plan = ProductionPlan.objects.filter(id=plan_ID, username=request.user)  # Get the plan to be deleted.
    plan.delete()  # Delete the plan.
    return redirect('get-plan-list')  # Redirect to the plan list page.

def initiate_plan_optimize(request, plan_ID):
    plan = ProductionPlan.objects.filter(id=plan_ID).values()  # Get the plan details.
    return view_plan_detail(request, plan_ID, plan[0]["length"])  # Call the view_plan_detail function with the plan details.

def initiate_sensitivity_analysis(request, plan_ID):
    plan = ProductionPlan.objects.filter(id=plan_ID).values()  # Get the plan details.
    return sensitivity_analysis(request, plan_ID, plan[0]["length"])  # Call the sensitivity_analysis function with the plan details.

@login_required(login_url='/login/')  # Require login to access this view.
def input_plan_variables(request, plan_ID):
    if request.method == "POST":  # Check if the request method is POST.
        inputDemand1 = request.POST.get('demand1')  # Get the demand for month 1 from the POST request.
        inputDemand2 = request.POST.get('demand2')  # Get the demand for month 2 from the POST request.
        inputDemand3 = request.POST.get('demand3')  # Get the demand for month 3 from the POST request.
        inputDemand4 = request.POST.get('demand4')  # Get the demand for month 4 from the POST request.
        inputDemand5 = request.POST.get('demand5')  # Get the demand for month 5 from the POST request.
        inputDemand6 = request.POST.get('demand6')  # Get the demand for month 6 from the POST request.
        inputDemand7 = request.POST.get('demand7')  # Get the demand for month 7 from the POST request.
        inputDemand8 = request.POST.get('demand8')  # Get the demand for month 8 from the POST request.
        inputDemand9 = request.POST.get('demand9')  # Get the demand for month 9 from the POST request.
        inputDemand10 = request.POST.get('demand10')  # Get the demand for month 10 from the POST request.
        inputDemand11 = request.POST.get('demand11')  # Get the demand for month 11 from the POST request.
        inputDemand12 = request.POST.get('demand12')  # Get the demand for month 12 from the POST request.
        inputNumPermanent = request.POST.get('numPermanent')  # Get the number of permanent employees from the POST request.
        inputProdPermanent = request.POST.get('prodPermanent')  # Get the production rate of permanent employees from the POST request.
        inputProdTemporary = request.POST.get('prodTemporary')  # Get the production rate of temporary employees from the POST request.
        inputCostHiring = request.POST.get('costHiring')  # Get the hiring cost from the POST request.
        inputCostFiring = request.POST.get('costFiring')  # Get the firing cost from the POST request.
        inputCostHoldingUnit = request.POST.get('costHoldingUnit')  # Get the holding cost per unit from the POST request.
        inputInventoryInitial = request.POST.get('inventoryInitial')  # Get the initial inventory from the POST request.
        inputInventoryFinal = request.POST.get('inventoryFinal')  # Get the final inventory from the POST request.
        ProductionPlan.objects.filter(id=plan_ID).update(  # Update the ProductionPlan with the new values.
            demand1 = inputDemand1, 
            demand2 = inputDemand2, 
            demand3 = inputDemand3, 
            demand4 = inputDemand4,
            demand5 = inputDemand5,
            demand6 = inputDemand6, 
            demand7 = inputDemand7, 
            demand8 = inputDemand8,
            demand9 = inputDemand9,
            demand10 = inputDemand10, 
            demand11 = inputDemand11, 
            demand12 = inputDemand12,
            numPermanent = inputNumPermanent,
            prodPermanent = inputProdPermanent,
            prodTemporary = inputProdTemporary,
            costHiring = inputCostHiring,
            costFiring = inputCostFiring,
            costHoldingUnit = inputCostHoldingUnit,
            inventoryInitial = inputInventoryInitial,
            inventoryFinal = inputInventoryFinal,
            filled = True
        )
        return redirect('get-plan-list')  # Redirect to the plan list page.
    else:
        plan = ProductionPlan.objects.filter(id=plan_ID).values()  # Get the plan details.
    return render(request, 'main/input_variables.html', {'plan': plan})  # Render the input variables page with the plan details.

def view_plan_detail(request, plan_ID, num_months):  # Define a function to view plan details.
    status = optimize_plan(plan_ID, num_months)  # Optimize the plan and get the status.
    if status == 1:  # Check if the optimization was successful.
        detail = ProductionPlan.objects.filter(id=plan_ID).values()  # Get the plan details from the database.
        rehire_termination_data = []  # To store rehire and termination data for API

        for x in detail:  # Loop through the plan details.
            total_hiring_cost = 0  # Initialize total hiring cost.
            total_firing_cost = 0  # Initialize total firing cost.
            total_holding_cost = 0  # Initialize total holding cost.

            demands = []  # Initialize list for demands.
            hiring_costs = []  # Initialize list for hiring costs.
            firing_costs = []  # Initialize list for firing costs.
            holding_costs = []  # Initialize list for holding costs.

            worker_numbers = [0]  # Initialize list for worker numbers.
            months = ['Start']  # Initialize list for months.

            # New lists for rehire and terminate employees
            rehire_employees = []  
            terminate_employees = []

            for month in range(1, num_months + 1):  # Loop through each month.
                demand = x[f'demand{month}'] - (x['numPermanent'] * x['prodPermanent'])  # Calculate the demand for the month.
                if month == 1:  # Check if it is the first month.
                    demand -= x['inventoryInitial']  # Subtract initial inventory from the demand.
                if demand < 0:  # Check if demand is negative.
                    demand = 0  # Set demand to 0 if negative.
                demands.append(demand)  # Append demand to the list.
                
                hC = x[f'hiredTemporary{month}'] * x['costHiring']  # Calculate hiring cost for the month.
                fC = x[f'firedTemporary{month}'] * x['costFiring']  # Calculate firing cost for the month.

                # Calculate the number of employees to rehire and terminate for this month
                rehire_count = x[f'hiredTemporary{month}']
                terminate_count = x[f'firedTemporary{month}']
                
                # Append rehire and termination counts to lists for each month
                rehire_employees.append(rehire_count)
                terminate_employees.append(terminate_count)

                if month != num_months:  # Check if it is not the last month.
                    
                    ihc = x['costHoldingUnit'] * x[f'inventoryMonth{month}']  # Calculate holding cost for the month.
                    holding_costs.append(ihc)  # Append holding cost to the list.
                    total_holding_cost += ihc  # Add holding cost to total holding cost.
                
                hiring_costs.append(hC)  # Append hiring cost to the list.
                firing_costs.append(fC)  # Append firing cost to the list.

                total_hiring_cost += hC  # Add hiring cost to total hiring cost.
                total_firing_cost += fC  # Add firing cost to total firing cost.
                
                worker_numbers.append(x[f'numberTemporary{month}'])  # Append number of temporary workers to the list.
                months.append(f'Month {month}')  # Append month name to the list.

                # Collect rehire and termination data for API response
                rehire_termination_data.append({
                    'month': month,
                    'rehire_count': rehire_count,
                    'terminate_count': terminate_count
                })
            
            # STEP 1: Prepare API Payload
            api_payload = {
                'plan_id': plan_ID,
                'num_months': num_months,
                'rehire_termination_data': rehire_termination_data
            }
            api_url = "#"  # actual endpoint
            headers = {
                'Authorization': 'Bearer YOUR_API_TOKEN',  # Add authentication if required
                'Content-Type': 'application/json'
            }

            # STEP 2: Send Data to External System
            try:
                response = requests.post(api_url, json=api_payload, headers=headers)
                if response.status_code == 200:  # Check for success
                    messages.success(request, "Rehire and termination data sent successfully.")
                else:
                    messages.error(request, f"Failed to send data: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"API request failed: {str(e)}")

            # FIGURES
            
            # Figure 1 : Total Cost Distribution (Malaysian Ringgit)
            labels = ['Inventory Holding Cost', 'Temp. Worker Hiring Cost', 'Temp. Worker Firing Cost']  # Define labels for the pie chart.
            values = [total_holding_cost, total_hiring_cost, total_firing_cost]  # Define values for the pie chart.
            colors = ['#636efa', '#00cc96', '#ef553b']  # Define colors for the pie chart.

            fig1Light = go.Figure(data=[go.Pie(labels=labels, textinfo='label+percent', values=values, hole=0.3, marker=dict(colors=colors))])  # Create a pie chart figure for light mode.
            fig1Light.update_layout(title='TOTAL COST DISTRIBUTION', showlegend=False)  # Update layout of the pie chart for light mode.
            
            fig1Dark = go.Figure(data=[go.Pie(labels=labels, textinfo='label+percent', values=values, hole=0.3, marker=dict(colors=colors))])  # Create a pie chart figure for dark mode.
            fig1Dark.update_layout(title='TOTAL COST DISTRIBUTION', showlegend=False, template='plotly_dark')  # Update layout of the pie chart for dark mode.
            
            # Figure 2 : Monthly Cost
            fig2Light = go.Figure(data=[
                go.Bar(name='Inventory Holding Cost', x=months[1:], y=holding_costs, marker=dict(color=colors[0])),  # Create a bar chart for holding costs in light mode.
                go.Bar(name='Hiring Cost', x=months[1:], y=hiring_costs, marker=dict(color=colors[1])),  # Create a bar chart for hiring costs in light mode.
                go.Bar(name='Firing Cost', x=months[1:], y=firing_costs, marker=dict(color=colors[2])),  # Create a bar chart for firing costs in light mode.
            ])
            fig2Light.update_layout(barmode='stack', title='MONTHLY COST', yaxis_title='Costs')  # Update layout of the bar chart for light mode.

            fig2Dark = go.Figure(data=[
                go.Bar(name='Inventory Holding Cost', x=months[1:], y=holding_costs, marker=dict(color=colors[0])),  # Create a bar chart for holding costs in dark mode.
                go.Bar(name='Hiring Cost', x=months[1:], y=hiring_costs, marker=dict(color=colors[1])),  # Create a bar chart for hiring costs in dark mode.
                go.Bar(name='Firing Cost', x=months[1:], y=firing_costs, marker=dict(color=colors[2])),  # Create a bar chart for firing costs in dark mode.
            ])
            fig2Dark.update_layout(barmode='stack', title='MONTHLY COST', yaxis_title='Costs', template='plotly_dark')  # Update layout of the bar chart for dark mode.

            # Figure 3 : Net Number of Temporary Workers per Month
            fig3Light = go.Figure(data=[go.Scatter(x=months, y=worker_numbers, mode='lines+markers', name="Number of Temporary Workers")])  # Create a line chart for number of temporary workers in light mode.
            fig3Light.update_layout(title='Net Number of Temporary Workers per Month', yaxis_title='Net Number of Temporary Workers')  # Update layout of the line chart for light mode.
            
            fig3Dark = go.Figure(data=[go.Scatter(x=months, y=worker_numbers, mode='lines+markers', name="Number of Temporary Workers")])  # Create a line chart for number of temporary workers in dark mode.
            fig3Dark.update_layout(title='Net Number of Temporary Workers per Month', yaxis_title='Net Number of Temporary Workers', template='plotly_dark')  # Update layout of the line chart for dark mode.

            # Figure 4 : Rehire and Termination Numbers per Month
            rehiring_counts = [x[f'hiredTemporary{month}'] for month in range(1, num_months + 1)]  # Extract rehiring data.
            termination_counts = [x[f'firedTemporary{month}'] for month in range(1, num_months + 1)]  # Extract termination data.

            fig4Light = go.Figure(data=[
                go.Bar(name='Rehired Employees', x=months[1:], y=rehiring_counts, marker=dict(color='#00cc96')),  # Rehire data in light mode.
                go.Bar(name='Terminated Employees', x=months[1:], y=termination_counts, marker=dict(color='#ef553b'))  # Termination data in light mode.
            ])
            fig4Light.update_layout(barmode='group', title='Rehire and Termination Numbers per Month', yaxis_title='Number of Employees')

            fig4Dark = go.Figure(data=[
                go.Bar(name='Rehired Employees', x=months[1:], y=rehiring_counts, marker=dict(color='#00cc96')),  # Rehire data in dark mode.
                go.Bar(name='Terminated Employees', x=months[1:], y=termination_counts, marker=dict(color='#ef553b'))  # Termination data in dark mode.
            ])
            fig4Dark.update_layout(barmode='group', title='Rehire and Termination Numbers per Month', yaxis_title='Number of Employees', template='plotly_dark')


        return render(request, "main/optimize.html", {  # Render the optimize template with the plan details and figures.
            'detail': detail, 
            'demands': demands, 
            'holding_costs': holding_costs,
            'hiring_costs': hiring_costs, 
            'firing_costs': firing_costs, 
            'total_hiring_cost': total_hiring_cost, 
            'total_firing_cost': total_firing_cost, 
            'total_holding_cost': total_holding_cost,
            'rehire_employees': rehire_employees,  # Added for the template
            'terminate_employees': terminate_employees,  # Added for the template 
            'fig1Light': fig1Light.to_html(full_html=False),  # Convert fig1Light to HTML for embedding.
            'fig1Dark': fig1Dark.to_html(full_html=False),  # Convert fig1Dark to HTML for embedding.
            'fig2Light': fig2Light.to_html(full_html=False),  # Convert fig2Light to HTML for embedding.
            'fig2Dark': fig2Dark.to_html(full_html=False),  # Convert fig2Dark to HTML for embedding.
            'fig3Light': fig3Light.to_html(full_html=False),  # Convert fig3Light to HTML for embedding.
            'fig3Dark': fig3Dark.to_html(full_html=False),  # Convert fig3Dark to HTML for embedding.
            'fig4Light': fig4Light.to_html(full_html=False),  # New rehire/terminate chart for light mode.
            'fig4Dark': fig4Dark.to_html(full_html=False),  # New rehire/terminate chart for dark mode.
            'rehire_termination_data': rehire_termination_data  # Added for transparency in UI if needed
        })
    
    elif status == 0:  # Check if the plan could not be solved.
        messages.error(request, "PLAN COULD NOT BE SOLVED")  # Display an error message.
    elif status == -1:  # Check if the plan is not feasible.
        messages.error(request, "PLAN IS NOT FEASIBLE")  # Display an error message.
    elif status == -2:  # Check if the plan results are unbounded.
        messages.error(request, "PLAN RESULTS IS UNBOUNDED")  # Display an error message.
    elif status == -3:  # Check if the plan results are undefined.
        messages.error(request, "PLAN RESULTS IS UNDEFINED")  # Display an error message.
    return redirect('get-plan-list')  # Redirect to the plan list page.

def sensitivity_analysis(request, plan_ID, num_months):  # Function definition with parameters: request, plan_ID, and num_months
    detail = ProductionPlan.objects.filter(id=plan_ID).values()  # Query the ProductionPlan table for the specified plan_ID and get the values
    adDemands = []  # List to store allowable decrease in demands
    aiDemands = []  # List to store allowable increase in demands
    decreasedDemands = []  # List to store demands after decrease
    increasedDemands = []  # List to store demands after increase
    
    for x in detail:  # Iterate over the details of the production plan
        # Extract relevant values from the production plan details
        inputDemands = [int(x[f'demand{i+1}']) for i in range(num_months)]  # List of demands for each month
        inputNumPermanent = int(x['numPermanent'])  # Number of permanent workers
        inputProdPermanent = int(x['prodPermanent'])  # Production rate of permanent workers
        inputProdTemporary = int(x['prodTemporary'])  # Production rate of temporary workers
        inputCostHiring = float(x['costHiring'])  # Cost of hiring
        inputCostFiring = float(x['costFiring'])  # Cost of firing
        inputCostHoldingUnit = float(x['costHoldingUnit'])  # Holding cost per unit
        inputInventoryInitial = int(x['inventoryInitial'])  # Initial inventory
        inputInventoryFinal = int(x['inventoryFinal'])  # Final inventory
        inputOptimalCost = int(x['optimalCost'])  # Optimal cost

        for i in range(1, num_months + 1):  # Loop through each month
            original_cost = inputOptimalCost  # Store the original optimal cost
            original_demand = inputDemands[i-1]  # Store the original demand for the month
            step_size = min(inputProdPermanent, inputProdTemporary)  # Define the perturbation step size
            aiDemand = 0  # Initialize allowable increase in demand
            adDemand = 0  # Initialize allowable decrease in demand
            iteration = 0  # Initialize iteration counter for increase perturbation
            
            while iteration < 100:  # Perform iterative perturbation to increase demand
                inputDemands[i-1] += step_size  # Increase the demand by step size
                
                # Define the linear programming problem to minimize cost
                month = list(range(num_months))
                monthIHC = list(range(num_months - 1))
                model = LpProblem("Minimize Cost", LpMinimize)
                
                # Define decision variables
                ihcDict = LpVariable.dicts('IHC', monthIHC, lowBound=0, cat='Integer')  # Inventory holding cost variables
                hcDict = LpVariable.dicts('HC', month, lowBound=0, cat='Integer')  # Hiring cost variables
                fcDict = LpVariable.dicts('FC', month, lowBound=0, cat='Integer')  # Firing cost variables
                ntwDict = LpVariable.dicts('NTW', month, lowBound=0, cat='Integer')  # Number of temporary workers variables
                
                # Objective function: minimize the sum of holding, hiring, and firing costs
                model += (lpSum([inputCostHoldingUnit * ihcDict[i] for i in monthIHC]) +
                          lpSum([inputCostHiring * hcDict[i] for i in month]) +
                          lpSum([inputCostFiring * fcDict[i] for i in month]))
                
                # Add constraints to the model based on inventory and production
                if num_months == 1:
                    model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) ==
                                        inputDemands[0] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name='ihcCons1')
                else:
                    model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) ==
                                        inputDemands[0] - (inputNumPermanent * inputProdPermanent) + ihcDict[0], name='ihcCons1')
                    
                    for i in range(1, num_months - 1):
                        model.addConstraint(ihcDict[i-1] + (inputProdTemporary * ntwDict[i]) ==
                                            inputDemands[i] - (inputNumPermanent * inputProdPermanent) + ihcDict[i], name=f'ihcCons{i+1}')
                    
                    model.addConstraint(ihcDict[num_months - 2] + (inputProdTemporary * ntwDict[num_months - 1]) ==
                                        inputDemands[num_months - 1] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name=f'ihcCons{num_months}')
                
                model.addConstraint(ntwDict[0] == hcDict[0] - fcDict[0], name='ntwCons1')
                
                if num_months > 1:
                    for i in range(1, num_months):
                        model.addConstraint(ntwDict[i] == ntwDict[i-1] + (hcDict[i] - fcDict[i]), name=f'ntwCons{i+1}')
                
                model.solve(pulp.PULP_CBC_CMD(timeLimit=5))  # Solve the linear programming problem with a time limit
                
                if model.status == 1:  # Check if the optimal solution is found
                    if value(model.objective) != original_cost:  # If the optimal cost changes
                        aiDemand = step_size * iteration  # Store the allowable increase in demand
                        break
                
                iteration += 1  # Increment the iteration counter

            inputDemands[i-1] = original_demand  # Reset the demand to its original value
            iteration = 0  # Initialize iteration counter for decrease perturbation
            
            while iteration < 200:  # Perform iterative perturbation to decrease demand
                inputDemands[i-1] -= step_size  # Decrease the demand by step size
                
                # Define the linear programming problem to minimize cost
                month = list(range(num_months))
                monthIHC = list(range(num_months - 1))
                model = LpProblem("Minimize Cost", LpMinimize)
                
                # Define decision variables
                ihcDict = LpVariable.dicts('IHC', monthIHC, lowBound=0, cat='Integer')  # Inventory holding cost variables
                hcDict = LpVariable.dicts('HC', month, lowBound=0, cat='Integer')  # Hiring cost variables
                fcDict = LpVariable.dicts('FC', month, lowBound=0, cat='Integer')  # Firing cost variables
                ntwDict = LpVariable.dicts('NTW', month, lowBound=0, cat='Integer')  # Number of temporary workers variables
                
                # Objective function: minimize the sum of holding, hiring, and firing costs
                model += (lpSum([inputCostHoldingUnit * ihcDict[i] for i in monthIHC]) +
                          lpSum([inputCostHiring * hcDict[i] for i in month]) +
                          lpSum([inputCostFiring * fcDict[i] for i in month]))
                
                # Add constraints to the model based on inventory and production
                if num_months == 1:
                    model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) ==
                                        inputDemands[0] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name='ihcCons1')
                else:
                    model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) ==
                                        inputDemands[0] - (inputNumPermanent * inputProdPermanent) + ihcDict[0], name='ihcCons1')
                    
                    for i in range(1, num_months - 1):
                        model.addConstraint(ihcDict[i-1] + (inputProdTemporary * ntwDict[i]) ==
                                            inputDemands[i] - (inputNumPermanent * inputProdPermanent) + ihcDict[i], name=f'ihcCons{i+1}')
                    
                    model.addConstraint(ihcDict[num_months - 2] + (inputProdTemporary * ntwDict[num_months - 1]) ==
                                        inputDemands[num_months - 1] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name=f'ihcCons{num_months}')
                
                model.addConstraint(ntwDict[0] == hcDict[0] - fcDict[0], name='ntwCons1')
                
                if num_months > 1:
                    for i in range(1, num_months):
                        model.addConstraint(ntwDict[i] == ntwDict[i-1] + (hcDict[i] - fcDict[i]), name=f'ntwCons{i+1}')
                
                model.solve(pulp.PULP_CBC_CMD(timeLimit=5))  # Solve the linear programming problem with a time limit
                
                if model.status == 1:  # Check if the optimal solution is found
                    if value(model.objective) != original_cost:  # If the optimal cost changes
                        adDemand = step_size * iteration  # Store the allowable decrease in demand
                        break
                
                iteration += 1  # Increment the iteration counter

            inputDemands[i-1] = original_demand  # Reset the demand to its original value
            
            aiDemands.append(aiDemand)  # Append the allowable increase in demand to the list
            adDemands.append(adDemand)  # Append the allowable decrease in demand to the list
            increasedDemands.append(inputDemands[i-1] + aiDemand)  # Append the increased demand to the list
            decreasedDemands.append(inputDemands[i-1] - adDemand)  # Append the decreased demand to the list
        
    # Render the sensitivity analysis results in the template
    return render(request, "main/sensitivity.html", {
        'detail': detail, 
        'aiDemands': aiDemands, 
        'adDemands': adDemands,
        'increasedDemands': increasedDemands, 
        'decreasedDemands': decreasedDemands
    })

def optimize_plan(plan_ID, num_months):  # Function definition with parameters: plan_ID and num_months
    detail = ProductionPlan.objects.filter(id=plan_ID).values()  # Query the ProductionPlan table for the specified plan_ID and get the values
    
    for x in detail:  # Iterate over the details of the production plan
        # Extract relevant values from the production plan details
        inputDemands = [int(x[f'demand{i+1}']) for i in range(num_months)]  # List of demands for each month
        inputNumPermanent = int(x['numPermanent'])  # Number of permanent workers
        inputProdPermanent = int(x['prodPermanent'])  # Production rate of permanent workers
        inputProdTemporary = int(x['prodTemporary'])  # Production rate of temporary workers
        inputCostHiring = float(x['costHiring'])  # Cost of hiring
        inputCostFiring = float(x['costFiring'])  # Cost of firing
        inputCostHoldingUnit = float(x['costHoldingUnit'])  # Holding cost per unit
        inputInventoryInitial = int(x['inventoryInitial'])  # Initial inventory
        inputInventoryFinal = int(x['inventoryFinal'])  # Final inventory

    month = list(range(num_months))  # List of months
    monthIHC = list(range(num_months - 1))  # List of months for inventory holding cost
    
    model = LpProblem("Minimize Cost", LpMinimize)  # Define the linear programming problem to minimize cost
    
    # Define decision variables
    ihcDict = LpVariable.dicts('IHC', monthIHC, lowBound=0, cat='Integer')  # Inventory holding cost variables
    hcDict = LpVariable.dicts('HC', month, lowBound=0, cat='Integer')  # Hiring cost variables
    fcDict = LpVariable.dicts('FC', month, lowBound=0, cat='Integer')  # Firing cost variables
    ntwDict = LpVariable.dicts('NTW', month, lowBound=0, cat='Integer')  # Number of temporary workers variables
    
    # Objective function: minimize the sum of holding, hiring, and firing costs
    model += (lpSum([inputCostHoldingUnit * ihcDict[i] for i in monthIHC]) + 
              lpSum([inputCostHiring * hcDict[i] for i in month]) + 
              lpSum([inputCostFiring * fcDict[i] for i in month]))
    
    if num_months == 1:  # Add constraints to the model for a single month
        model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) == 
                            inputDemands[0] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name='ihcCons1')
    else:  # Add constraints to the model for multiple months
        model.addConstraint(inputInventoryInitial + (inputProdTemporary * ntwDict[0]) == 
                            inputDemands[0] - (inputNumPermanent * inputProdPermanent) + ihcDict[0], name='ihcCons1')
    
        for i in range(1, num_months - 1):  # Add constraints for intermediate months
            model.addConstraint(ihcDict[i-1] + (inputProdTemporary * ntwDict[i]) == 
                                inputDemands[i] - (inputNumPermanent * inputProdPermanent) + ihcDict[i], name=f'ihcCons{i+1}')
        
        model.addConstraint(ihcDict[num_months - 2] + (inputProdTemporary * ntwDict[num_months - 1]) == 
                            inputDemands[num_months - 1] - (inputNumPermanent * inputProdPermanent) + inputInventoryFinal, name=f'ihcCons{num_months}')
    
    model.addConstraint(ntwDict[0] == hcDict[0] - fcDict[0], name='ntwCons1')  # Constraint for the first month's net temporary workers
    
    if num_months > 1:  # Add constraints for the net temporary workers in subsequent months
        for i in range(1, num_months):
            model.addConstraint(ntwDict[i] == ntwDict[i-1] + (hcDict[i] - fcDict[i]), name=f'ntwCons{i+1}')
    
    model.solve(pulp.PULP_CBC_CMD(timeLimit=5))  # Solve the linear programming problem with a time limit
    optimizationStatus = model.status  # Store the optimization status
    
    # Create a dictionary to update the ProductionPlan with the optimization results
    update_dict = {f'inventoryMonth{i+1}': ihcDict[i].varValue for i in range(num_months - 1)}
    update_dict.update({f'hiredTemporary{i+1}': hcDict[i].varValue for i in range(num_months)})
    update_dict.update({f'firedTemporary{i+1}': fcDict[i].varValue for i in range(num_months)})
    update_dict.update({f'numberTemporary{i+1}': ntwDict[i].varValue for i in range(num_months)})
    update_dict['optimalCost'] = value(model.objective)  # Add the optimal cost to the update dictionary
    
    ProductionPlan.objects.filter(id=plan_ID).update(**update_dict)  # Update the ProductionPlan with the optimization results
    
    return optimizationStatus  # Return the optimization status

# Define worksheet header row style.
style_head_row = xlwt.easyxf("""    
        align:  
        wrap off,  
        vert center,  
        horiz center;  
        borders:  
        left THIN,  
        right THIN,  
        top THIN,  
        bottom THIN;  
        font:  
        name Arial,  
        colour_index white,  
        bold on,  
        height 0xA0;  
        pattern:  
        pattern solid,  
        fore-colour 0x19;  
        """
    )

# Define worksheet data row style.
style_data_row = xlwt.easyxf("""
        align:  
        wrap on,  
        vert center,  
        horiz left;  
        font:  
        name Arial,  
        bold off,  
        height 0XA0;  
        borders:  
        left THIN,  
        right THIN,  
        top THIN,  
        bottom THIN;  
        """
    )

# Define worksheet data row style for cost columns.
style_data_row_cost = xlwt.easyxf("""
        align:  
        wrap on,  
        vert center,  
        horiz right;  
        font:  
        name Arial,  
        bold off,  
        height 0XA0;  
        borders:  
        left THIN,  
        right THIN,  
        top THIN,  
        bottom THIN;  
        """
    )

# Define worksheet footer row style.
style_footer_row = xlwt.easyxf("""
        align:  
        wrap on,  
        vert center,  
        horiz center;  
        font:  
        name Arial,  
        bold on,  
        height 0XA0;  
        borders:  
        left THIN,  
        right THIN,  
        top THIN,  
        bottom THIN;  
        """
    )

# Define worksheet footer row style for cost columns.
style_footer_row_cost = xlwt.easyxf("""
        align:  
        wrap on,  
        vert center,  
        horiz right;  
        font:  
        name Arial,  
        bold on,  
        height 0XA0;  
        borders:  
        left THIN,  
        right THIN,  
        top THIN,  
        bottom THIN;  
        """
    )

# Define a green color style.
style_green = xlwt.easyxf(" pattern: fore-colour 0x11, pattern solid;")  # Solid green background color

# Define a red color style.
style_red = xlwt.easyxf(" pattern: fore-colour 0x0A, pattern solid;")  # Solid red background color

@login_required(login_url='/login/')  # Ensure the user is logged in before accessing the view.
def generate_report(request, plan_ID):
    response = HttpResponse(content_type='application/vnd.ms-excel')  # Set response content type to Excel file.
    response['Content-Disposition'] = 'attachment;filename=viewOptimized.xls'  # Set the content-disposition to attachment for file download.
    work_book = xlwt.Workbook(encoding='utf-8')  # Create a new Excel workbook.
    work_sheet = work_book.add_sheet(u'plan details')  # Add a new sheet to the workbook named 'plan details'.
    detail = ProductionPlan.objects.filter(id=plan_ID).values()  # Retrieve production plan details for the given plan_ID.
    for x in detail:
        total_hiring_cost = 0  # Initialize total hiring cost.
        total_firing_cost = 0  # Initialize total firing cost.
        total_holding_cost = 0  # Initialize total holding cost.

        demands = []  # List to store demands.
        hiring_costs = []  # List to store hiring costs.
        firing_costs = []  # List to store firing costs.
        holding_costs = []  # List to store holding costs.

        worker_numbers = [0]  # List to store worker numbers, starting with 0.
        months = ['Start']  # List to store months, starting with 'Start'.
        for month in range(1, 13):
            demand = x[f'demand{month}'] - (x['numPermanent'] * x['prodPermanent'])  # Calculate monthly demand.
            if month == 1:
                demand -= x['inventoryInitial']  # Adjust demand for the initial month with initial inventory.
            if demand < 0:
                demand = 0  # Ensure demand is not negative.
            demands.append(demand)
            
            hC = x[f'hiredTemporary{month}'] * x['costHiring']  # Calculate hiring cost for the month.
            fC = x[f'firedTemporary{month}'] * x['costFiring']  # Calculate firing cost for the month.
            if month == 12:
                ihc = x['costHoldingUnit'] * x['inventoryFinal']  # Calculate holding cost for the final month.
            else:
                ihc = x['costHoldingUnit'] * x[f'inventoryMonth{month}']  # Calculate holding cost for the month.
            
            hiring_costs.append(hC)
            firing_costs.append(fC)
            holding_costs.append(ihc)

            total_hiring_cost += hC  # Accumulate total hiring cost.
            total_firing_cost += fC  # Accumulate total firing cost.
            total_holding_cost += ihc  # Accumulate total holding cost.
            
            worker_numbers.append(x[f'numberTemporary{month}'])  # Append number of temporary workers for the month.
            months.append(f'Month {month}')  # Append the month to the months list.

    work_sheet.write(0, 0, 'MONTH', style_head_row)  # Write the header 'MONTH' in the first cell.
    work_sheet.write(0, 1, 'DEMAND', style_head_row)  # Write the header 'DEMAND' in the second cell.
    work_sheet.write(0, 2, 'REMAINING DEMAND', style_head_row)  # Write the header 'REMAINING DEMAND' in the third cell.
    work_sheet.write(0, 3, 'ENDING INVENTORY UNITS', style_head_row)  # Write the header 'ENDING INVENTORY UNITS' in the fourth cell.
    work_sheet.write(0, 4, 'NUMBER OF TEMPORARY WORKER HIRED', style_head_row)  # Write the header 'NUMBER OF TEMPORARY WORKER HIRED' in the fifth cell.
    work_sheet.write(0, 5, 'NUMBER OF TEMPORARY WORKER FIRED', style_head_row)  # Write the header 'NUMBER OF TEMPORARY WORKER FIRED' in the sixth cell.
    work_sheet.write(0, 6, 'NET NUMBER OF TEMPORARY WORKERS', style_head_row)  # Write the header 'NET NUMBER OF TEMPORARY WORKERS' in the seventh cell.
    work_sheet.write(0, 7, 'HIRING COST', style_head_row)  # Write the header 'HIRING COST' in the eighth cell.
    work_sheet.write(0, 8, 'FIRING COST', style_head_row)  # Write the header 'FIRING COST' in the ninth cell.
    work_sheet.write(0, 9, 'INVENTORY HOLDING COST', style_head_row)  # Write the header 'INVENTORY HOLDING COST' in the tenth cell.

    work_sheet.write(1, 0, '1', style_data_row)  # Write month '1' in the first row.
    work_sheet.write(1, 1, x['demand1'], style_data_row)  # Write demand for month 1.
    work_sheet.write(1, 2, demands[0], style_data_row)  # Write remaining demand for month 1.
    work_sheet.write(1, 3, x['inventoryMonth1'], style_data_row)  # Write inventory for month 1.
    work_sheet.write(1, 4, x['hiredTemporary1'], style_data_row)  # Write number of temporary workers hired in month 1.
    work_sheet.write(1, 5, x['firedTemporary1'], style_data_row)  # Write number of temporary workers fired in month 1.
    work_sheet.write(1, 6, x['numberTemporary1'], style_data_row)  # Write net number of temporary workers in month 1.
    work_sheet.write(1, 7, hiring_costs[0], style_data_row_cost)  # Write hiring cost for month 1.
    work_sheet.write(1, 8, firing_costs[0], style_data_row_cost)  # Write firing cost for month 1.
    work_sheet.write(1, 9, holding_costs[0], style_data_row_cost)  # Write holding cost for month 1.

    work_sheet.write(2, 0, '2', style_data_row)  # Write month '2' in the second row.
    work_sheet.write(2, 1, x['demand2'], style_data_row)  # Write demand for month 2.
    work_sheet.write(2, 2, demands[1], style_data_row)  # Write remaining demand for month 2.
    work_sheet.write(2, 3, x['inventoryMonth2'], style_data_row)  # Write inventory for month 2.
    work_sheet.write(2, 4, x['hiredTemporary2'], style_data_row)  # Write number of temporary workers hired in month 2.
    work_sheet.write(2, 5, x['firedTemporary2'], style_data_row)  # Write number of temporary workers fired in month 2.
    work_sheet.write(2, 6, x['numberTemporary2'], style_data_row)  # Write net number of temporary workers in month 2.
    work_sheet.write(2, 7, hiring_costs[1], style_data_row_cost)  # Write hiring cost for month 2.
    work_sheet.write(2, 8, firing_costs[1], style_data_row_cost)  # Write firing cost for month 2.
    work_sheet.write(2, 9, holding_costs[1], style_data_row_cost)  # Write holding cost for month 2.

    work_sheet.write(3, 0, '3', style_data_row)  # Write month '3' in the third row.
    work_sheet.write(3, 1, x['demand3'], style_data_row)  # Write demand for month 3.
    work_sheet.write(3, 2, demands[2], style_data_row)  # Write remaining demand for month 3.
    work_sheet.write(3, 3, x['inventoryMonth3'], style_data_row)  # Write inventory for month 3.
    work_sheet.write(3, 4, x['hiredTemporary3'], style_data_row)  # Write number of temporary workers hired in month 3.
    work_sheet.write(3, 5, x['firedTemporary3'], style_data_row)  # Write number of temporary workers fired in month 3.
    work_sheet.write(3, 6, x['numberTemporary3'], style_data_row)  # Write net number of temporary workers in month 3.
    work_sheet.write(3, 7, hiring_costs[2], style_data_row_cost)  # Write hiring cost for month 3.
    work_sheet.write(3, 8, firing_costs[2], style_data_row_cost)  # Write firing cost for month 3.
    work_sheet.write(3, 9, holding_costs[2], style_data_row_cost)  # Write holding cost for month 3.

    work_sheet.write(4, 0, '4', style_data_row)  # Write month '4' in the fourth row.
    work_sheet.write(4, 1, x['demand4'], style_data_row)  # Write demand for month 4.
    work_sheet.write(4, 2, demands[3], style_data_row)  # Write remaining demand for month 4.
    work_sheet.write(4, 3, x['inventoryMonth4'], style_data_row)  # Write inventory for month 4.
    work_sheet.write(4, 4, x['hiredTemporary4'], style_data_row)  # Write number of temporary workers hired in month 4.
    work_sheet.write(4, 5, x['firedTemporary4'], style_data_row)  # Write number of temporary workers fired in month 4.
    work_sheet.write(4, 6, x['numberTemporary4'], style_data_row)  # Write net number of temporary workers in month 4.
    work_sheet.write(4, 7, hiring_costs[3], style_data_row_cost)  # Write hiring cost for month 4.
    work_sheet.write(4, 8, firing_costs[3], style_data_row_cost)  # Write firing cost for month 4.
    work_sheet.write(4, 9, holding_costs[3], style_data_row_cost)  # Write holding cost for month 4.

    work_sheet.write(5, 0, '5', style_data_row)  # Write month '5' in the fifth row.
    work_sheet.write(5, 1, x['demand5'], style_data_row)  # Write demand for month 5.
    work_sheet.write(5, 2, demands[4], style_data_row)  # Write remaining demand for month 5.
    work_sheet.write(5, 3, x['inventoryMonth5'], style_data_row)  # Write inventory for month 5.
    work_sheet.write(5, 4, x['hiredTemporary5'], style_data_row)  # Write number of temporary workers hired in month 5.
    work_sheet.write(5, 5, x['firedTemporary5'], style_data_row)  # Write number of temporary workers fired in month 5.
    work_sheet.write(5, 6, x['numberTemporary5'], style_data_row)  # Write net number of temporary workers in month 5.
    work_sheet.write(5, 7, hiring_costs[4], style_data_row_cost)  # Write hiring cost for month 5.
    work_sheet.write(5, 8, firing_costs[4], style_data_row_cost)  # Write firing cost for month 5.
    work_sheet.write(5, 9, holding_costs[4], style_data_row_cost)  # Write holding cost for month 5.

    work_sheet.write(6, 0, '6', style_data_row)  # Write month '6' in the sixth row.
    work_sheet.write(6, 1, x['demand6'], style_data_row)  # Write demand for month 6.
    work_sheet.write(6, 2, demands[5], style_data_row)  # Write remaining demand for month 6.
    work_sheet.write(6, 3, x['inventoryMonth6'], style_data_row)  # Write inventory for month 6.
    work_sheet.write(6, 4, x['hiredTemporary6'], style_data_row)  # Write number of temporary workers hired in month 6.
    work_sheet.write(6, 5, x['firedTemporary6'], style_data_row)  # Write number of temporary workers fired in month 6.
    work_sheet.write(6, 6, x['numberTemporary6'], style_data_row)  # Write net number of temporary workers in month 6.
    work_sheet.write(6, 7, hiring_costs[5], style_data_row_cost)  # Write hiring cost for month 6.
    work_sheet.write(6, 8, firing_costs[5], style_data_row_cost)  # Write firing cost for month 6.
    work_sheet.write(6, 9, holding_costs[5], style_data_row_cost)  # Write holding cost for month 6.

    work_sheet.write(7, 0, '7', style_data_row)  # Write month '7' in the seventh row.
    work_sheet.write(7, 1, x['demand7'], style_data_row)  # Write demand for month 7.
    work_sheet.write(7, 2, demands[6], style_data_row)  # Write remaining demand for month 7.
    work_sheet.write(7, 3, x['inventoryMonth7'], style_data_row)  # Write inventory for month 7.
    work_sheet.write(7, 4, x['hiredTemporary7'], style_data_row)  # Write number of temporary workers hired in month 7.
    work_sheet.write(7, 5, x['firedTemporary7'], style_data_row)  # Write number of temporary workers fired in month 7.
    work_sheet.write(7, 6, x['numberTemporary7'], style_data_row)  # Write net number of temporary workers in month 7.
    work_sheet.write(7, 7, hiring_costs[6], style_data_row_cost)  # Write hiring cost for month 7.
    work_sheet.write(7, 8, firing_costs[6], style_data_row_cost)  # Write firing cost for month 7.
    work_sheet.write(7, 9, holding_costs[6], style_data_row_cost)  # Write holding cost for month 7.

    work_sheet.write(8, 0, '8', style_data_row)  # Write month '8' in the eighth row.
    work_sheet.write(8, 1, x['demand8'], style_data_row)  # Write demand for month 8.
    work_sheet.write(8, 2, demands[7], style_data_row)  # Write remaining demand for month 8.
    work_sheet.write(8, 3, x['inventoryMonth8'], style_data_row)  # Write inventory for month 8.
    work_sheet.write(8, 4, x['hiredTemporary8'], style_data_row)  # Write number of temporary workers hired in month 8.
    work_sheet.write(8, 5, x['firedTemporary8'], style_data_row)  # Write number of temporary workers fired in month 8.
    work_sheet.write(8, 6, x['numberTemporary8'], style_data_row)  # Write net number of temporary workers in month 8.
    work_sheet.write(8, 7, hiring_costs[7], style_data_row_cost)  # Write hiring cost for month 8.
    work_sheet.write(8, 8, firing_costs[7], style_data_row_cost)  # Write firing cost for month 8.
    work_sheet.write(8, 9, holding_costs[7], style_data_row_cost)  # Write holding cost for month 8.

    work_sheet.write(9, 0, '9', style_data_row)  # Write month '9' in the ninth row.
    work_sheet.write(9, 1, x['demand9'], style_data_row)  # Write demand for month 9.
    work_sheet.write(9, 2, demands[8], style_data_row)  # Write remaining demand for month 9.
    work_sheet.write(9, 3, x['inventoryMonth9'], style_data_row)  # Write inventory for month 9.
    work_sheet.write(9, 4, x['hiredTemporary9'], style_data_row)  # Write number of temporary workers hired in month 9.
    work_sheet.write(9, 5, x['firedTemporary9'], style_data_row)  # Write number of temporary workers fired in month 9.
    work_sheet.write(9, 6, x['numberTemporary9'], style_data_row)  # Write net number of temporary workers in month 9.
    work_sheet.write(9, 7, hiring_costs[8], style_data_row_cost)  # Write hiring cost for month 9.
    work_sheet.write(9, 8, firing_costs[8], style_data_row_cost)  # Write firing cost for month 9.
    work_sheet.write(9, 9, holding_costs[8], style_data_row_cost)  # Write holding cost for month 9.

    work_sheet.write(10, 0, '10', style_data_row)  # Write month '10' in the tenth row.
    work_sheet.write(10, 1, x['demand10'], style_data_row)  # Write demand for month 10.
    work_sheet.write(10, 2, demands[9], style_data_row)  # Write remaining demand for month 10.
    work_sheet.write(10, 3, x['inventoryMonth10'], style_data_row)  # Write inventory for month 10.
    work_sheet.write(10, 4, x['hiredTemporary10'], style_data_row)  # Write number of temporary workers hired in month 10.
    work_sheet.write(10, 5, x['firedTemporary10'], style_data_row)  # Write number of temporary workers fired in month 10.
    work_sheet.write(10, 6, x['numberTemporary10'], style_data_row)  # Write net number of temporary workers in month 10.
    work_sheet.write(10, 7, hiring_costs[9], style_data_row_cost)  # Write hiring cost for month 10.
    work_sheet.write(10, 8, firing_costs[9], style_data_row_cost)  # Write firing cost for month 10.
    work_sheet.write(10, 9, holding_costs[9], style_data_row_cost)  # Write holding cost for month 10.

    work_sheet.write(11, 0, '11', style_data_row)  # Write month '11' in the eleventh row.
    work_sheet.write(11, 1, x['demand11'], style_data_row)  # Write demand for month 11.
    work_sheet.write(11, 2, demands[10], style_data_row)  # Write remaining demand for month 11.
    work_sheet.write(11, 3, x['inventoryMonth11'], style_data_row)  # Write inventory for month 11.
    work_sheet.write(11, 4, x['hiredTemporary11'], style_data_row)  # Write number of temporary workers hired in month 11.
    work_sheet.write(11, 5, x['firedTemporary11'], style_data_row)  # Write number of temporary workers fired in month 11.
    work_sheet.write(11, 6, x['numberTemporary11'], style_data_row)  # Write net number of temporary workers in month 11.
    work_sheet.write(11, 7, hiring_costs[10], style_data_row_cost)  # Write hiring cost for month 11.
    work_sheet.write(11, 8, firing_costs[10], style_data_row_cost)  # Write firing cost for month 11.
    work_sheet.write(11, 9, holding_costs[10], style_data_row_cost)  # Write holding cost for month 11.

    work_sheet.write(12, 0, '12', style_data_row)  # Write month '12' in the twelfth row.
    work_sheet.write(12, 1, x['demand12'], style_data_row)  # Write demand for month 12.
    work_sheet.write(12, 2, demands[11], style_data_row)  # Write remaining demand for month 12.
    work_sheet.write(12, 3, x['inventoryFinal'], style_data_row)  # Write final inventory.
    work_sheet.write(12, 4, x['hiredTemporary12'], style_data_row)  # Write number of temporary workers hired in month 12.
    work_sheet.write(12, 5, x['firedTemporary12'], style_data_row)  # Write number of temporary workers fired in month 12.
    work_sheet.write(12, 6, x['numberTemporary12'], style_data_row)  # Write net number of temporary workers in month 12.
    work_sheet.write(12, 7, hiring_costs[11], style_data_row_cost)  # Write hiring cost for month 12.
    work_sheet.write(12, 8, firing_costs[11], style_data_row_cost)  # Write firing cost for month 12.
    work_sheet.write(12, 9, holding_costs[11], style_data_row_cost)  # Write holding cost for month 12.

    # Write the total individual costs in the row 13.
    work_sheet.write_merge(13, 13, 0, 6, 'TOTAL INDIVIDUAL COSTS', style_footer_row)  # Merge cells for total costs label.
    work_sheet.write(13, 7, total_hiring_cost, style_footer_row_cost)  # Write total hiring cost.
    work_sheet.write(13, 8, total_firing_cost, style_footer_row_cost)  # Write total firing cost.
    work_sheet.write(13, 9, total_holding_cost, style_footer_row_cost)  # Write total holding cost.

    # Write the optimized final cost for multi-period planning in the row 14.
    work_sheet.write_merge(14, 14, 0, 6, "OPTIMIZED FINAL COST FOR MULTI-PERIOD PLANNING", style_footer_row)  # Merge cells for final cost label.
    work_sheet.write_merge(14, 14, 7, 9, x['optimalCost'], style_footer_row)  # Merge cells for final cost value.

    output = BytesIO()  # Create a BytesIO object to hold the Excel file in memory.
    work_book.save(output)  # Save the workbook to the BytesIO object.
    output.seek(0)  # Seek to the beginning of the BytesIO object.
    response.write(output.getvalue())  # Write the content of the BytesIO object to the HTTP response.

    return response  # Return the HTTP response.

# Require login to access this view, redirect to login page if not authenticated
@login_required(login_url='/login/')
def create_user(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the first name from the POST data
        first_name = request.POST.get("first_name")
        # Retrieve the last name from the POST data
        last_name = request.POST.get("last_name")
        # Retrieve the username from the POST data
        username = request.POST.get("username")
        # Retrieve the email from the POST data
        email = request.POST.get("email")
        # Retrieve the password from the POST data
        password = request.POST.get("password")
        # Create a new user instance but do not save it yet
        user = User(
            first_name=first_name, 
            last_name=last_name, 
            username=username, 
            email=email
        )
        # Set the password (this will handle hashing)
        user.set_password(password)
        # Save the user to the database
        user.save()
        # Redirect to the read-user view after successful creation
        return redirect("read-user")
    # If request method is not POST, render the create user form
    return render(request, "main/users/create.html")

# Define a view for user registration, accessible without login
def register(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the first name from the POST data
        first_name = request.POST.get("first_name")
        # Retrieve the last name from the POST data
        last_name = request.POST.get("last_name")
        # Retrieve the username from the POST data
        username = request.POST.get("username")
        # Retrieve the email from the POST data
        email = request.POST.get("email")
        # Retrieve the password from the POST data
        password = request.POST.get("password")
        # Create a new user instance but do not save it yet
        user = User(
            first_name=first_name, 
            last_name=last_name, 
            username=username, 
            email=email
        )
        # Set the password (this will handle hashing)
        user.set_password(password)
        # Save the user to the database
        user.save()
        # Redirect to the login view after successful registration
        return redirect("login")
    # If request method is not POST, render the registration form
    return render(request, "main/register.html")

# Require login to access this view, redirect to login page if not authenticated
@login_required(login_url='/login/')
def read_user(request):
    # Retrieve all user data from the database
    userData = User.objects.all().values
    # Render the read user template with the user data
    return render(request, 'main/users/read.html', {'userData': userData})

# Require login to access this view, redirect to login page if not authenticated
@login_required(login_url='/login/')
def update_user(request, id):
    # Retrieve user data for the given id
    userData = User.objects.get(id=id)
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the first name from the POST data
        first_name = request.POST.get("first_name")
        # Retrieve the last name from the POST data
        last_name = request.POST.get("last_name")
        # Retrieve the username from the POST data
        username = request.POST.get("username")
        # Retrieve the email from the POST data
        email = request.POST.get("email")
        # Retrieve the active status from the POST data
        is_active = request.POST.get("is_active")
        # Retrieve the staff status from the POST data
        is_staff = request.POST.get("is_staff")
        # Retrieve the superuser status from the POST data
        is_superuser = request.POST.get("is_superuser")
        # Update the user data
        userData.first_name = first_name
        userData.last_name = last_name
        userData.username = username
        userData.email = email
        userData.is_active = (is_active == 'on')
        userData.is_staff = (is_staff == 'on')
        userData.is_superuser = (is_superuser == 'on')
        # Save the updated user data to the database
        userData.save()
        # Redirect to the read-user view after successful update
        return redirect("read-user")
    # If request method is not POST, render the update user form
    return render(request, "main/users/update.html", {"userData": userData})

# Require login to access this view, redirect to login page if not authenticated
@login_required(login_url='/login/')
def edit_profile(request, id):
    # Retrieve user data for the given id
    userData = User.objects.get(id=id)
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the first name from the POST data
        first_name = request.POST.get("first_name")
        # Retrieve the last name from the POST data
        last_name = request.POST.get("last_name")
        # Update the user data
        userData.first_name = first_name
        userData.last_name = last_name
        # Save the updated user data to the database
        userData.save()
        # Redirect to the home view after successful update
        return redirect("home")
    # If request method is not POST, render the edit profile form
    return render(request, "main/edit_profile.html", {"userData": userData})

# Require login to access this view, redirect to login page if not authenticated
@login_required(login_url='/login/')
def delete_user(request, id):
    # Retrieve user data for the given id
    userData = User.objects.get(id=id)
    # Delete the user from the database
    userData.delete()
    # Redirect to the read-user view after successful deletion
    return redirect("read-user")