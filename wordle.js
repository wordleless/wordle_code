
var height = 8; //попыток
var width = 5; //длина

var row = 0; //номер попытки
var col = 0; //номер буквы попытки

var gameOver = false;
var wordList = ["кошка", "вальс", "абака"]


var word = wordList[Math.floor(Math.random()*wordList.length)].toUpperCase();
console.log(word);

window.onload = function(){
    intialize();
}


function intialize() {

    // табличка
    for (let r = 0; r < height; r++) {
        for (let c = 0; c < width; c++) {
            let tile = document.createElement("span");
            tile.id = r.toString() + "-" + c.toString();
            tile.classList.add("tile");
            tile.innerText = "";
            document.getElementById("board").appendChild(tile);
        }
    }


    //подключаем клавиатуру
    document.addEventListener("keypress", (e) => {
        processInput(e);
    })
}



function processKey() {
    e = { "charcode" : this.id };
    processInput(e);
}

function processInput(e) {
    if (gameOver) return; 

    if (1040 <= e.charCode && e.charCode <= 1103) {
        if (col < width) {
            let currTile = document.getElementById(row.toString() + '-' + col.toString());
            if (currTile.innerText == "") {
                currTile.innerText = String.fromCharCode(e.charCode).toUpperCase();
                col += 1;
            }
        }
    }
    else if (e.code == "Backspace") { //я ещё не смогла норм подключить бэкспейс но всё будет
        if (0 < col && col <= width) {
            col -=1;
        }
        let currTile = document.getElementById(row.toString() + '-' + col.toString());
        currTile.innerText = "";
    }

    else if (e.code == "Enter") {
        update();
    }

    if (!gameOver && row == height) {
        gameOver = true;
        document.getElementById("answer").innerText = word;
    }
}

function update() {
    let guess = "";
    document.getElementById("answer").innerText = "";

    //соединяем буквы в слово
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;
        guess += letter;
    }

    guess = guess.toLowerCase();
    console.log(guess);

    if (!wordList.includes(guess)) {
        document.getElementById("answer").innerText = "Нет в списке слов";
        return;
    }
    
    //погнали проверять попытку
    let correct = 0;

    let letterCount = {}; //шоб не дважды
    for (let i = 0; i < word.length; i++) {
        let letter = word[i];

        if (letterCount[letter]) {
           letterCount[letter] += 1;
        } 
        else {
           letterCount[letter] = 1;
        }
    }

    console.log(letterCount);

    //правильные
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;

        //правильные по позиции
        if (word[c] == letter) {
            currTile.classList.add("correct");

            correct += 1;
            letterCount[letter] -= 1; //счётчик обратно
        }

        if (correct == width) {
            gameOver = true;
        }
    }

    console.log(letterCount);
    //не совсем правильные
    for (let c = 0; c < width; c++) {
        let currTile = document.getElementById(row.toString() + '-' + c.toString());
        let letter = currTile.innerText;

        //да уже ясно что там всё хорошо, скипаем
        if (!currTile.classList.contains("correct")) {
            //в слове ли?
            if (word.includes(letter) && letterCount[letter] > 0) {
                currTile.classList.add("present");
                
                letterCount[letter] -= 1;
            } //не в слове((
            else {
                currTile.classList.add("absent");
            }
        }
    }

    row += 1; //новая попытка
    col = 0; //начинается с нуля
}