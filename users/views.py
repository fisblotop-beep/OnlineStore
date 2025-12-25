from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings

from checkout.models import Order
from .forms import CreationForm, FeedbackForm
from .models import Feedback


@login_required
def user_orders(request):
    """
    Представление списка заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'users/user_orders.html', context)


@login_required
def profile(request):
    """
    Представление профиля пользователя.
    """
    return render(request, 'users/profile.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('store:home')
    template_name = 'users/signup.html'


def feedback_processing(request):
    """
    Прием и обработка формы обратной связи.
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = Feedback.objects.create(
                feedback_name=form.cleaned_data['feedback_name'],
                feedback_email=form.cleaned_data['feedback_email'],
                feedback_message=form.cleaned_data['feedback_message'],
            )

            # ✉️ Отправка email
            send_mail(
                subject='Новое сообщение с сайта',
                message=(
                    f"Имя: {feedback.feedback_name}\n"
                    f"Email: {feedback.feedback_email}\n\n"
                    f"Сообщение:\n{feedback.feedback_message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return render(request, 'users/feedback_success.html')

    return render(request, 'users/feedback_failed.html')
