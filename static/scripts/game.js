

class Game {

    constructor(id, time=60) {
        this.time = time;
        this.score = 0;
        this.plays = 0; //Could be greater than words.length if words were rejected
        this.highscore = {score: 0, plays: 0};
        this.words = new Set();    //Set of unique words
//        this.$board = $(`#${id}`);
        this.word = document.querySelector("#word");
        this.timeDisplay = document.querySelector("#time-remaining");
        this.timeDisplay.innerHTML = "60";
        this.timer = setInterval((event) => {
            this.time --;
            this.timeDisplay.innerHTML = `${this.time}`;
            if(this.time <= 0) {
                this.stopGame();
            }
        }, 1000);
    }

/**
 * Clicking on a letter on the board adds it to the word to be submitted. A feature.
 * @param {Event} event 
 */    
    addLetter = (event) => {
        event.preventDefault();
        this.word.value += event.target.innerText;
        this.word.focus();
    }

/**
 * Stop the game when the timer runs out. Post the score while telling the server the game is over.
 * If the score is the new high score the serer will return that information.
 */
    stopGame() {
        $("#word").prop("disabled", true);
        $("#submitWord").prop("disabled", true);
        clearInterval(this.timer);
        if(this.score > this.highscore) {
            this.highscore = this.score
        }
        axios.post('/end', {params: {"score": this.score, "plays": this.plays, "highscore": this.highscore}}).then(response => {
            if(!response.data.highscore)return;
            this.highscore = response.data.highscore;
            $("#highscore").html(`${this.highscore['score']}/${this.highscore['plays']}`)
            $("#wordList").prepend(`<font size='4'>${response.data.message}</font>`)
        })
    }

/**
 * Submit a word to be checked and - if valid - scored and addedto the list of played words.
 * Note that we use an arrow function so that 'this' is the instance of Game
 * @param {Event} event 
 */    
    submitWord = (event) => {
        event.preventDefault();
        if(this.word.value.length <= 0)return;
        axios.post('/add-word', {"word": this.word.value}).then(response => {
            let word = response.data.word;
            let score = response.data.score;
            let message = response.data.message;
            this.listWord(word, score, message);
        })
        this.word.value = "";
    }

/**
 * When the XHR returns a word it can be valid or invalid and it has a point value. The word will be added to the list of words
 * and the new score will be calculated.
 * @param {*} word 
 * @param {*} score 
 * @param {*} valid 
 */
    listWord = (word, score, message = "") => {
        let $item = $("<li>", {text:`${word} => ${score} ${message}`})
        if(score <= 0) {
            $item.addClass('invalid');
        }
        else {
            if(word in this.words) return;
            this.score += score;
            this.plays ++;
            $("#score").html(`${this.score}/${this.plays}`);
        }
        $("#wordList").append($item)
    }

}