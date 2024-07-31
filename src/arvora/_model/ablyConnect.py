import asyncio
import time
from ably import AblyRealtime, AblyRest

async def main():

  # conectando ably
  # Connect to Ably with your API key
  ably = AblyRealtime('LpWF9g.DOL7Qg:UqnSdD--SkQmbHCVb_q2gl0s4KhDF4pqdJ-2el1UZzI')
  await ably.connection.once_async('connected')

  rest = AblyRest(key='LpWF9g.DOL7Qg:UqnSdD--SkQmbHCVb_q2gl0s4KhDF4pqdJ-2el1UZzI')
  token_request_params = {
    'clientId': 'client@example.com',
  }

  token_details = await rest.auth.request_token(token_params=token_request_params)
  print(token_request_params,token_details)
  print('Connected to Ably')

  #cria o canal
  # Create a channel called 'get-started' and register a listener to subscribe to all messages with the name 'first'
  channel = ably.channels.get('get-started')
  def listener(message):
      print('Message received: ' + message.data)
  await channel.subscribe('first', listener)

  # publica mensagem em 1s
  # Publish a message with the name 'first' and the contents 'Here is my first message!'
  time.sleep(1)
  await channel.publish('first', 'Here is my first message!')

  # fecha a conexão com o ably depois de 5s
  # Close the connection to Ably after a 5 second delay
  time.sleep(5)
  await ably.close()
  print('Closed the connection to Ably.')

asyncio.run(main())

"""
rest = AblyRest(key='xVLyHw.n0e_Dg:TuH_8e3L2GvCnkqyvnribF2PLDgBf-uBClsUmJjes0w')
token_request_data = {
    'clientId': 'client@example.com',
}


token_details = await rest.auth.request_token(token_params=token_request_data)


header = {
    "typ": "JWT",
    "alg": "HS256",
    "x-ably-token": token_details.token
}
claims = {
    "exp": int(time.time()) + 3600
}


base64_header = base64.urlsafe_b64encode(bytes(json.dumps(header), 'utf-8')).decode('utf-8')
base64_claims = base64.urlsafe_b64encode(bytes(json.dumps(claims), 'utf-8')).decode('utf-8')


signature = hashlib.sha256((base64_header + "." + base64_claims + "{{API_KEY_SECRET}}").encode('utf-8')).digest()
signature_base64 = base64.urlsafe_b64encode(signature).decode('utf-8')


jwt_token = base64_header + "." + base64_claims + "." + signature_base64

"""
