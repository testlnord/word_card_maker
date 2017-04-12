# Word Card Maker
Flash cards from your browser
============================
Using current plugin: it works on wikipedia.org
============================
* deploy the bash script
* preferences can be checked by typing "about:addons" in Firefox browser
* currently, in preferences you can select different colors of border(e.g. "red") -- and the border will change. In future, here the language will be selected
* by double-clicking the word, you will see the red box in the top left corner. It will contain the word itself, "Translation" - in order to get translation from server later, and the current context in which the word was found.
* currently, by right-clicking you'll get the context menu(for future making visible the card and getting translation). Unuseful staff: by clicking "picturesque", you'll get redirected to the url with the picture, and by clicking "changeColor", you'll change the border color. It is here only to test the options.
* the icon on the bar doesn't have any functionality yet. Here, in the future, the preference menu can be added(it was not discussed yet)

Server setup
============================

Make sure you have installed:

- Docker v1.9.0
- Docker Compose v1.5.0

Clone the repository:
```
git clone https://github.com/testlnord/word_card_maker.git
```
Go to `backend` folder and copy `fake.env` to `.env` file:
```
cd ./backend
cp fake.env .env
```
Change `YA_API_KEY` in `.env` to something retrieved here: https://tech.yandex.ru/keys/get/?service=dict

Run `docker-compose`:
```
sudo docker-compose up
```
Congratulations, server is running
