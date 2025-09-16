from frappe.model.document import Document
from datetime import datetime
from frappe.utils.file_manager import save_file
import pytz
import frappe
from frappe.utils.file_manager import save_file
import re
import base64
import json

@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_tutor():
     try:
        print("hola")
        raw_data = frappe.request.data
        data = json.loads(raw_data.decode("utf-8")) if raw_data else {}
            
        if not data:
            frappe.throw("No se recibió información")

        docTutor = frappe.get_doc({
            "doctype": "Tutor",
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "identification": data.get("identification"),
            "phone": data.get("phone"),
            "birthday": data.get("birthday"),
            "password": data.get("password"),}).insert()

        imageTutor = save_file(
            filename = data.get("identification"),
            content = data.get("profile_photo"),
            dt = "Tutor",
            dn = docTutor.name,
            decode = True,
            is_private = int(1)
        )
        docTutor.db_set("photo", imageTutor.file_url)

        #Crea token push notificacion
        #createOneSignalToken(data.get("email"),data.get("phone"),data.get(""),docTutor.name)

        frappe.db.commit()
        return {
            ""
        }
     except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error en create_tutor")
        raise
		
def create_one_signal_token(email, phone, id):
    time_zone = pytz.timezone("America/Guayaquil")
    timestamp_now = int(datetime.now().timestamp())

    url = "https://api.onesignal.com/users"   # ajusta la URL según tu configuración
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer TU_API_KEY_DE_ONESIGNAL"
    }

    properties = {
        "language": "es",
        "timezone_id": time_zone.zone,
        "lat": 90,
        "long": 135,
        "email": email,
        "phone": phone,
        "country": "EC",
        "first_active": timestamp_now,
        "last_active": timestamp_now
    }

    identity = {
        "external_id": str(id)
    }

    payload = {
        "properties": properties,
        "identity": identity
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    frappe.logger().info(f"OneSignal response: {response.json()}")
