const textInput = $("#input");
const submitButton = $("#submit");
const gamesPlayed = $("#games");
const highScore = $("#hscore");

submitButton.click(confirmWord);

async function confirmWord(){

    let response = await axios({
        url: '/boggle/play',
        method: 'post',
        data: {word: textInput.val()}
    });

    
    console.log("GOT A RESPONSE!");
    console.log(response);
    
    let msg;

    if (response.data['result'] == "ok") msg = "<p class='correct'>Hurray!</p>";
    if (response.data['result'] == "not-on-board") msg = "<p class='absent'>That word is not on the board.</p>";
    if (response.data['result'] == "not-word") msg = "<p class='jibberish'>That is not a word.</p>";
    if (response.data['result'] == "already-found") msg = "<p class='duplicate'>That word was already found.</p>";

    $('#messages').html(msg);
    $('#score').html(response.data['points']);

}

const timerElement = $('#timer');

//I don't know why this is not working
timer = {
    time: 60,
    countdown(s = 60){
        timer.time = s;
        handle = setInterval(function(){
            timer.time = timer.time - 1;
            timerElement.html(timer.time)
            console.log(timer.time);

            if (timer.time <= 0){
                clearInterval(handle);
                submitButton.unbind();
                submitButton.text("Time's up!");

                recordStats();
            }
            
        }, 1000,)
        
    }
}

async function recordStats(){
    let reply = await axios({
        url: '/boggle/done',
        method: 'post',
        data: {stats: "game complete"}
    });

    if (reply.data['new_hscore'] == 'true'){
        highScore.text(reply.data['hscore'])
    }

    if (reply.data['games']){
        gamesPlayed.text(reply.data['games'])
    }
}

timer.countdown(60);
