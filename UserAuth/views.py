from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from UserAuth.models import UserProfileDetail,Product
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
                if type(otp) == 'init':
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
        if msg:
            return JsonResponse({'message': "Verified", 'status': 200})
        else:
            return JsonResponse({'message': "Wrong otp please try again", 'status': 200})
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

@csrf_exempt
def AddProduct(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        unique_number = json_data.get('uniqueNumber')
        url = json_data.get('url')
        
        if unique_number and url:
            product = user_auth.AddProductServices(unique_number, url)
            if isinstance(product, Product):
                return JsonResponse({'message': 'Product added successfully', 'status': 200})
            else:
                return JsonResponse({'message': str(product), 'status': 500})
        else:
            return JsonResponse({'message': 'Unique number and URL are required', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def DeleteProductById(request, product_id):
    if request.method == 'DELETE':
        try:
            product_id = int(product_id)
            message = user_auth.DeleteProductByIdServices(product_id)
            return JsonResponse({'message': message, 'status': 200})
        except ValueError:
            return JsonResponse({'message': 'Invalid product ID', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})

@csrf_exempt
def UpdateUser(request, user_id):
    if request.method == 'PUT':
        try:
            user_id = int(user_id)
            json_data = json.loads(request.body.decode('utf-8'))
            rejected = json_data.get('rejected', [])
            accepted = json_data.get('accepted', [])
            
            # Ensure that the IDs in accepted and rejected lists are integers
            rejected = [int(id) for id in rejected]
            accepted = [int(id) for id in accepted]
            
            # Update user profile
            user = UserProfileDetail.objects.get(id=user_id)
            if rejected:
                user.Rejected = rejected
            if accepted:
                user.Accepted = accepted
            user.save()
            
            return JsonResponse({'message': 'User updated successfully', 'status': 200})
        except ValueError:
            return JsonResponse({'message': 'Invalid user ID', 'status': 400})
        except UserProfileDetail.DoesNotExist:
            return JsonResponse({'message': f'User with ID {user_id} does not exist', 'status': 404})
        except Exception as e:
            return JsonResponse({'message': f'An error occurred while updating user: {str(e)}', 'status': 500})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})
    

@csrf_exempt
def DeleteUserById(request, user_id):
    if request.method == 'DELETE':
        try:
            user_id = int(user_id)
            message = user_auth.DeleteUserByIdServices(user_id)
            return JsonResponse({'message': message, 'status': 200})
        except ValueError:
            return JsonResponse({'message': 'Invalid user ID', 'status': 400})
    else:
        return JsonResponse({'message': 'Method not allowed', 'status': 405})