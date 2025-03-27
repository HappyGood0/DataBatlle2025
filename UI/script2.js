// Light/Dark mode toggle
const toggleButton = document.querySelector('.toggle-mode');
const body = document.querySelector('body');
toggleButton.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
});

let currentQuestion = 0;
let score = 0;
let nbQuestion;
let nbPoint = 0;

const optionsEl = document.querySelector('.options');
const nextBtn = document.getElementById('next-btn');
const progressBar = document.getElementById('progress-bar');
const scoreDisplay = document.createElement('p');

scoreDisplay.style.fontWeight = "bold";
scoreDisplay.style.color = "#004080";
scoreDisplay.style.textAlign = "left";
scoreDisplay.textContent = `Score: ${score}`;
document.querySelector('.quiz-container').prepend(scoreDisplay);

function loadQuestion() {
  document.getElementById(currentQuestion).classList.remove("hide");

  document.getElementById(currentQuestion).querySelectorAll('button').forEach(b => {
    b.addEventListener('click', checkAnswer);
  });

  // Animate progress bar
  setTimeout(() => {
    progressBar.style.width = `${((currentQuestion) / nbQuestion) * 100}%`;
  }, 100);
}

function checkAnswer(e) {
  dataset = document.getElementById(currentQuestion).dataset;
  if("responce" in dataset){
    const correct    = dataset.responce;
    const allButtons = document.getElementById(currentQuestion).querySelectorAll('button');

    allButtons.forEach(b => b.disabled = true);
    if(this.dataset.buttonid === correct){
      this.style.background = "#28a745";
      score++;
    }
    else{
      this.style.background = "#dc3545";
      document.getElementById(currentQuestion+"_"+correct).style.background = "#28a745";
    }
  }
  else{
    const correct = this.dataset.responce;
    ids = this.id.replace("_True", "").replace("_False", "");
    document.getElementById(ids+"_True").disabled = true;
    document.getElementById(ids+"_False").disabled = true;

    if(this.innerHTML === correct){
      this.style.background = "#28a745";
      score++;
    }
    else{
      this.style.background = "#dc3545";
      document.getElementById(ids+"_"+correct).style.background = "#28a745";
    }
  }
  scoreDisplay.textContent = `Score: ${score}`;
}

nextBtn.addEventListener('click', () => {
  nbPoint+=parseInt(document.getElementById(currentQuestion+"options").dataset.nbpoint);
  if(currentQuestion < nbQuestion - 1){
    document.getElementById(currentQuestion).classList.add("hide");
    currentQuestion++;
    loadQuestion();
  }
  else{
    progressBar.style.width = `100%`;
    document.querySelector('.quiz-container').innerHTML = `<h2>🎉 Quiz Completed!</h2><p>Your score: ${score}/${nbPoint}</p><a href="quiz.php" class="button">Start Quiz</a>`;
  }
});

function Load(nb){
  nbQuestion = nb;
  loadQuestion();
}
