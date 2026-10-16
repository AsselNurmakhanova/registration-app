from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import User, Attendance
from .forms import CustomUserCreationForm

@login_required
def mark_attendance(request):
    # Check if the logged-in user is a teacher
    if request.user.role != 'TEACHER':
        return render(request, 'attendance_app/not_authorized.html')
    today = timezone.now().date()
    students = User.objects.filter(role='STUDENT')
    if request.method == 'POST':
        date = request.POST.get('date', today)
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status}
                )
        return redirect('attendance_list')
    context = {
        'students': students,
        'today': today,
    }
    return render(request, 'attendance_app/mark_attendance.html', context)

@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')
    context = {'records': records}
    return render(request, 'attendance_app/attendance_list.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'attendance_app/signup.html', {'form': form})

@login_required
def delete_student(request, student_id):
    if request.user.role != 'TEACHER':
        return redirect('mark_attendance')
    student = get_object_or_404(User, id=student_id, role='STUDENT')
    student.delete()
    
    return redirect('mark_attendance')



@login_required
def add_student(request):
    if request.user.role != 'TEACHER':
        return redirect('mark_attendance')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.role = 'STUDENT' 
            student.save()
            return redirect('mark_attendance')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'attendance_app/add_student.html', {'form': form})