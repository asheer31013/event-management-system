from django.shortcuts import render, get_object_or_404
from .models import Event, Registration
from django.contrib import messages
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
# Show list of events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# Show event detail and handle registration

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST['name']
        roll_number = request.POST['roll_number']

        existing = Registration.objects.filter(event=event, roll_number=roll_number)

        if not existing:
            Registration.objects.create(
                event=event,
                name=name,
                roll_number=roll_number
            )

            messages.success(request, "Registration successful!")

        else:
            messages.error(request, "You already registered for this event.")

    return render(request, 'events/event_detail.html', {'event': event})


def organizer_report(request):
    events = Event.objects.all()

    report_data = []

    for event in events:
        total_registered = Registration.objects.filter(event=event).count()
        total_attended = Registration.objects.filter(event=event, attended=True).count()

        report_data.append({
            'event': event,
            'registered': total_registered,
            'attended': total_attended
        })

    return render(request, 'events/report.html', {'report_data': report_data})
def export_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="event_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Event', 'Registered', 'Attended'])

    events = Event.objects.all()

    for event in events:
        registered = Registration.objects.filter(event=event).count()
        attended = Registration.objects.filter(event=event, attended=True).count()

        writer.writerow([event.title, registered, attended])

    return response

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.conf import settings
import os


def download_certificate(request, registration_id):

    registration = Registration.objects.get(id=registration_id)

    # Allow certificate only if attended
    if not registration.attended:
        return HttpResponse("Certificate available only after attendance confirmation.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    width, height = A4
    p = canvas.Canvas(response, pagesize=A4)

    # ---------- Certificate Background ----------
    bg_path = os.path.join(settings.BASE_DIR, 'events/static/events/images/certificate_bg.jpg')

    if os.path.exists(bg_path):
        background = ImageReader(bg_path)
        p.drawImage(background, 0, 0, width=width, height=height)

    # ---------- Certificate Title ----------
    p.setFont("Helvetica-Bold", 36)
    p.setFillColorRGB(0.1, 0.2, 0.6)
    p.drawCentredString(width/2, height-200, "Certificate of Participation")

    # ---------- Subtitle ----------
    p.setFont("Helvetica", 18)
    p.drawCentredString(width/2, height-260, "This certificate is proudly presented to")

    # ---------- Student Name ----------
    p.setFont("Helvetica-Bold", 28)
    p.setFillColorRGB(0,0,0)
    p.drawCentredString(width/2, height-320, registration.name)

    # ---------- Participation Text ----------
    p.setFont("Helvetica", 18)
    p.drawCentredString(width/2, height-370, "for successfully participating in")

    # ---------- Event Title ----------
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width/2, height-420, registration.event.title)

    # ---------- Date ----------
    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height-470, f"Date: {registration.event.date}")

    # ---------- Signature Section ----------
    p.line(width/2 - 80, 150, width/2 + 80, 150)

    p.setFont("Helvetica", 14)
    p.drawCentredString(width/2, 130, "Event Organizer")

    p.showPage()
    p.save()

    return response