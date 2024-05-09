import requests 
import random
import smtplib
import os
from Log.logger import logger_call
from .models import UserProfileDetail, PhoneVerification, EmailVerification, Product
from PixelotechDemo.settings import EMAIL,API_KEY,EMAIL_KEY
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class UserAuth:
    def __init__(self, ProcessId):
        self.ProcessId = ProcessId

    def OtpGenerationServices(self, PhoneNumber=None, EmailRecipient=None):
        try:
            if PhoneNumber:
                if UserProfileDetail.objects.filter(PhoneNumber=PhoneNumber).exists():
                    return "Phone number is already in use"
                otp = random.randint(1000, 9999)  
                sms_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/{PhoneNumber}/{otp}"

                response = requests.get(sms_url)
                response.raise_for_status()
                logger_call("/Log/UserAuth.log", self.ProcessId, "OTP sent via SMS", "Info")
                phoneVerification = PhoneVerification(PhoneNumber=PhoneNumber, Otp=otp)
                phoneVerification.save()
                return otp
            elif EmailRecipient:
                if UserProfileDetail.objects.filter(Email=EmailRecipient).exists():
                    return "Email is already in use"
                otp = random.randint(1000, 9999)  
                email_settings = EMAIL 

                msg = MIMEMultipart()
                msg['From'] = email_settings["sender_email"]
                msg['To'] = EmailRecipient
                msg['Subject'] = EMAIL["subject"]

            # Attach HTML message
                html_message = MIMEText(EMAIL["message"], 'html')
                msg.attach(html_message)
                
                plain_message = MIMEText(f'Your OTP is: {otp}', 'plain')
                msg.attach(plain_message)

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(email_settings["sender_email"], EMAIL_KEY)
                server.sendmail(email_settings["sender_email"], EmailRecipient, msg.as_string())
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
                otp_from_db = PhoneVerification.objects.filter(PhoneNumber=PhoneNumber).last()
                if otp_from_db and str(Otp) == str(otp_from_db.Otp):
                    return True
            elif Email:
                otp_from_db = EmailVerification.objects.filter(Email=Email).last()
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
            logger_call("/Log/UserAuth.log", self.ProcessId, f"A new user is created with Name: {Name}, Email: {Email}, Phone Number: {PhoneNumber}", "Info")
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

    def GetProductByIdServices(self, unique_number):
        try:
            product = Product.objects.get(UniqueNumber=unique_number)
            product_info = {
            'UniqueNumber': product.UniqueNumber,
            'Url': product.Url
            }
            return product_info
        except Product.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Product with unique number {unique_number} does not exist", "Error")
            return None
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving product details: {e}", "Error")
            return None
        
    def GetAllProductServices(self):
        try:
            products = Product.objects.all()
            return products
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while retrieving all products: {e}", "Error")
            return []

    def AddProductServices(self, unique_number, url):
        try:
            product = Product.objects.create(UniqueNumber=unique_number, Url=url)
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Product added with Unique Number: {unique_number}, URL: {url}", "Info")
            return product
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while adding product: {e}", "Error")
            return str(e)

    def DeleteProductByIdServices(self, ProductId):
        try:
            product = Product.objects.get(UniqueNumber=ProductId)
            product.delete()
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Product with ID {ProductId} deleted successfully", "Info")
            return "Product deleted successfully"
        except Product.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"Product with ID {ProductId} does not exist", "Error")
            return f"Product with ID {ProductId} does not exist"
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while deleting product: {e}", "Error")
            return str(e)

    def UpdateUserServices(self, UserId, rejected=None, accepted=None):
        try:
            user = UserProfileDetail.objects.get(id=UserId)
            if rejected is not None:
                user.Rejected = rejected
            if accepted is not None:
                user.Accepted = accepted
            user.save()
            logger_call("/Log/UserAuth.log", self.ProcessId, f"User with ID {UserId} updated successfully", "Info")
            return "User updated successfully"
        except UserProfileDetail.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"User with ID {UserId} does not exist", "Error")
            return f"User with ID {UserId} does not exist"
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while updating user: {e}", "Error")
            return str(e)

    def DeleteUserByIdServices(self, UserId):
        try:
            user = UserProfileDetail.objects.get(id=UserId)
            user.delete()
            logger_call("/Log/UserAuth.log", self.ProcessId, f"User with ID {UserId} deleted successfully", "Info")
            return "User deleted successfully"
        except UserProfileDetail.DoesNotExist:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"User with ID {UserId} does not exist", "Error")
            return f"User with ID {UserId} does not exist"
        except Exception as e:
            logger_call("/Log/UserAuth.log", self.ProcessId, f"An error occurred while deleting user: {e}", "Error")
            return str(e)
