from django.shortcuts import render, redirect
from .models import InfoMessage
 
 
def ChatView(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    all_messages = InfoMessage.objects.all()
    context = {'messages':all_messages}
    return render(request, "chat/chatpage.html", context)