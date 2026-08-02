from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcademicSessionViewSet, GradeViewSet, SectionViewSet, SubjectViewSet,
    ClassSubjectAssignmentViewSet, GuardianViewSet, StudentViewSet,
    StudentGuardianAssignmentViewSet, StaffViewSet, EnrollmentViewSet,
    AttendanceViewSet, FeeHeadViewSet, FeeStructureViewSet,
    FeeStructureItemViewSet, StudentFeeConcessionViewSet,
    ExamTypeViewSet, ExamViewSet, ExamSubjectScheduleViewSet, StudentExamResultViewSet,
    FeeInvoiceViewSet, FeeInvoiceItemViewSet, FeePaymentViewSet
)

router = DefaultRouter()
router.register(r'academic-sessions', AcademicSessionViewSet, basename='academic-session')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'class-subject-assignments', ClassSubjectAssignmentViewSet, basename='class-subject-assignment')
router.register(r'guardians', GuardianViewSet, basename='guardian')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-guardian-assignments', StudentGuardianAssignmentViewSet, basename='student-guardian-assignment')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'fee-heads', FeeHeadViewSet, basename='fee-head')
router.register(r'fee-structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'fee-structure-items', FeeStructureItemViewSet, basename='fee-structure-item')
router.register(r'student-fee-concessions', StudentFeeConcessionViewSet, basename='student-fee-concession')
router.register(r'exam-types', ExamTypeViewSet, basename='exam-type')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-subject-schedules', ExamSubjectScheduleViewSet, basename='exam-subject-schedule')
router.register(r'student-exam-results', StudentExamResultViewSet, basename='student-exam-result')
router.register(r'fee-invoices', FeeInvoiceViewSet, basename='fee-invoice')
router.register(r'fee-invoice-items', FeeInvoiceItemViewSet, basename='fee-invoice-item')
router.register(r'fee-payments', FeePaymentViewSet, basename='fee-payment')
urlpatterns = [
    path('', include(router.urls)),
]
