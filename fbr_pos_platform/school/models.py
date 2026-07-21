from django.db import models

# Create your models here.
from companies.models import *
from digital_invoicing.models import *
import secrets
import uuid
from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class AcademicSession(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tennant_id=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='academic_sessions')
    name=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class grade(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tennant_id=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='grades')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    sort=models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class section(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    grade_id=models.ForeignKey(grade,on_delete=models.CASCADE,related_name='sections')
    academic_session_id=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,related_name='sections')
    name=models.CharField(max_length=100)
    room_number=models.CharField(max_length=100,blank=True,null=True)
    class_teacher_id=models.ForeignKey("Staff",on_delete=models.SET_NULL,related_name='class_teacher',blank=True,null=True)
    capacity=models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.name
    
class subject(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='subjects')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    code=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name
class ClassSubjectAssignment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    section_id=models.ForeignKey(section,on_delete=models.CASCADE,related_name='class_subject_assignments')
    subject_id=models.ForeignKey(subject,on_delete=models.CASCADE,related_name='class_subject_assignments')
    teacher_id=models.ForeignKey("Staff",on_delete=models.SET_NULL,related_name='class_subject_assignments',blank=True,null=True)

    def __str__(self):
        return f"{self.section_id.name} - {self.subject_id.name}"

class guardian(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='guardians')
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    cnic=models.CharField(max_length=15,blank=True,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Student(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='students')
    fullname=models.CharField(max_length=100)
    email=models.EmailField(blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    cnic=models.CharField(max_length=15,blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    gender=models.CharField(max_length=10,choices=(('male','Male'),('female','Female')),blank=True,null=True)
    registration_number=models.CharField(max_length=20,blank=True,null=True)
    admission_date=models.DateField(blank=True,null=True)
    current_section_id=models.ForeignKey(section,on_delete=models.SET_NULL,related_name='students',blank=True,null=True)
    status=models.CharField(max_length=20,choices=(('active','Active'),('inactive','Inactive')),default='active')
    def __str__(self):
        return self.fullname
    

class StudentGuardianAssignment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='guardian_assignments')
    guardian_id=models.ForeignKey(guardian,on_delete=models.CASCADE,related_name='student_assignments')
    relation=models.CharField(max_length=100,blank=True,null=True)
    is_primary_billing_contact=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_id.fullname} - {self.guardian_id.fullname}"

class Staff (models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='staffs')
    fullname=models.CharField(max_length=100)
    email=models.EmailField(blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    cnic=models.CharField(max_length=15,blank=True,null=True)
    date_of_birth=models.DateField(blank=True,null=True)
    designation=models.CharField(max_length=100,blank=True,null=True)
    date_of_joining=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=20,choices=(('active','Active'),('inactive','Inactive')),default='active')

    def __str__(self):
        return self.fullname
    
class Enrollment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='enrollments')
    section_id=models.ForeignKey(section,on_delete=models.CASCADE,related_name='enrollments')
    enrollment_date=models.DateField(default=timezone.now)
    status=models.CharField(max_length=20,choices=(('ongoing','Ongoing'),('permotted','Permotted'),('repeated','Repeated'),('left','Left')),default='active')
    academic_session_id=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,related_name='enrollments')
    grade_id=models.ForeignKey(grade,on_delete=models.CASCADE,related_name='enrollments')
    student_registration_number=models.CharField(max_length=20,blank=True,null=True)





    def __str__(self):
        return f"{self.student_id.fullname} - {self.section_id.name}"



class Attendance(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendances')
    date=models.DateField(default=timezone.now)
    status=models.CharField(max_length=20,choices=(('present','Present'),('absent','Absent')),default='absent')
    enrollement_id=models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='attendances')
    marked_by=models.ForeignKey(Staff,on_delete=models.SET_NULL,related_name='marked_attendances',blank=True,null=True)


    def __str__(self):
        return f"{self.student_id.fullname} - {self.date}"
    

class FeeHead(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='fee_heads')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    
    is_recurring=models.BooleanField(default=False)
    default_pct_code=models.CharField(max_length=10,blank=True,null=True)
    is_active=models.BooleanField(default=True)




    def __str__(self):
        return self.name

class FeeStructure(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    tennant_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='fee_structures')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    academic_session_id=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,related_name='fee_structures')
    grade_id=models.ForeignKey(grade,on_delete=models.CASCADE,related_name='fee_structures')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class FeeStructureItem(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fee_structure_id=models.ForeignKey(FeeStructure,on_delete=models.CASCADE,related_name='fee_structure_items')
    fee_head_id=models.ForeignKey(FeeHead,on_delete=models.CASCADE,related_name='fee_structure_items')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    due_date=models.DateField(blank=True,null=True)
    is_active=models.BooleanField(default=True)
    frequency=models.CharField(max_length=20,choices=(('once','Once'),('monthly','Monthly'),('quarterly','Quarterly'),('yearly','Yearly')),default='once')

    def __str__(self):
        return f"{self.fee_structure_id.name} - {self.fee_head_id.name}"

class StudentFeeConcession(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='fee_concessions')
    fee_structure_item_id=models.ForeignKey(FeeStructureItem,on_delete=models.CASCADE,related_name='student_fee_concessions')
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    consession_type=models.CharField(max_length=20,choices=(('percentage','Percentage'),('fixed','Fixed')),default='fixed')
    is_active=models.BooleanField(default=True)
    enrollement_id=models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='fee_concessions')
    fee_head_id=models.ForeignKey(FeeHead,on_delete=models.CASCADE,related_name='student_fee_concessions')
    value=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    reason=models.TextField(blank=True,null=True)
    approved_by=models.ForeignKey(Staff,on_delete=models.SET_NULL,related_name='approved_fee_concessions',blank=True,null=True)


    def __str__(self):
        return f"{self.student_id.fullname} - {self.fee_structure_item_id.fee_head_id.name}"


class FeeInvoice(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='fee_invoices')
    fee_structure_id=models.ForeignKey(FeeStructure,on_delete=models.CASCADE,related_name='fee_invoices')
    enrollement_id=models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='fee_invoices')
    invoice_date=models.DateField(default=timezone.now)
    due_date=models.DateField(blank=True,null=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=(('unpaid','Unpaid'),('paid','Paid'),('partial','Partial')),default='unpaid')
    academic_session_id=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,related_name='fee_invoices')
    grade_id=models.ForeignKey(grade,on_delete=models.CASCADE,related_name='fee_invoices')
    guardian_id=models.ForeignKey(guardian,on_delete=models.CASCADE,related_name='fee_invoices',blank=True,null=True)
    total_concession_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_payable_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    invoice_status_fbr=models.CharField(max_length=20,choices=(('draft','Draft'), ('sent_to_fbr','Sent to FBR'), ('failed','Failed')), default='draft')
    core_invoice_id=models.ForeignKey('pos.Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='fee_invoices', help_text='Link to the core POS Sale for FBR submission')
    fbr_invoice_number=models.CharField(max_length=100, blank=True, null=True, help_text='Mirrors what core Invoice already stores, denormalized for fast school-side lookup')
    generated_by=models.CharField(max_length=20, choices=(('auto', 'Auto (batch job)'), ('manual', 'Manual')), default='manual')
    

    def __str__(self):
        return f"{self.student_id.fullname} - {self.invoice_date}"


class FeeInvoiceItem(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fee_invoice_id=models.ForeignKey(FeeInvoice,on_delete=models.CASCADE,related_name='items')
    fee_head_id=models.ForeignKey(FeeHead,on_delete=models.SET_NULL,null=True,blank=True,related_name='invoice_items')
    description=models.CharField(max_length=255,blank=True,null=True,help_text='Denormalized snapshot of fee head name at time of billing')
    quantity=models.DecimalField(max_digits=10,decimal_places=2,default=1.00)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2)
    discount_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax_rate=models.DecimalField(max_digits=5,decimal_places=2,default=0)
    tax_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_amount=models.DecimalField(max_digits=12,decimal_places=2)
    pct_code=models.CharField(max_length=20,blank=True,null=True,help_text='Snapshot of FBR PCT code used')

    def __str__(self):
        return f"{self.fee_invoice_id} - {self.description}"


class FeePayment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    fee_invoice_id=models.ForeignKey(FeeInvoice,on_delete=models.CASCADE,related_name='payments')
    amount_paid=models.DecimalField(max_digits=12,decimal_places=2)
    payment_date=models.DateField(default=timezone.now)
    payment_mode=models.CharField(max_length=20,choices=(('cash','Cash'),('bank','Bank'),('online','Online'),('cheque','Cheque')),default='cash')
    received_by_id=models.ForeignKey(Staff,on_delete=models.SET_NULL,null=True,blank=True,related_name='received_payments')
    reference_no=models.CharField(max_length=100,blank=True,null=True,help_text='e.g. cheque number')

    def __str__(self):
        return f"{self.fee_invoice_id} - {self.amount_paid} - {self.payment_date}"


class ExamType(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='exam_types')
    name=models.CharField(max_length=100,help_text='"Mid Term", "Final Term", "Monthly Test"')

    def __str__(self):
        return self.name


class Exam(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    exam_type_id=models.ForeignKey(ExamType,on_delete=models.CASCADE,related_name='exams')
    academic_session_id=models.ForeignKey(AcademicSession,on_delete=models.CASCADE,related_name='exams')
    grade_id=models.ForeignKey(grade,on_delete=models.CASCADE,related_name='exams')
    name=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()

    def __str__(self):
        return f"{self.name} - {self.grade_id.name}"


class ExamSubjectSchedule(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    exam_id=models.ForeignKey(Exam,on_delete=models.CASCADE,related_name='subject_schedules')
    subject_id=models.ForeignKey(subject,on_delete=models.CASCADE,related_name='exam_schedules')
    exam_date=models.DateField()
    max_marks=models.DecimalField(max_digits=6,decimal_places=2,default=100)
    passing_marks=models.DecimalField(max_digits=6,decimal_places=2,default=33)

    def __str__(self):
        return f"{self.exam_id.name} - {self.subject_id.name}"


class StudentExamResult(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    enrollment_id=models.ForeignKey(Enrollment,on_delete=models.CASCADE,related_name='exam_results')
    exam_subject_schedule_id=models.ForeignKey(ExamSubjectSchedule,on_delete=models.CASCADE,related_name='student_results')
    marks_obtained=models.DecimalField(max_digits=6,decimal_places=2)
    grade_letter=models.CharField(max_length=10,blank=True,null=True)
    remarks=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.enrollment_id.student_id.fullname} - {self.exam_subject_schedule_id.subject_id.name}"