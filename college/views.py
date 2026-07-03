import razorpay
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Student  # Replace with your actual model name
from .forms import StudentForm  # Replace with your actual form name

# Initialize Razorpay Client (Get these from your Razorpay Dashboard)
razorpay_client = razorpay.Client(auth=("rzp_test_T9B7RaLD9cqR5o", "N5n8j6ebyW5p0gqndBMqqWhA"))


def register(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # 1. Save form data to database, but mark is_paid as False for now
            student = form.save(commit=False)
            student.is_paid = False
            student.save()

            # 2. Create a Razorpay Order (Razorpay calculates in paise, so 100 Rupees = 10000 paise)
            payment_amount = 10000
            order_currency = 'INR'

            razorpay_order = razorpay_client.order.create(dict(
                amount=payment_amount,
                currency=order_currency,
                receipt=f"order_rcptid_{student.id}",
                payment_capture='1'  # Automatically capture the payment
            ))

            # 3. Save the order ID to your database so we can find this student later
            student.razorpay_order_id = razorpay_order['id']
            student.save()

            # 4. Reload the page with the payment variables to trigger the popup
            context = {
                'form': form,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_merchant_key': "rzp_test_T9B7RaLD9cqR5o",
                'razorpay_amount': payment_amount,
                'currency': order_currency,
            }
            return render(request, 'college/register.html', context)
    else:
        form = StudentForm()

    return render(request, 'college/register.html', {'form': form})


@csrf_exempt
def payment_success(request):
    # This view runs after the user successfully completes the payment in the popup
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')

        # Find the student using the order ID and update their payment status
        student = Student.objects.get(razorpay_order_id=order_id)
        student.is_paid = True
        student.razorpay_payment_id = payment_id
        student.save()

        return HttpResponse("Payment Successful! Your registration is complete and saved to the database.")