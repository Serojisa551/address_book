from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm
from .models import Contact
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError


def register_contact(request):
    """
    Handles requests to register new contacts.
    Creates and saves a contact if the form is valid, otherwise displays an empty form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list') 
    else:
        form = ContactForm()
    return render(request, 'addressbook/contact_register.html', {'form': form})

def contact_list(request):
    """
    Displays a list of all contacts retrieved from the database.
    """
    contacts = Contact.objects.all()
    return render(request, 'addressbook/contact_list.html', {'contacts': contacts})

def delete_contact(request, pk):
    """
    Deletes a contact based on the provided pk if the request is made using the POST method,
    otherwise displays a confirmation page for contact deletion.
    """
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'addressbook/contact_delete.html', {'contact': contact})

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

def save_address_book(request):
    """
    Handles the process of saving the address book data to a JSON file.
    Retrieves contact data from the database, serializes it to JSON format,
    and saves it to a user-specified or default file in the 'data' directory.
    If no file name is provided, the default name 'address_book_backup.json' is used.
    """
    if request.method == 'POST':
        file_name = request.POST.get('file_name')

        if file_name[-5:] != ".json" and len(file_name) != 0:
            file_name = file_name + '.json'

        elif len(file_name) == 0:
            file_name = "address_book_backup.json"

        contacts = Contact.objects.all()
        json_data = serialize('json', contacts)

        file_path = f'data/{file_name}' 
        with open(file_path, 'w') as file:
            file.write(json_data)

    return render(request, 'addressBook/backup_address_book.html')

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

    return render(request, 'addressBook/import_address_book.html')
