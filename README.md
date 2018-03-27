# Shiny Umbrella

Shiny Umbrella is a system for controlling your Linux computer by [voice
command](https://www.youtube.com/watch?v=JKoSZS4ovKA). It's designed to work
using Dragon NaturallySpeaking / Dragon Professional
Individual 15 and Linux. Nuance has a lot of names for what is mostly the same
product with different vocabularies and features. DPI 15 is the newest version
of Dragon for people outside of law and medicine. Dragon runs in a Windows
virtual machine, and connects to a Linux server server over TCP. Dragon sends
events over the TCP socket and receives commands that control dictation.
Theoretically we could run Dragon inside of Wine but that is future work. We
could also theoretically use other speech recognizers e.g. Mozilla's DeepSpeech.
That will only be viable if their implementation gets a lot faster. Dragon is
the best option available even though it is very expensive and the setup is
baroque.

This design is similar to Aenea with Dragonfly but different in that most of the
logic lives on the Linux side.

N.b. this project isn't usable at all right now.
