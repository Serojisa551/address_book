from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .forms import ContactForm
from .models import Contact


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

def update_contact(request, pk):
    """
    Handles requests to update the details of an existing contact.
    Retrieves the contact from the database based on the provided primary key (pk),
    processes the submitted form data if the request method is POST, and updates the contact details.
    Displays a form with pre-filled data for the user to edit, allowing changes to phone numbers,
    email addresses, and other contact information.
    """
    contact = Contact.objects.get(pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'addressbook/contact_update.html', {'form': form})

def contact_search(request, query):
    """
    Handles requests to search for contacts based on user-specified criteria.
    Retrieves contacts from the database that match the search criteria,
    such as name, phone number, email address, or notes.
    Displays a list of matching contacts  if no results are found.
    # """
    contacts_db = Contact.objects.all()
    langht = len(contacts_db)
    contacts = []
    for index in range(0, langht):
        elm = contacts_db[index]
        if elm.name == query or elm.phone_number == query or elm.email == query or elm.notes == query:
            contacts.append(elm)


    return render(request, 'addressbook/contact_search_results.html', {'contacts': contacts, 'query': query})
