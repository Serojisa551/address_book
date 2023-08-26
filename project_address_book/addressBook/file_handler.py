from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.template import loader
from .forms import ContactForm
from .models import Contact
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
@login_required
def register_contact(request):
    """
    Handles requests to register new contacts.
    Creates and saves a contact if the form is valid, otherwise displays an empty form.
    """
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        userPk = request.user.pk 
        request_copy = request.POST.copy()
        request_copy["userId"] = userPk
        request.POST = request_copy
        form = ContactForm(request.POST)
        for obj in phone_number:
            if 48 > ord(obj) or ord(obj) > 57:
                return render(request, 'addressbook/contact_register.html')
        if form.is_valid():
            form.save()
            return redirect('contact_list') 
    else:
        form = ContactForm()
    return render(request, 'addressbook/contact_register.html', {'form': form})

@login_required
def contact_list(request):
    """
    Displays a list of all contacts retrieved from the database.
    """
    contacts = Contact.objects.all()
    contacts_pk = []
    userPk = request.user.username 
    for obj in contacts: 
        userId = str(obj.userId)
        if userPk == userId:
            contacts_pk.append(obj.userId.pk)
    contacts = Contact.objects.filter(userId__in=contacts_pk)
    return render(request, 'addressbook/contact_list.html', {'contacts': contacts})

@login_required
def delete_contact(request, pk):
    """
    Deletes a contact based on the provided pk if the request is made using the POST method,
    otherwise displays a confirmation page for contact deletion.
    """
    contact = get_object_or_404(Contact, pk=pk)
    userPk = request.user.username
    userId = contact.userId
    if request.method == 'POST':
        if userPk == userId:
            print("userPk  userId", userPk, userId)
            contact.delete()
            return redirect('contact_list')
    return render(request, 'addressbook/contact_delete.html', {'contact': contact})

@login_required
def details_contact(request, pk):
    """
    Displays the details of a specific contact based on the provided primary key (pk).
    Retrieves the contact from the database and renders the contact details template.
    """
    contact = Contact.objects.get(pk=pk)
    template = loader.get_template("addressbook/contact_details.html")
    context = {
        "contact": contact,
    }
    return HttpResponse(template.render(context, request))

@login_required
def save_address_book(request):
    """
    Handles the process of saving the address book data to a JSON file.
    Retrieves contact data from the database, serializes it to JSON format,
    and saves it to a user-specified or default file in the 'data' directory.
    If no file name is provided, the default name 'backup.json' is used.
    """
    if request.method == 'POST':
        file_name = request.POST.get('file_name')

        if file_name[-5:] != ".json" and len(file_name) != 0:
            file_name = file_name + '.json'

        elif len(file_name) == 0:
            file_name = "backup.json"

        contacts = Contact.objects.all()
        contacts_pk = []
        userPk = request.user.username 
        for obj in contacts: 
            userId = str(obj.userId)
            if userPk == userId:
                contacts_pk.append(obj.userId.pk)
        contacts = Contact.objects.filter(userId__in=contacts_pk)
        json_data = serialize('json', contacts)

        file_path = f'data/{file_name}' 
        with open(file_path, 'w') as file:
            file.write(json_data)

    return render(request, 'addressBook/backup_address_book.html')

@login_required
def import_address_book(request):
    """
    Handles the process of importing contact data from a JSON file into the database.
    Reads the JSON file, parses the data, and creates Contact objects in the database.
    """
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        file_path = f'data/{file_name}'

        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                for item in json_data:
                    contact_data = {
                        'name': item['fields']['name'],
                        'phone_number': item['fields']['phone_number'],
                        'email': item['fields']['email'],
                        'notes': item['fields']['notes']
                    }
                    try:
                        Contact.objects.create(**contact_data)
                    except IntegrityError:
                        pass
        except FileNotFoundError:
            pass
        return redirect('contact_list')
    return render(request, 'addressBook/import_address_book.html')

@login_required
def update_contact(request, pk):
    """
    Handles requests to update the details of an existing contact.
    Retrieves the contact from the database based on the provided primary key (pk),
    processes the submitted form data if the request method is POST, and updates the contact details.
    Displays a form with pre-filled data for the user to edit, allowing changes to phone numbers,
    email addresses, and other contact information.
    """
    contact = Contact.objects.get(pk=pk)
    userPk = request.user.username
    userId = contact.userId
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if userPk == userId:
            if form.is_valid():
                form.save()
                return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'addressbook/contact_update.html', {'form': form})

@login_required
def contact_search(request):
    """
    Handles requests to search for contacts based on user-specified criteria.
    Retrieves contacts from the database that match the search criteria,
    such as name, phone number, email address, or notes.
    Displays a list of matching contacts  if no results are found.
    """
    if request.method == 'POST':
        query = request.POST.get("query")
        contacts_db = Contact.objects.all()
        langht = len(contacts_db)
        contacts = []
        userPk = request.user.username
        for index in range(0, langht):
            obj = contacts_db[index]
            userId = obj.userId
            if userPk == userId and obj.name == query or obj.phone_number == query or obj.email == query or obj.notes == query:
                contacts.append(obj)
        return render(request, 'addressbook/contact_search_results.html', {'contacts': contacts, 'query': query})
    return render(request, 'addressbook/contact_search_results.html')

def register_user(request):
    """
    This function handles user registration.
    
    If the request method is POST, it processes the registration form data.
    If the form is valid, a new user is created and redirected to the contact list page.
    
    If the request method is not POST, the user registration form is displayed.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list') 
    else:
        form = UserCreationForm()
    return render(request, 'addressBook/register_users.html', {'form': form})

def login_request(request):
    """
    This function handles user login.
    
    If the request method is POST, it processes the login form data.
    If the form is valid and the provided credentials match a user, the user is logged in.
    
    If the request method is not POST or if the credentials are invalid, the login form is displayed.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  
                return redirect("contact_list")
            else:
                messages.error(request, "Invalid username or password.") 
    form = AuthenticationForm()
    return render(request, "addressBook/login_users.html", {"login_form": form})


def logout_request(request):
    """
    Logs out the currently logged-in user and redirects to the login page.
    """
    logout(request) 
    return redirect('login_request') 

@login_required    
def delete_all_contact(request):
    """
    Deletes all contacts from the address book and redirects to the contact list.
    """
    contacts = Contact.objects.all()
    contacts.delete()
    return redirect('contact_list')
