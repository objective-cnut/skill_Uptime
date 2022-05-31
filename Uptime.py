from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import AnyExcept, IntentHandler, Online
import subprocess
class Uptime(AliceSkill):
	"""
	Author: Bobby C
	Description: find out the uptime
	"""
	@IntentHandler("Uptime")
	@Online
	def runUptime(self, session: DialogSession):
		self.ThreadManager.doLater(interval=0, func=self.getUptime, kwargs={'session': session})
		self.logInfo("Finding uptime")
		self.endDialog(sessionID=session.sessionId, text=self.randomTalk('running'))

	@AnyExcept(exceptions=(KeyError), text='failed', printStack=True)
	@Online
	def getUptime(self,session: DialogSession):
			self.logInfo("Calculating uptime.")
			raw = subprocess.check_output('uptime').decode("utf8").split(" ")
			self.logInfo(raw)
			if raw[5] == "min":
				answer = raw[4]+" minutes"
			elif raw[5] == "days":
				answer = raw[4]+" Days"
			else:
				answer = raw[4]+" Hours"
			self.logInfo(f'Uptime: {raw}')
			self.say(text=self.randomTalk(text='raw', replace=[raw]), deviceUid=session.deviceUid)
