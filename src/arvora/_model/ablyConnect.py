import asyncio
import time
from ably import AblyRealtime

async def main():

  # conectando ably
  # Connect to Ably with your API key
  ably = AblyRealtime('LpWF9g.DOL7Qg:UqnSdD--SkQmbHCVb_q2gl0s4KhDF4pqdJ-2el1UZzI')
  await ably.connection.once_async('connected')
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
