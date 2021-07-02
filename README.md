# Question answering system by asking in Japanese and answering in English

## Setup environment

1. Create a conda environment
	```
	conda create -n environment_name python=3.8
	```

1. Install toolkits

	```
	conda install -c anaconda pyaudio
	conda install -c conda-forge ffmpeg
	conda install -c conda-forge pydub

	pip install dill
	pip install sklearn
	pip install sklearn-crfsuite
	pip install gensim
	pip install mecab-python3
	pip install google-cloud-translate
	pip install --upgrade google-cloud-speech
	pip install google-cloud-speech

	brew install --cask google-cloud-sdk
	```

## How to train

1. Prepare train/examples.txt, where `da` defines dialogue acts and concepts are highlighted in the XML format


1. Train dialogue act estimation model

	```
	cd train/dialogue_act
	python generate_da_samples.py
	python train_da_model.py
	```

	You can confirm that the model is working by running:

	```
	python da_extractor.py
	```

1. Train concept estimation model

	```
	cd train/concept
	python generate_concept_samples.py
	python train_concept_model.py
	```

	You can confirm that the model is working by running:

	```
	python concept_extractor.py
	```

## How to use

1. Create a Google account and register for Google Cloud Platform.
	1. Create a project.
	1. Enable "Cloud Speech-to-Text API", "Cloud Text-to-Speech API", and "Cloud Translation API".
	1. Create an account key and get a json file.

1. Place json API key file at the same directory as `qatranslator.py`. Also, set the following environment variable:

	```
	export GOOGLE_APPLICATION_CREDENTIALS="/path/to/json/file.json"
	```

1. Run app

	```
	python qatranslator.py
	```

	The program starts listening to you immediately.
	For example, if you ask "京都について教えてください", the system will answer "Kyoto is a place name and city in Japan."


## Reference

東中, 稲葉, 水上, 『Pythonでつくる対話システム』, オーム社 (2020).
