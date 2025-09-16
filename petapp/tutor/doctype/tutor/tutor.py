# Copyright (c) 2025, mark1 and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.file_manager import save_file
import pytz
import frappe
from frappe.utils.file_manager import save_file
import re
import base64



class Tutor(Document):
	pass


@frappe.whitelist(allow_guest=True, methods=["POST"])
def createTutor():
	data = frappe.parse_json(frappe.request.data) if frappe.request and frappe.request.data else {}
	if not data:
		frappe.throw("Error en la recpeción de la información")
	docTutor = frappe.get_doc({
		"doctype": "Tutor",
		"full_name": data.get("full_name"),
		"email": data.get("email"),
		"identification": data.get("identification"),
		"phone": data.get("phone"),
		"birthday": data.get("birthday"),
		"password": data.get("password"),
	}).insert()

	imageTutor = save_file(
		filename = data.get("identification"),
		content = data.get("profilePhoto"),
		dt = "Tutor",
		dn = docTutor.name,
		decode = true,
		is_private = int(1)
	)
	docTutor.db_set("photo", imageTutor.file_url)

	#Crea token push notificacion
	createOneSignalToken()

	frappe.db.commit()
	return {
		""
	}
		
def createOneSignalToken(email, phone, id):
	time_zone = pytz.timezone("America/Guayaquil")
	timestamp_now = int(datetime.now().timestamp())
	url = "https://api.onesignal.com/users"   # ajusta la URL base según tu config
	headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer os_v2_app_t7mtrcuo4rdnzmhzsnpyx4j33ywhup3cuamuldeclpewp4xvp555slyl4pwbypjskadnot6bfz3ndkl6zzfny5k5vfdsc3kgnvw37ey"  # si tu API de OneSignal lo requiere
    }
	properties = {
		"language": "es",
		"timezone_id": time_zone.zone,   # equivalente a timeZone.getID()
		"lat": 90,
		"long": 135,
		"email": email,
		"phone": uphone,
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
	print(response)
