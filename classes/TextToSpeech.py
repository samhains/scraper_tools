from classes.BaseThread import BaseThread as Parent
import random
import time
import wave
import boto3
import os, os.path

client = boto3.client('polly')

class TextToSpeech(Parent):
    def __init__(self, mixer, sleep=False, max_client=None, save=False, file_index=0):
        Parent.__init__(self)
        self.mixer = mixer
        self.text = ""
        self.save_file = save
        self.max_client = max_client
        self.sleep = sleep
        self.file_index = file_index

        self._voice_ids = [
            'Geraint', 'Gwyneth', 'Mads', 'Naja', 'Hans', 'Marlene', 'Nicole',
            'Russell', 'Amy', 'Brian', 'Emma', 'Raveena', 'Ivy', 'Joanna', 'Joey',
            'Justin', 'Kendra', 'Kimberly', 'Salli', 'Conchita', 'Enrique', 'Miguel',
            'Penelope', 'Chantal', 'Celine', 'Mathieu', 'Dora', 'Karl', 'Carla',
            'Giorgio', 'Mizuki', 'Liv', 'Lotte', 'Ruben', 'Ewa', 'Jacek', 'Jan',
            'Maja', 'Ricardo', 'Vitoria', 'Cristiano', 'Ines', 'Carmen', 'Maxim',
            'Tatyana', 'Astrid', 'Filiz', 'Vicki'
        ]

    def _get_file_index(self):
        i = len([name for name in os.listdir('../audio/')])
        return "{0:0>3}".format(i)


    def _save(self, text, sound_data):
        self.text = text
        self.file_index = self._get_file_index()
        fname = "../audio/{}.wav".format(self.file_index)
        data = wave.open(fname, 'w')
        data.setparams((1, 2, 16200, 0, 'NONE', 'NONE'))
        data.writeframes(sound_data)
        if self.max_client != None:
            self.max_client.send_message("/speak", fname)

    def _polly_request(self, text):
        voice_id = random.choice(['Joey', 'Joanna', 'Emma'])
        response = client.synthesize_speech(
            OutputFormat='pcm',
            TextType="ssml",
            Text="<speak>{}<break time='1000ms'/>.</speak>".format(text),
            VoiceId=voice_id
        )
        self.sound_data = response["AudioStream"].read()
        # print(type(self.sound_data))
        if self.save_file:
            self._save(text, self.sound_data)
        else:
            sound = self.mixer.Sound(self.sound_data)
            self.mixer.stop()
            sound.play()
            # pygame is non blocking so thread things we are done!
            time.sleep(8)

    def run_(self, text):
        self.text = text
        self.target = self._polly_request
        self.args = [self.text]
        self.start()
        if self.sleep:
            time.sleep(self.sleep)
