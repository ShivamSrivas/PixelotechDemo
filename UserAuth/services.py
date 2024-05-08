import requests 
import random
import smtplib
from Log.logger import logger_call
from .models import UserProfileDetail, PhoneVerification, EmailVerification, Product
from PixelotechDemo.settings import API_KEY, EMAIL_KEY, EMAIL

class UserAuth:
    def __init__(self, ProcessId):
        self.ProcessId = ProcessId

    def OtpGenerationServices(self, PhoneNumber=None, EmailRecipient=None):
        try:
            if PhoneNumber:
                if UserProfileDetail.objects.filter(PhoneNumber=PhoneNumber).exists():
                    return "Phone number is already in use"
                otp = random.randint(1000, 2222)
                url = f"https://2factor.in/API/V1/{API_KEY}/SMS/{PhoneNumber}/{otp}"
                response = requests.get(url)
                response.raise_for_status()
                logger_call("/Log/UserAuth.log", self.ProcessId, "OTP sent via SMS", "Info")
                phoneVerification = PhoneVerification(PhoneNumber=PhoneNumber, Otp=otp)
                phoneVerification.save()
                return otp
            elif EmailRecipient:
                if UserProfileDetail.objects.filter(Email=EmailRecipient).exists():
                    return "Email is already in use"
                otp = random.randint(1000, 2222)
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL["sender_email"], EMAIL_KEY)
                server.sendmail(EMAIL["sender_email"], EmailRecipient, msg=str(otp))
                server.quit()
                logger_call("/Log/UserAuth.log", self.ProcessId, "OTP sent via email", "Info")
                emailVerification = EmailVerification(Email=EmailRecipient, Otp=otp)
                emailVerification.save()
                return otp
            else:
                raise ValueError("Neither PhoneNumber nor EmailRecipient provided.")
        except Exception as error:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Unexpected error: {error}", "Error")
            return str(error)

    def UserVerificationServices(self, Otp, PhoneNumber=None, Email=None):
        try:
            if PhoneNumber:
                otp_from_db = PhoneVerification.objects.filter(PhoneNumber=PhoneNumber).first()
                if otp_from_db and str(Otp) == str(otp_from_db.Otp):
                    return True
            elif Email:
                otp_from_db = EmailVerification.objects.filter(Email=Email).order_by('-Date', '-Time').first()
                if otp_from_db and str(Otp) == str(otp_from_db.Otp):
                    return True
            return False
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred in UserVerificationServices: {e}", "Error")
            return False

    def UserRegistrationServices(self, Name, Email, PhoneNumber, Password):
        try:
            if UserProfileDetail.objects.filter(PhoneNumber=PhoneNumber).exists():
                return "Phone number is already in use"
            if UserProfileDetail.objects.filter(Email=Email).exists():
                return "Email is already in use"
            user = UserProfileDetail(Name=Name, Email=Email, PhoneNumber=PhoneNumber, Password=Password)
            user.save()
            logger_call("Log/UserAuth.log", self.ProcessId, f"A new user is created with Name: {Name}, Email: {Email}, Phone Number: {PhoneNumber}", "Info")
            return user
        except Exception as error:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Error occurred during user registration: {error}", "Error")
            return str(error)

    def GetAllUserDetailsServices(self):
        try:
            users = UserProfileDetail.objects.all()
            return users
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving all user details: {e}", "Error")
            return []

    def GetUserByIdServices(self, UserId):
        try:
            user = UserProfileDetail.objects.filter(id=UserId).values('Email', 'PhoneNumber', 'Name', 'Rejected', 'Accepted').first()
            return user
        except UserProfileDetail.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"User with ID {UserId} does not exist", "Error")
            return None
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving user details: {e}", "Error")
            return None

    def GetProductByIdServices(self, ProductId):
        try:
            product = Product.objects.get(id=ProductId)
            return product
        except Product.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Product with ID {ProductId} does not exist", "Error")
            return None
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving product details: {e}", "Error")
            return None
        
    def GetAllProductServices(self):
        try:
            users = Product.objects.all()
            return users
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving all user details: {e}", "Error")
            return []
