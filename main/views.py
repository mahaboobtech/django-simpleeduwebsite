from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Course, Purchase
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('courses')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')

def courses(request):
    if not request.user.is_authenticated:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

# def payment(request, course_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     course = Course.objects.get(id=course_id)
#     return render(request, 'payment.html', {'course': course})



def logout_view(request):
    logout(request)
    return redirect('home')


def payment(request, course_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch course object
    course = get_object_or_404(Course, id=course_id)
    
    # Calculate the amount in paise
    amount = int(course.price * 100)  # Convert price to paise (1 INR = 100 paise)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create an order in Razorpay
    order_receipt = f"order_{course_id}_{request.user.id}"
    
    payment_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'receipt': order_receipt,
        'payment_capture': '1',  # Auto capture payment
    })

    # Pass necessary context to the template
    context = {
        'course': course,
        'razorpay_order_id': payment_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount,  # Pass amount in paise
    }

    return render(request, 'payment.html', context)


@csrf_exempt
def payment_success(request):
    # Get the Razorpay payment details from the request
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')

    if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
        return HttpResponse("Missing payment details", status=400)

    # Fetch the course_id from the request (you need to make sure this is passed correctly)
    course_id = request.GET.get('course_id')
    print(f"Received course_id: {course_id}")  # Log the course_id for debugging

    if not course_id:
        return HttpResponse("Course ID not provided", status=400)
    
    # Fetch the course from the database
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponse(f"Course with id {course_id} does not exist", status=404)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Prepare the Razorpay order data for verification
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    
    try:
        # Verify the payment signature to ensure it's legit
        client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse("Payment verification failed", status=400)

    # If the payment is successfully verified, save the purchase
    if request.user.is_authenticated:
        # Get or create the Purchase record
        purchase, created = Purchase.objects.get_or_create(user=request.user, course=course)
        
        # You can send email confirmation or any additional logic here

    # Render the success page
    return render(request, 'payment_success.html', {'course': course})
