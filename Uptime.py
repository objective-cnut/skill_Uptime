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

	def onStart(self):
		super().onStart()
		print("Starting.....")
	@IntentHandler('Uptime')
	@Online
	def Uptime(self, session: DialogSession):
		self.ThreadManager.doLater(interval=0, func=self.getUptime, kwargs={'session': session})
		self.logDebug("Finding uptime")
		self.endDialog(sessionID=session.sessionId, text=self.randomTalk('running'))

	@AnyExcept(exceptions=(KeyError), text='failed', printStack=True)
	@Online
	def getUptime(self,session: DialogSession):
			self.logInfo("Calculating uptime.")
			raw = subprocess.check_output('uptime').decode("utf8").split(" ")
			self.logDebug(raw)
			if raw[4] == "min,":
				self.result = raw[3]+" minutes"
			elif raw[4] == "days":
				self.result = raw[3]+" Days"
			else:
				self.result = raw[3]+" Hours"
			self.logDebug(f'Uptime: {self.result}')
			self.say(text=self.randomTalk(text='self.result', replace=[self.result]), deviceUid=session.deviceUid)
