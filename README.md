# Question answering system by asking in Japanese and answering in English

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

```
python frame_weather_system.py
```

Start dialogue by typing `/start`.


## Reference

東中, 稲葉, 水上, 『Pythonでつくる対話システム』, オーム社 (2020).
