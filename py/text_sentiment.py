import io
import os
import json
from google.cloud import language_v1
from google.cloud.language_v1 import enums as fish
from google.cloud.speech_v1 import enums
from google.cloud import speech_v1


credential_path = "My First Project-82ed8a17d1d9.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition
    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
            }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    print("got a response")
    print(response)
    output = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        output.append(alternative.transcript)
        print(alternative)
        print(u"Transcript: {}".format(alternative.transcript))
    return output

def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = fish.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = fish.EncodingType.UTF8

    response = client.analyze_sentiment(document, encoding_type=encoding_type)
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
            u"Document sentiment magnitude: {}".format(
                response.document_sentiment.magnitude
                )
            )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(sentence.sentiment)
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))
    return response.document_sentiment.score


def main():
    directory = "audio/"
    print("running main")
    scores = dict()
    for filename in os.listdir(directory):
        print(filename)
        print(directory)
        strList = sample_recognize(directory+filename)
        sentiments = []
        for item in strList:
            print(item)
            sentiments.append(sample_analyze_sentiment(item))
        sum = 0
        for item in sentiments:
            sum = sum + item
        sum = sum/len(sentiments)
        goodpart, badpart = os.path.splitext(filename)
        print(goodpart)
        scores[int(goodpart)] = sum
        print(sum)
    sortedData = dict()
    for k in sorted(scores.keys()):
        sortedData[k] = scores[k]
    with open("appSpeechData.json", "w") as fp:
        fp.write(json.dumps(sortedData))
    print(sortedData)

if __name__ == "__main__":
    main()
