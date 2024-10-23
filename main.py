from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import json
import os

app = Flask(__name__)

# Configuración de Twilio
TWILIO_ACCOUNT_SID = 'tu_account_sid'
TWILIO_AUTH_TOKEN = 'tu_auth_token'
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Archivo para almacenar las citas
APPOINTMENTS_FILE = 'appointments.json'

# Horario de trabajo
BUSINESS_HOURS = {
    'Lunes': ['09:00', '18:00'],
    'Martes': ['09:00', '18:00'],
    'Miércoles': ['09:00', '18:00'],
    'Jueves': ['09:00', '18:00'],
    'Viernes': ['09:00', '18:00'],
    'Sábado': ['09:00', '14:00']
}

# Servicios disponibles y duración en minutos
SERVICES = {
    '1': {'name': 'Manicura', 'duration': 45, 'price': 20},
    '2': {'name': 'Pedicura', 'duration': 60, 'price': 25},
    '3': {'name': 'Depilación facial', 'duration': 30, 'price': 15},
    '4': {'name': 'Limpieza facial', 'duration': 60, 'price': 40}
}

def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, 'w') as f:
        json.dump(appointments, f)

def get_available_slots(date, service_duration):
    appointments = load_appointments()
    day_name = date.strftime('%A')
    if day_name not in BUSINESS_HOURS:
        return []
    
    start_time = datetime.datetime.strptime(BUSINESS_HOURS[day_name][0], '%H:%M').time()
    end_time = datetime.datetime.strptime(BUSINESS_HOURS[day_name][1], '%H:%M').time()
    
    current_time = datetime.datetime.combine(date, start_time)
    end_datetime = datetime.datetime.combine(date, end_time)
    
    slots = []
    while current_time + datetime.timedelta(minutes=service_duration) <= end_datetime:
        slot_str = current_time.strftime('%Y-%m-%d %H:%M')
        if slot_str not in appointments:
            slots.append(current_time.strftime('%H:%M'))
        current_time += datetime.timedelta(minutes=30)
    
    return slots

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    resp = MessagingResponse()
    msg = resp.message()

    # Estado del usuario
    user_states = {}
    
    if sender not in user_states:
        user_states[sender] = {'state': 'initial'}

    if incoming_msg == 'hola':
        msg.body("""¡Bienvenida al sistema de citas de Estética Belle!
        
Para comenzar, estos son nuestros servicios:
1. Manicura (45min - 20€)
2. Pedicura (60min - 25€)
3. Depilación facial (30min - 15€)
4. Limpieza facial (60min - 40€)

Por favor, responde con el número del servicio que deseas.""")
        user_states[sender]['state'] = 'selecting_service'
    
    elif user_states[sender]['state'] == 'selecting_service':
        if incoming_msg in SERVICES:
            service = SERVICES[incoming_msg]
            user_states[sender]['service'] = service
            user_states[sender]['state'] = 'selecting_date'
            
            msg.body("""Por favor, indica la fecha deseada en formato DD/MM/YYYY.
Por ejemplo: 25/10/2024""")
        else:
            msg.body("Por favor, selecciona un número de servicio válido (1-4).")
    
    elif user_states[sender]['state'] == 'selecting_date':
        try:
            date = datetime.datetime.strptime(incoming_msg, '%d/%m/%Y')
            service = user_states[sender]['service']
            available_slots = get_available_slots(date, service['duration'])
            
            if available_slots:
                user_states[sender]['date'] = date
                user_states[sender]['state'] = 'selecting_time'
                msg.body(f"Horarios disponibles para {date.strftime('%d/%m/%Y')}:\n" + 
                        "\n".join(available_slots) +
                        "\nPor favor, selecciona un horario (formato HH:MM)")
            else:
                msg.body("Lo siento, no hay horarios disponibles para esa fecha. Por favor, elige otra fecha.")
        except ValueError:
            msg.body("Por favor, introduce una fecha válida en formato DD/MM/YYYY")
    
    elif user_states[sender]['state'] == 'selecting_time':
        try:
            time = datetime.datetime.strptime(incoming_msg, '%H:%M').time()
            date = user_states[sender]['date']
            service = user_states[sender]['service']
            
            appointment_datetime = datetime.datetime.combine(date, time)
            appointments = load_appointments()
            
            if appointment_datetime.strftime('%Y-%m-%d %H:%M') not in appointments:
                appointments[appointment_datetime.strftime('%Y-%m-%d %H:%M')] = {
                    'service': service['name'],
                    'client': sender
                }
                save_appointments(appointments)
                
                msg.body(f"""¡Cita confirmada!
Servicio: {service['name']}
Fecha: {date.strftime('%d/%m/%Y')}
Hora: {time.strftime('%H:%M')}
Precio: {service['price']}€

Te esperamos. Para cancelar tu cita, envía 'cancelar'.""")
                user_states[sender] = {'state': 'initial'}
            else:
                msg.body("Lo siento, ese horario ya no está disponible. Por favor, elige otro horario.")
        except ValueError:
            msg.body("Por favor, introduce un horario válido en formato HH:MM")

    elif incoming_msg == 'cancelar':
        appointments = load_appointments()
        client_appointments = {k: v for k, v in appointments.items() if v['client'] == sender}
        
        if client_appointments:
            for appointment in client_appointments:
                del appointments[appointment]
            save_appointments(appointments)
            msg.body("Tu cita ha sido cancelada. ¡Esperamos verte pronto!")
        else:
            msg.body("No tienes ninguna cita programada.")
    
    else:
        msg.body("""Bienvenida al sistema de citas de Estética Belle.
Para comenzar, envía 'hola'.
Para cancelar tu cita, envía 'cancelar'.""")

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
