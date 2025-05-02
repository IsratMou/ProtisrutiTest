from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_type, password=None):
        if not email:
            raise ValueError("Email is required")
        email=self.normalize_email(email)
        user=self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, user_type, password=None): 
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        
        return self.create_user(email, first_name, last_name, 'admin', password)
    
    