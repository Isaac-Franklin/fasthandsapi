from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoginSerializer, RegisterSerializer
from userregapp.models import UserRegisterModel
from userregapp.checkuserinfo import CheckUserData
from django.shortcuts import redirect


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



#   implement my customization of token claim when displaying user data I create a custome view for it as below:
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
# 


@api_view(['GET'])
def  Welcome_Page(request):
    # AllUser = UserRegisterModel.objects.all()
    # serializer = RegisterSerializer(AllUser, many=True)
    # return Response(serializer.data)
    return Response({
        'Welcome': 'Welcome to the FastHands API, Use the follwing routes below to navigate and view available resources.',
        'See all artisans': 'https://franklin007.pythonanywhere.com/allartisans/',
        'Register an artisan': 'https://franklin007.pythonanywhere.com/register/',
        'Find (or update) a specific artisan by email': 'https://franklin007.pythonanywhere.com/artisan/emailaddress/',
        'Find a specific artisan location': 'https://franklin007.pythonanywhere.com/searchlocation/enterlocation/',
        'Delete a specific artisan': 'https://franklin007.pythonanywhere.com/artisan/enterartisanemailaddresshere/',
    })
    

@api_view(['GET'])
def All_Users(request):
    AllUser = UserRegisterModel.objects.all()
    serializer = RegisterSerializer(AllUser, many=True)
    return Response(serializer.data)
    


@api_view(['POST', 'GET'])
def Register_User(request):
    if request.method == 'POST':
        # serializer = RegisterSerializer(data = request.data)
        CheckEmail = UserRegisterModel.objects.filter(Email = request.data['Email'])
        CheckPassword = request.data['Password'] != request.data['ConfirmPassword']
        if CheckEmail:
            return Response({
                'status':400,
                'message': 'This email address has already been registered.'
            })
            
        if CheckPassword:
            return Response({
                'status':400,
                'message': 'Passwords are not same'
            })
            
        RegisterNewUser = UserRegisterModel.objects.create(
            Fullname = request.data['Fullname'],
            Email = request.data['Email'],
            PhoneNumber = request.data['PhoneNumber'],
            Skill = request.data['Skill'],
            Location = request.data['Location'],
            NIN = request.data['NIN'],
            Password = request.data['Password'],
            ConfirmPassword = request.data['ConfirmPassword'],
        )      
        serializer = RegisterSerializer(RegisterNewUser, many=False)
        if (serializer):
            return Response({
                'status':200,
                'message':'User created successfully',
                'data':serializer.data
            })
            
        else:
            return Response({
                'status':400,
                'message': 'An error occured. Try again',
                'error': serializer.error_messages
            })
    else:
        return Response({
            'Prompt':'Provide the following information within the centent box(in JSON) format in order to register an artisan',
            'Information required': "1. 'Fullname', 2. 'Email', 3. 'PhoneNumber', 4. 'Skill', 5. 'Location', 6. 'NIN', 7. 'Password', 8. 'ConfirmPassword'",
        })



@api_view(['POST'])
def Login_User(request):
    try: 
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            
            user = authenticate(email = email, password = password)
            
            if user is None:
                return Response({
                    'status': 400,
                    'message': 'Invalid user details, Try again',
                    'data': serializer.error
                })
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'status':200,
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data['email']
            })
            
        else:
            return Response({
                'status': 400,
                'message': 'An error occured',
                'error': serializer.error_messages
            })        
    except:
        pass

    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.', 
                             'status' : 200
                             })
        except Exception as e:
            return Response({'error': str(e),
                             'message': 'An erro occured. Try again'
                             })
        


# FIND AN ARTISAN BY EMAIL ADDRESS AND ALSO UPDATE USER DATA
@api_view(['GET', 'PUT'])
def Aritisan(request, email):
    if request.method == 'GET':
        try:
            CurrentUser = UserRegisterModel.objects.get(Email = email)
            if CurrentUser:
                CurrentUserSerialized = RegisterSerializer(CurrentUser, many = False)
                return Response({
                    'status': 200,
                    'message': 'User Data Found',
                    'data': CurrentUserSerialized.data
                })
                
            else:
                return Response({
                    'status': 400,
                    'message': 'Email was not found',
                })
                
        except:
                return Response({
                    'Prompt':'Provide an email address within the URL in order to find an artisan',
                    'URL Format': "https://franklin007.pythonanywhere.com/userdetails/enteremailaddresshere/",
                })
    # UPDATE AN ARTISAN DATA STARTS HERE
    if request.method == 'PUT':
        CurrentUser = UserRegisterModel.objects.get(Email = email)
        CurrentUser.Fullname = request.data['Fullname']
        CurrentUser.Email = request.data['Email']
        CurrentUser.PhoneNumber = request.data['PhoneNumber']
        CurrentUser.Skill = request.data['Skill']
        CurrentUser.Location = request.data['Location']
        CurrentUser.NIN = request.data['NIN']
        
        CurrentUser.save()
        CurrentUserSerialized = RegisterSerializer(CurrentUser, many=False)
        return Response({
            'status': 200,
            'message': 'Artisan data has been updated successfully',
            'data': CurrentUserSerialized.data
        })


@api_view(['DELETE', 'GET'])
def Delete_Aritisan(request, email):
    try: 
        if request.user == 'DELETE':
            CurrentUser = UserRegisterModel.objects.get(Email = email)
            CurrentUser.delete()
            return redirect('All_Users')
    
    except: 
            return Response({
                'status': 400,
                'message': 'No artisan is found in this Location for now',
            })
    
    return Response({
        'Prompt':"Provide the artisan's email address using the format below within the URL to delete",
        'Format': "https://franklin007.pythonanywhere.com/artisan/enteremailaddresshere/",
    })
    

# FIND AN ARTISAN BY LOCATION
@api_view(['GET'])
def FindLocation(request, location):
   try:
        CurrentLocation = UserRegisterModel.objects.filter(Location__icontains = location)
        if CurrentLocation:
            CurrentLocationSerialized = RegisterSerializer(CurrentLocation, many = True)
            return Response({
                'status': 200,
                'message': 'Artisan found in this Location.',
                'result': CurrentLocation.count(),
                'data': CurrentLocationSerialized.data
            })
            
        else:
            return Response({
                'status': 400,
                'message': 'No artisan is found in this Location for now',
            })
            
   except:
        return Response({
            'Prompt':'Provide an location within the URL in order to find an artisan',
            'URL Format': "https://franklin007.pythonanywhere.com/userdetails/enterlocationhere/",
        })
    # return Response('Find Location')
















# {
#     "Fullname": "John Peters",
#     "Email": "johnpeters@gmail.com",
#     "PhoneNumber": "09022234343",
#     "Skill": "tailor",
#     "Location": "Abuja",
#     "NIN": "00001111000",
#     "Password": "123",
#     "ConfirmPassword": "123"
# }