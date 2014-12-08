# main.py -- put your code here!
#leds = [pyb.LED(i) for i in range(1,5)]

import micropython
import time
import yellow
import orange
import math
from pyb import DAC
import wave


def dacTone( dac, tone ):
	# Create a buffer containing a sine-wave
	buf = bytearray(100)
	for i in range(len(buf)):
		buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))
 		print("buf[ " + str(i) + "] = " + str(buf[i]) )

	# Output the sine-wave at tone (Hz)
	dac.write_timed(buf, tone * len(buf), mode=DAC.CIRCULAR)


turretDialogueDir = "turretDialogue"

# Map FileName with delays for each respective part
turretDialogueDict = { 
	"Searching"        : [800],
	"AreYouStillThere" : [700, 700],
	"ISeeYou"          : [550],
}

def turretSpeak( say ):
	numSegments = len( turretDialogueDict[say] )
	delayList = turretDialogueDict[say]

	global turretDialogueDir

	for i in range(numSegments):
		print("fileName: " + turretDialogueDir + '/' + "Turret_" + say + '_' + str(i+1) + '.wav')
		f = wave.open(turretDialogueDir + '/' + "Turret_" + say + '_' + str(i+1) + '.wav', 'r')
		dac.write_timed(f.readframes( f.getnframes() ), f.getframerate(), mode=DAC.NORMAL)
		# Delay for proper amount of time before sending the next audio segment
		pyb.delay(delayList[i])



def rotate( servo, oscillations, speed ):
	i = 0
	while (i < oscillations):
		servo.angle(30, speed)
		pyb.delay(speed)
		servo.angle(-30, speed)
		pyb.delay(speed)
		i+=1
	servo.angle(0, speed)




# Hardware mapping
dac = DAC(2)
motionDetectPin = pyb.Pin(pyb.Pin.board.X10, pyb.Pin.IN)
laserBeamPin = pyb.Pin(pyb.Pin.board.X8, pyb.Pin.OUT_PP)
rotateServo = pyb.Servo(1)



backToSleepTimeout = 100000

# Init servo to "home" position
rotateServo.angle(0)

# Let the motion sensor gain some awareness
pyb.delay(5000)



while( 1<2 ):
	# When the pin goes high. motion happened
	if motionDetectPin.value():
		laserBeamPin.high() # Turn on ze laser!!!!
		turretSpeak( "Searching" )
		# Make our turret rotate back and forth
		rotate( rotateServo, 4, 2000 )

		pyb.LED(2).on()
		pyb.delay(1000)


		i = 0
		# This doesn't really work, motion pin is active for too long
		while(i < backToSleepTimeout):
			if motionDetectPin.value():
				# Fire Away!
				#turretSpeak("Fire")
				pass
			i += 1

		turretSpeak("AreYouStillThere")
		# A breather is good, otherwise it can immediately go back into Activated Mode
		pyb.delay(1000)


	else:
		laserBeamPin.low() # turn laserBeam off
		pyb.LED(2).off()
		pyb.delay(1000)






		


	




