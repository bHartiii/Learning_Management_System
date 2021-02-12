from rest_framework import serializers
from .models import Course, Mentor, StudentCourseMentor, Student, Education, Performance
import sys
import re
from .utils import Pattern

sys.path.append('..')
from Auth.models import User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'cid', 'duration_weeks', 'description', 'course_price']
        extra_kwargs = {'id': {'read_only': True}, 'duration_weeks': {'required': True}, 'cid': {'read_only': True}}

    def validate(self, data):
        data['course_name'] = data['course_name'].upper()
        return data


class CourseMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['mentor', 'course']
        extra_kwargs = {'mentor': {'read_only': True}}


class MentorSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = ['id', 'mentor', 'course']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile', 'role']


class StudentCourseMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMentor
        fields = ['student', 'course', 'mentor', 'create_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'create_by': {'read_only': True}}

    def validate(self, data):
        data['create_by'] = self.context['user']
        return data


class StudentCourseMentorReadSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    create_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentCourseMentor
        fields = ['id', 'student_id', 'mentor_id', 'course_id', 'student', 'mentor', 'course', 'create_by',
                  'updated_by']


class StudentCourseMentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMentor
        fields = ['course', 'mentor', 'updated_by']
        extra_kwargs = {'course': {'required': True}, 'mentor': {'required': True}, 'updated_by': {'read_only': True}}

    def validate(self, data):
        data['updated_by'] = self.context['user']
        return data


class StudentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    mentor_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

    class Meta:
        model = StudentCourseMentor
        fields = ['id', 'course_id', 'student_id', 'mentor_id', 'student', 'course', 'mentor']


class StudentBasicSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'student']


class StudentDetailsSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    alt_number = serializers.CharField(max_length=13, min_length=10, required=True)
    relation_with_alt_number_holder = serializers.CharField(read_only=True, max_length=10)
    current_location = serializers.CharField(min_length=3, max_length=30, required=True)
    current_address = serializers.CharField(min_length=5, required=True)
    git_link = serializers.CharField(required=True, min_length=10)
    year_of_experience = serializers.IntegerField(required=True)

    class Meta:
        model = Student
        fields = ['id', 'student', 'alt_number', 'relation_with_alt_number_holder', 'current_location',
                  'current_address', 'git_link', 'year_of_experience']

    def validate(self, data):
        if not re.fullmatch(Pattern.GIT_PATTERN.value, data['git_link']):
            raise serializers.ValidationError('Invalid git link')
        if not re.fullmatch(Pattern.MOBILE_PATTERN.value, data['alt_number']):
            raise serializers.ValidationError('Invalid Mobile number format')
        return data


class EducationSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    institute = serializers.CharField(required=True)
    stream = serializers.CharField(required=True)
    percentage = serializers.FloatField(required=True)
    from_date = serializers.DateField(required=True)
    till = serializers.DateField(required=True)

    class Meta:
        model = Education
        fields = ['id', 'student_id', 'student', 'institute', 'degree', 'stream', 'percentage', 'from_date', 'till']

    def validate(self, data):
        data['student_id'] = self.context['student']  # storing logged in student id and returning with data
        return data


class EducationUpdateSerializer(serializers.ModelSerializer):
    institute = serializers.CharField(required=True)
    stream = serializers.CharField(required=True)
    percentage = serializers.FloatField(required=True)
    from_date = serializers.DateField(required=True)
    till = serializers.DateField(required=True)

    class Meta:
        model = Education
        fields = ['institute', 'stream', 'percentage', 'from_date', 'till']


class CourseMentorSerializerDetails(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StudentCourseMentor
        fields = ['id', 'student_id', 'mentor_id', 'course_id', 'student', 'mentor', 'course']


class NewStudentsSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student', 'course_assigned']


class PerformanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True)
    update_by = serializers.StringRelatedField(read_only=True)
    score = serializers.FloatField(max_value=10, min_value=1)
    review_date = serializers.DateField(required=True)

    class Meta:
        model = Performance
        fields = ['student_id', 'student', 'course_id', 'course', 'mentor_id', 'mentor', 'score', 'week_no', 'remark',
                  'review_date', 'update_by']
        read_only_fields = ('student', 'week_no', 'mentor', 'course', 'update_by')

    def validate(self, data):
        data['update_by'] = self.context['user']
        return data


class ExcelDataSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate(self, data):
        if data['file']._name.split('.')[1] not in ['xlsx']:
            raise serializers.ValidationError('response: Invalid file format. [.xlsx] expected')
        return data


class AddMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['mid', 'mentor', 'course']
        extra_kwargs = {'mid': {'read_only': True}, 'mentor': {'read_only': True}}


class MentorDetailSerializer(serializers.ModelSerializer):
    mentor = AddMentorSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'mobile', 'mentor']

class MentorCourseSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField(read_only=True)
    course = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Mentor
        fields = ['mid', 'mentor', 'course']
        return data


class AddStudentSerializer(serializers.ModelSerializer):
    student = StudentCourseMentorUpdateSerializer(required=False)
    name = serializers.CharField(max_length=50, required=False)
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'student']