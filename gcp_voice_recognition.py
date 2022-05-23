from google.cloud.speech_v1.types.cloud_speech import SpeechContext
# from google.cloud import language
from google.oauth2 import service_account

path=r'C:\Users\Bilal\Desktop\POC\instance\audio-uploads\2022-01-10_192329.778877.wav'
def transcribe_file(speech_file):
    # credentials = service_account.Credentials.from_service_account_file("C:/Users/Bilal/Downloads/banded-arcana-337718-06d3bc030572.json")
    # client = language.LanguageServiceClient(credentials=credentials)
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech_v1p1beta1
    speech_context = speech_v1p1beta1.SpeechContext(phrases=["two","Imtiaz"],boost=15.0)
    client = speech_v1p1beta1.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech_v1p1beta1.RecognitionAudio(content=content)

    config = speech_v1p1beta1.RecognitionConfig(
        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-PK",
        speech_contexts=[speech_context]
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    return result.alternatives[0].transcript
