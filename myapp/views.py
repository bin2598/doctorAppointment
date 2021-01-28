from django.shortcuts import render,redirect
from .models import people,appointment
from .forms import registerForm
import datetime


def register(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        user = request.POST.get('user')
        pasw = request.POST.get('pasw')

        # validation
        p = people.objects.filter(username=user)
        if p.exists():
            context = {'m': 'username already exists'}
            return render(request, 'register.html', context)

        p = people(name=name, email=email, phone=phone, role=role, username=user, password=pasw)
        p.save()
        return render(request, 'login.html')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pasw = request.POST.get('pasw')

        p = people.objects.filter(username=user,password=pasw)
        if p.exists():
            for i in p:
                request.session['user'] = i.id

                if i.role == 'Patient':
                    return redirect(patient)
                else:
                    return redirect(doctor)
        else:
            context = {"m":'Invalid Username or Password'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def patient(request):

    # to remove the expired appointment

    d = datetime.datetime.now().date()
    a = appointment.objects.all()
    for i in a:
        s = i.date - d
        print(s.days)
        if s.days < 0:
            i.is_active = False
            i.save()
        print(i.is_active)
    # -------------------------------------

    s = request.session.get('user')
    user = people.objects.get(id=s)
    doctor = people.objects.filter(role='Doctor')
    a = appointment.objects.filter(patient=user).order_by('date')
    print(a)
    context = {'user': user, 'doctor': doctor, 'a':a}
    return render(request, 'patient.html', context)

def doctor(request):
    # to remove the expired appointment

    d = datetime.datetime.now().date()
    a = appointment.objects.all()
    for i in a:
        s = i.date - d
        if s.days < 0:
            i.is_active = False
            i.save()
    # -------------------------------------


    s = request.session.get('user')
    user = people.objects.get(id=s)
    a = appointment.objects.filter(doctor_name=user.name, is_active=True).order_by('date')
    context = {'user': user, 'appointment': a}
    return render(request, 'doctor.html', context)

def book_appointment(request):
    if request.method == 'POST':
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        s = request.session.get('user')
        p = people.objects.get(id=s)
        a = appointment(patient=p, doctor_name=doctor, date=date, time=time)
        a.save()
        return redirect(patient)

    doctor = people.objects.filter(role__iexact='doctor')
    context = {'doctor':doctor}
    return render(request, 'book_appointment.html', context)

def doctor_appointment(request,i):
    a = appointment.objects.get(id=i)
    context = {'a':a}
    return render(request, 'doctorappoint.html', context)

def logout(request):
    del request.session['user']
    return redirect(login)