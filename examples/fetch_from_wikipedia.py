import requests


def get_abstract_from_wikipedia(noun: str) -> str:
    url = f"https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={noun}"

    response = requests.get(url)
    res_json = response.json()

    abstract = []
    for id in res_json["query"]["pages"]:
        if id == "-1":
            print(f"Sorry, I don't know the word {noun}")
            return ""
        else:
            abstract = [res_json["query"]["pages"][id]["extract"]
                        for id in res_json["query"]["pages"]]

    return abstract[0].split("\n")[0]


def main():
    nouns = ["吾輩はねこである", "吾輩は猫である", "ちくわ", "京都"]

    for noun in nouns:
        abstract = get_abstract_from_wikipedia(noun)
        print(abstract)


if __name__ == "__main__":
    main()
