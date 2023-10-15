from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Course, Lesson
from .serializers import LessonSerializer, CourseSerializer


class CourseListView(View):
    """Представление для отображения списка курсов."""

    def get(self, request):
        """Обрабатывает GET-запрос для отображения списка курсов."""
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {'courses': courses})


class CourseDetailView(View):
    """Представление для отображения деталей курса."""

    def get(self, request, pk):
        """Обрабатывает GET-запрос для отображения конкретного курса."""
        course = get_object_or_404(Course, pk=pk)
        return render(request, 'courses/course_detail.html', {'course': course})


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для выполнения операций CRUD над курсами."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """Представление для отображения и создания уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(viewsets.ViewSet):
    """ViewSet для выполнения операций CRUD над уроками."""

    queryset = Lesson.objects.all()

    def list(self, request):
        """Обрабатывает GET-запрос для вывода списка уроков."""
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Обрабатывает POST-запрос для создания урока."""
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Обрабатывает GET-запрос для получения урока."""
        queryset = Lesson.objects.all()
        lesson = get_object_or_404(queryset, pk=pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Обрабатывает PUT-запрос для обновления урока."""
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Обрабатывает DELETE-запрос для удаления урока."""
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
