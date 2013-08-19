from pluginmanager.pluginmanager import register_plugin, plugin
import random

class RandomNumber(plugin):

  name = 'Random number'
  
  # 0: Match on Private Messages | 1: Match on Group Chat
  permissions = [True,True]   

  def plugin_init():
    pass

  def match():
    return '^!(random-number)($|\s)'

  def send_message(message,match,nick):
    msg = message.split(' ')[1:]
    if len(msg) == 2 and msg[0].isdecimal() and msg[1].isdecimal():
      try:
        return str(random.randint(int(msg[0]), int(msg[1])))
      except ValueError as v:
        return 'Ouch %s that hurts, please try again with a valid number range' % nick
    else:
      return 'Usage:\n\t!random-number <range-begin> <range-end>'

  def help():
    return 'Random number plugin\nUsage: !random-number <range-begin> <range-end>'
      
register_plugin(RandomNumber)
