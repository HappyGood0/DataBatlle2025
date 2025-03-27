// Light/Dark mode toggle
const toggleButton = document.querySelector('.toggle-mode');
const body = document.querySelector('body');
toggleButton.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
});

// Counter animation (only if counters exist)
const counters = document.querySelectorAll('.counter');
if(counters.length > 0) {
  counters.forEach(counter => {
    counter.innerText = '0';
    const updateCounter = () => {
      const target = +counter.getAttribute('data-target');
      const count = +counter.innerText.replace(/[^0-9]/g, '');
      const increment = target / 100;
      if(count < target) {
        counter.innerText = count + Math.ceil(increment);
        setTimeout(updateCounter, 30);
      } else {
        if (counter.getAttribute('data-target') !== "99") {
          counter.innerText = "+" + target;
        } else {
          counter.innerText = target + "%";
        }
      }
    };
    updateCounter();
  });
}

// Testimonials slider (only if testimonials exist)
if (document.querySelector('.testimonial-cards')) {
  $('.testimonial-cards').slick({
    dots: true,
    arrows: false,
    slidesToShow: 1,
    autoplay: true,
    autoplaySpeed: 4000
  });
}

// ===== QUIZ FUNCTIONALITY =====
if (document.querySelector('.quiz-container')) {
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

  const questionEl = document.querySelector('.question');
  const optionsEl = document.querySelector('.options');
  const questionNumber = document.querySelector('.question-box h3');
  const nextBtn = document.querySelector('.next-btn');

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
  }

  function checkAnswer(selected, btn) {
    const correct = questions[currentQuestion].answer;
    const allButtons = document.querySelectorAll('.options button');

    allButtons.forEach(b => b.disabled = true);
    if (selected === correct) {
      btn.style.background = "#28a745";
    } else {
      btn.style.background = "#dc3545";
      allButtons[correct].style.background = "#28a745";
    }
  }

  nextBtn.addEventListener('click', () => {
    if (currentQuestion < questions.length - 1) {
      currentQuestion++;
      loadQuestion();
    } else {
      document.querySelector('.quiz-container').innerHTML = `<h2>🎉 Quiz Completed!</h2><p>You’ve reached the end.</p>`;
    }
  });

  // Load first question
  loadQuestion();
}
