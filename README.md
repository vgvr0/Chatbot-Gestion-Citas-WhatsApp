# BeautySalon WhatsApp Booking System 🌟💅

Un sistema moderno de gestión de citas para salones de belleza y estéticas a través de WhatsApp, desarrollado con Python, Flask y Twilio.

## 🎯 Características Principales

- **Reserva de Citas por WhatsApp**: Sistema automatizado y conversacional
- **Gestión de Servicios**: Configura fácilmente tus servicios, precios y duraciones
- **Horarios Flexibles**: Define tus horarios de trabajo para cada día de la semana
- **Almacenamiento Simple**: Sistema de persistencia basado en JSON
- **Fácil de Personalizar**: Adapta los mensajes y servicios a tu negocio
- **Interfaz Conversacional**: Experiencia natural y amigable para los clientes

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/beautysalon-whatsapp-booking.git
cd beautysalon-whatsapp-booking
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tus credenciales de Twilio:
```python
TWILIO_ACCOUNT_SID = 'tu_account_sid'
TWILIO_AUTH_TOKEN = 'tu_auth_token'
```

4. Inicia el servidor:
```bash
python app.py
```

## 📋 Requisitos Previos

- Python 3.7+
- Cuenta de Twilio
- Número de WhatsApp Business
- Servidor web con HTTPS (para producción)

## 🛠️ Configuración

### Servicios
Modifica el diccionario `SERVICES` en `app.py`:
```python
SERVICES = {
    '1': {'name': 'Manicura', 'duration': 45, 'price': 20},
    '2': {'name': 'Pedicura', 'duration': 60, 'price': 25},
    # Añade más servicios aquí
}
```

### Horarios
Ajusta el diccionario `BUSINESS_HOURS` según tus necesidades:
```python
BUSINESS_HOURS = {
    'Lunes': ['09:00', '18:00'],
    'Martes': ['09:00', '18:00'],
    # Configura más días aquí
}
```

## 💬 Uso

Los clientes pueden interactuar con el sistema mediante comandos simples por WhatsApp:

- `hola` - Inicia el proceso de reserva
- `cancelar` - Cancela una cita existente

El sistema guiará al cliente a través del proceso de reserva paso a paso.

## 🤝 Contribuir

1. Haz un Fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commitea tus cambios (`git commit -m 'Add: alguna característica asombrosa'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## ✨ Próximas Características

- [ ] Sistema de recordatorios automáticos
- [ ] Panel de administración web
- [ ] Lista de espera para cancelaciones
- [ ] Múltiples idiomas
- [ ] Estadísticas y reportes
- [ ] Integración con Google Calendar

