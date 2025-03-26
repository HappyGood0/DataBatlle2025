// Light/Dark mode toggle
const toggleButton = document.querySelector('.toggle-mode');
const body = document.querySelector('body');
toggleButton.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
});

const questions = [
  {
    question: "What is the time limit for replying to a communication under Article 94(3) EPC?",
    options: ["Two months", "Four months", "Six months", "Eight months"],
    answer: 1
  },
  {
    question: "Which authority receives European patent applications?",
    options: ["EPO", "WIPO", "USPTO", "JPO"],
    answer: 0
  },
  {
    question: "Under which article can re-establishment of rights be requested?",
    options: ["Article 87", "Article 122", "Article 94", "Article 54"],
    answer: 1
  }
];

let currentQuestion = 0;
let score = 0;

const questionEl = document.querySelector('.question');
const optionsEl = document.querySelector('.options');
const questionNumber = document.querySelector('.question-box h3');
const nextBtn = document.querySelector('.next-btn');
const progressBar = document.querySelector('.progress-bar');
const scoreDisplay = document.createElement('p');

scoreDisplay.style.fontWeight = "bold";
scoreDisplay.style.color = "#004080";
scoreDisplay.style.textAlign = "left";
scoreDisplay.textContent = `Score: ${score}`;
document.querySelector('.quiz-container').prepend(scoreDisplay);

function loadQuestion() {
  const q = questions[currentQuestion];
  questionEl.textContent = q.question;
  questionNumber.textContent = `Question ${currentQuestion + 1}/${questions.length}`;
  optionsEl.innerHTML = "";

  q.options.forEach((opt, idx) => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.textContent = `${String.fromCharCode(65 + idx)}) ${opt}`;
    btn.addEventListener('click', () => checkAnswer(idx, btn));
    li.appendChild(btn);
    optionsEl.appendChild(li);
  });

  // Animate progress bar
  setTimeout(() => {
    progressBar.style.width = `${((currentQuestion) / questions.length) * 100}%`;
  }, 100);
}

function checkAnswer(selected, btn) {
  const correct = questions[currentQuestion].answer;
  const allButtons = document.querySelectorAll('.options button');

  allButtons.forEach(b => b.disabled = true);
  if (selected === correct) {
    btn.style.background = "#28a745";
    score++;
  } else {
    btn.style.background = "#dc3545";
    allButtons[correct].style.background = "#28a745";
  }
  scoreDisplay.textContent = `Score: ${score}`;
}

nextBtn.addEventListener('click', () => {
  if (currentQuestion < questions.length - 1) {
    currentQuestion++;
    loadQuestion();
  } else {
    progressBar.style.width = `100%`;
    document.querySelector('.quiz-container').innerHTML = `<h2>🎉 Quiz Completed!</h2><p>Your score: ${score}/${questions.length}</p>`;
  }
});

loadQuestion();
