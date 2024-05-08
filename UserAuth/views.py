from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from UserAuth.models import UserProfileDetail
from random import randint
from UserAuth.services import UserAuth
import json

user_auth = UserAuth(ProcessId=randint(0000, 1111))

@csrf_exempt
def OtpGeneration(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            phone_number = json_data.get('phone_number')
            email_recipient = json_data.get('email_recipient')
            if phone_number or email_recipient:
                otp = user_auth.OtpGenerationServices(phone_number, email_recipient)
                if otp:
                    return JsonResponse({'data': {'otp': otp, 'contactInfo': phone_number if phone_number else email_recipient}, 'message': 'OTP sent successfully', 'status': 200})
                else:
                    return JsonResponse({'message': 'Failed to send OTP', 'status': 500})
            else:
                return JsonResponse({'message': 'Phone or Email is required', 'status': 400})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def UserVerification(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        otp = json_data.get('otp')
        phone_number = json_data.get('phone_number')
        email = json_data.get('email_recipient')
        msg = user_auth.UserVerificationServices(otp, phone_number, email)
        return JsonResponse({'message': msg, 'status': 200})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def UserRegistration(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        name = json_data.get('name')
        email = json_data.get('email')
        phone_number = json_data.get('phone_number')
        password = json_data.get('password')

        if name and email and phone_number and password:
            user = user_auth.UserRegistrationServices(name, email, phone_number, password)
            if isinstance(user, UserProfileDetail):
                return JsonResponse({'message': 'User registered successfully', 'status': 200})
            else:
                return JsonResponse({'message': str(user), 'status': 500})
        else:
            return JsonResponse({'message': 'All fields are required', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def GetAllUser(request):
    if request.method == 'GET':
        users = user_auth.GetAllUserDetailsServices()
        if users:
            return JsonResponse({'data': list(users.values()), 'message': 'Users retrieved successfully', 'status': 200})
        else:
            return JsonResponse({'message': 'No users found', 'status': 404})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def GetUserById(request, user_id):
    if request.method == 'GET':
        try:
            user_id = int(user_id)
            user = user_auth.GetUserByIdServices(user_id)
            if user:
                return JsonResponse({'data': user, 'message': f'User with ID {user_id} retrieved successfully', 'status': 200})
            else:
                return JsonResponse({'message': f'User with ID {user_id} not found', 'status': 404})
        except ValueError:
            return JsonResponse({'message': 'Invalid user ID', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})
    
@csrf_exempt
def GetAllProduct(request):
    if request.method == 'GET':
        products = user_auth.GetAllProductServices()
        if products:
            return JsonResponse({'data': list(products.values()), 'message': 'Products retrieved successfully', 'status': 200})
        else:
            return JsonResponse({'message': 'No products found', 'status': 404})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def GetProductById(request, product_id):
    if request.method == 'GET':
        try:
            product_id = int(product_id)
            product = user_auth.GetProductByIdServices(product_id)
            if product:
                return JsonResponse({'data': product, 'message': f'Product with ID {product_id} retrieved successfully', 'status': 200})
            else:
                return JsonResponse({'message': f'Product with ID {product_id} not found', 'status': 404})
        except ValueError:
            return JsonResponse({'message': 'Invalid product ID', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})