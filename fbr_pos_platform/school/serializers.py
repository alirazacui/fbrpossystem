from rest_framework import serializers
from .models import (
    AcademicSession, grade, section, subject, ClassSubjectAssignment,
    guardian, Student, StudentGuardianAssignment, Staff, Enrollment, Attendance,
    FeeHead, FeeStructure, FeeStructureItem, StudentFeeConcession,
    ExamType, Exam, ExamSubjectSchedule, StudentExamResult,
    FeeInvoice, FeeInvoiceItem, FeePayment
)

class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = grade
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = subject
        fields = '__all__'

class ClassSubjectAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubjectAssignment
        fields = '__all__'

class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = guardian
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentGuardianAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGuardianAssignment
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class FeeHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeHead
        fields = '__all__'

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeeStructureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructureItem
        fields = '__all__'

class StudentFeeConcessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeeConcession
        fields = '__all__'

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamSubjectScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubjectSchedule
        fields = '__all__'

class StudentExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExamResult
        fields = '__all__'

class FeeInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeInvoiceItem
        fields = '__all__'
        read_only_fields = ['fee_invoice_id']

class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = '__all__'

class FeeInvoiceSerializer(serializers.ModelSerializer):
    items = FeeInvoiceItemSerializer(many=True, read_only=True)
    payments = FeePaymentSerializer(many=True, read_only=True)

    class Meta:
        model = FeeInvoice
        fields = '__all__'
