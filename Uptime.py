from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import AnyExcept, IntentHandler, Online
import subprocess
class Uptime(AliceSkill):
	"""
	Author: Bobby C
	Description: find out the uptime
	"""
	def __init__(self):
		self.result = ""
		super().__init__()

	@IntentHandler('Uptime')
	@Online
	def runUptime(self, session: DialogSession):
		self.ThreadManager.doLater(interval=0, func=self.getUptime, kwargs={'session': session})
		self.logDebug("Finding uptime")
		self.endDialog(sessionID=session.sessionId, text=self.randomTalk('running'))

	@AnyExcept(exceptions=(KeyError), text='failed', printStack=True)
	@Online
	def getUptime(self,session: DialogSession):
			self.logInfo("Calculating uptime.")
			raw = subprocess.check_output('uptime').decode("utf8").split(" ")
			self.logDebug(raw)
			if raw[5] == "min":
				self.result = raw[4]+" minutes"
			elif raw[5] == "days":
				self.result = raw[4]+" Days"
			else:
				self.result = raw[4]+" Hours"
			self.logDebug(f'Uptime: {self.result}')
			self.say(text=self.randomTalk(text='self.result', replace=[self.result]), deviceUid=session.deviceUid)
