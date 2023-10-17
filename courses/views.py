from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Lesson, Payment, Course
from .serializers import LessonSerializer, PaymentSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from courses.serializers import CourseSerializer
from courses.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

class CourseListView(View):
    """Представление для отображения списка курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request):
        """Обрабатывает GET-запрос для отображения списка курсов."""
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {'courses': courses})


class CourseDetailView(View):
    """Представление для отображения деталей курса."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, pk):
        """Обрабатывает GET-запрос для отображения конкретного курса."""
        course = get_object_or_404(Course, pk=pk)
        return render(request, 'courses/course_detail.html', {'course': course})


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для выполнения операций CRUD над курсами."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


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
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        lesson = self.get_object()
        payments = Payment.objects.filter(lesson=lesson)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

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


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_paid',)


class CustomTokenObtainView(APIView):
    def post(self, request):
        # Получение токена
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token_key),
                'refresh': str(refresh)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YourView(APIView):
    """
    API View для примера.

    Этот пример демонстрирует использование авторизации через JWT.
    В данном случае, доступ к этому эндпоинту разрешен только для авторизованных пользователей.

    Methods:
        get(request): Обработчик HTTP GET запроса.

    Attributes:
        permission_classes (list): Список классов разрешений.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Обработчик HTTP GET запроса.

        Args:
            request (HttpRequest): Объект запроса.

        Returns:
            Response: Объект ответа.

        """
        # Ваш код

        return Response("This is a protected view")
