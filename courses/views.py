import stripe as stripe
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .serializers import LessonSerializer, PaymentSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from courses.serializers import CourseSerializer
from rest_framework.decorators import action
from .models import Lesson, Payment
from courses.models import Course
from .permissions import IsModerator, IsOwnerOrReadOnly
from django.views import View
from django.http import JsonResponse


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для выполнения операций CRUD над курсами."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Разрешения для разных действий
        permission_classes = [IsAuthenticated]
        if self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]
        elif self.action in ["destroy", "retrieve"]:
            if self.action == "create":
                # Модератор не может создать курс или урок
                return [IsAuthenticated(), ~IsModerator()]
            elif self.action in ["update", "partial_update"]:
                # Модератор может редактировать любой курс или урок
                # Обычный пользователь может редактировать только свои курсы и уроки
                return [IsAuthenticated(), IsModerator() | IsOwnerOrReadOnly()]
            elif self.action == "destroy":
                # Модератор может видеть и редактировать, но не удалять урок
                # Обычный пользователь не имеет доступа к удалению
                return [IsAuthenticated(), IsModerator() | IsOwnerOrReadOnly()]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


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


# Test Secret Key
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


class PaymentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Получаем данные из запроса (или передаем их в теле запроса)
        amount = request.data.get('amount')  # сумма платежа в центах
        currency = request.data.get('currency')  # валюта (например, 'usd')

        # Создаем платеж в Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency
        )

        # Возвращаем клиенту данные для оплаты
        return Response({
            'client_secret': payment_intent.client_secret
        }, status=status.HTTP_200_OK)


class PaymentView(View):
    def post(self, request):
        amount = 1000  # Сумма оплаты
        currency = "usd"  # Валюта

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency
            )

            # Создаем новый объект Payment и сохраняем его в базе данных
            payment = Payment.objects.create(
                user=request.user,  # Укажите пользователя, совершившего платеж
                date_paid=payment_intent.created,
                content_type=None,  # Укажите соответствующий content_type
                object_id=None,  # Укажите соответствующий object_id
                amount=amount / 100.0,  # Сумма в долларах
                payment_method="stripe"  # Укажите метод оплаты
            )

            return JsonResponse({"client_secret": payment_intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
