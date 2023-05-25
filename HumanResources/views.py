from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest, JsonResponse, HttpResponse
from HumanResources.serializers import EmployeeSerializer, VacationSerializer
from .models import Employee, Vacation
from .form import EmployeeForm
import json


# done.
def index(request: HttpRequest):
    return render(request, 'index.html')


# done.
def home(request: HttpRequest):
    return render(request, 'pages/home.html')


# done.
def searchEmployee(request: HttpRequest):
    return render(request, 'pages/search-employees.html')


# done.
def addEmployee(request: HttpRequest):
    if request.method == 'POST':
        employeeID = request.POST.get('id')
        try:
            Employee.objects.get(id=employeeID)
            return render(request, 'pages/add-employee.html', {'errorMessage': 'Employee ID already exists'})
        except:
            pass
        employeeName = request.POST.get('name')
        employeeEmail = request.POST.get('email')
        employeePhoneNumber = request.POST.get('phoneNumber')
        employeeAddress = request.POST.get('address')
        employeeGender = request.POST.get('gender')
        employeeMaritalStatus = request.POST.get('maritalStatus')
        employeeAvailableVacationDays = request.POST.get('availableVacationDays')
        employeeApprovedVacationDays = request.POST.get('approvedVacationDays')
        employeeBirthDate = request.POST.get('birthDay')
        employeeSalary = request.POST.get('salary')

        Employee.objects.create(
            id=employeeID, name=employeeName, email=employeeEmail,
            phoneNumber=employeePhoneNumber, address=employeeAddress, gender=employeeGender,
            maritalStatus=employeeMaritalStatus, availableVacationDays=employeeAvailableVacationDays,
            approvedVacationDays=employeeApprovedVacationDays, birthDay=employeeBirthDate, salary=employeeSalary
        )
        return redirect('searchEmployee')
    return render(request, 'pages/add-employee.html')


# done.
def initialFormData(employee: Employee, isDesiabled: bool = True) -> EmployeeForm:
    initialData = {
        'id': employee.id,
        'name': employee.name,
        'email': employee.email,
        'address': employee.address,
        'phoneNumber': employee.phoneNumber,
        'gender': employee.gender,
        'maritalStatus': employee.maritalStatus,
        'availableVacationDays': employee.availableVacationDays,
        'approvedVacationDays': employee.approvedVacationDays,
        'salary': employee.salary,
        'birthDay': employee.birthDay
    }
    form = EmployeeForm(initial=initialData)
    return form


# done.
def editEmployee(request: HttpRequest):
    return render(request, 'pages/edit-employee.html', {
        'errorMessage': 'You did not choose any employee to be edited or deleted.'
    })


# done.
def editEmployeeForm(request: HttpRequest, employeeId: int):
    if request.method == 'POST':
        employee = Employee.objects.get(id=employeeId)
        employee.name = request.POST.get('name')
        employee.phoneNumber = request.POST.get('phoneNumber')
        employee.address = request.POST.get('address')
        employee.maritalStatus = request.POST.get('maritalStatus')
        employee.availableVacationDays = request.POST.get('availableVacationDays')
        employee.approvedVacationDays = request.POST.get('approvedVacationDays')
        employee.salary = request.POST.get('salary')
        employee.save()
        return redirect('searchEmployee')

    employee = Employee.objects.get(id=employeeId)
    form = initialFormData(employee)
    return render(request, 'pages/edit-employee.html', {
        'form': form,
        'id': employee.id
    })


# done.
def deleteEmployee(request: HttpRequest, employeeId: int):
    try:
        employee = Employee.objects.get(id=employeeId)
        employee.delete()
    except:
        return render(request, 'pages/edit-employee.html', {
            'errorMessage': 'Employee does not exist to be deleted.',
            'id': employeeId,
            'form': EmployeeForm()
        })
    return redirect('searchEmployee')


# done.
def vacationForm(request: HttpRequest, employeeId):
    return render(request, 'pages/vacation-form.html')


# done.
def vacations(request: HttpRequest):
    return render(request, 'pages/vacations.html')


# done.
@api_view(['GET', 'POST'])
def vacation_list(request):
    if (request.method == 'GET'):
        vacations = Vacation.objects.all()
        serializer = VacationSerializer(vacations, many=True)
        return Response(serializer.data)
    
    elif (request.method == 'POST'):
        employee = Employee.objects.get(id=(request.data['employee-id']))
        vacation_data = json.loads(request.data['vacation'])
        
        vacation = Vacation.objects.create(
            employee=employee,
            startDate=vacation_data['startDate'],
            endDate=vacation_data['endDate'],
            vacationReason=vacation_data['vacationReason'],
            status=vacation_data['status'],
        )
        vacation.save()
        
        serializer = VacationSerializer(instance=vacation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def update_vacation(request, vacationId):
    if (request.method == 'POST'):
        vacation = Vacation.objects.get(pk=vacationId)
        if not vacation:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        vacation.status = request.data['status']
        vacation.save()
        return Response(status=status.HTTP_302_FOUND)
    
    else:
        render(request, 'search-employees.html')


# TODO: to be tested.
def getEmployees(request: HttpRequest):
    return JsonResponse({'employees': list(Employee.objects.all().values())})


# done.
def employee_deatil(request: HttpRequest, employeeId: int):
    employee = Employee.objects.get(id=employeeId)
    serializer = EmployeeSerializer(employee)
    return JsonResponse(serializer.data)
