#==>Local Import
from kavenegar import *


def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('5548565754686E477A666B68443666645A785078485252734454454D68584E5575325537426730556767413D')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{code}کد تایید شما'
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)