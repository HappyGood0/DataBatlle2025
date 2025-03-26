<?php
$n = 5;
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Law Quiz</title>
    <link rel="stylesheet" href="style2.css" />
  </head>
  <body onload="Load(<?php echo $n; ?>);">

    <header class="main-header">
      <div class="logo"><a href="index.html">LegalQuizGPT</a></div>
      <div class="toggle-mode">🌙 Light/Dark</div>
    </header>

    <section class="quiz-container">
      
      <h2>Test Your Knowledge</h2>
      <div>
        <div id="progress-bar"><div class="progress"></div></div>
      </div>

      <?php
      $n = 5;
      $all_json = file_get_contents('../Data/many_to_one.json'); 
      $all_json = json_decode($all_json, true);
      $number = range(0, count($all_json));
      shuffle($number);
      for($i = 0; $i < $n; $i++){ ?>
        <div id="<?php echo $i; ?>" class="question-box hide" <?php if($all_json[$number[$i]]["type"] == "qcm"){ echo 'data-responce="'.strtolower($all_json[$number[$i]]["answer"]).'"';} ?>>
          <h3>Question <?php echo $i."/".$n; ?></h3>
          <p class="question"><?php echo $all_json[$number[$i]]["question_text"];?></p>
          <?php 
          if($all_json[$number[$i]]["type"] == "qcm"){ ?>
            <ul id="<?php echo $i; ?>options" class="options" data-nbPoint="1">
            <?php 
            $keys = array_keys($all_json[$number[$i]]["answer_choices"]);
            for($j = 0; $j < count($keys); $j++){ ?>
              <li><button id="<?php echo $i."_".$keys[$j]; ?>" data-buttonid="<?php echo $keys[$j]; ?>"><?php echo $all_json[$number[$i]]["answer_choices"][$keys[$j]]; ?></button></li>
            <?php } ?>
            </ul>
          <?php }
          elseif($all_json[$number[$i]]["type"] == "true or false"){
            $keys = array_keys($all_json[$number[$i]]["answer_choices"]);?>
            <ul id="<?php echo $i; ?>options" class="options" data-nbPoint="<?php echo count($keys); ?>">
            <?php 
            for($j = 0; $j < count($keys); $j++){ ?>
              <p><?php echo $all_json[$number[$i]]["answer_choices"][$keys[$j]]; ?></p>
              <li>
                <button id="<?php echo $i."_".$keys[$j]."_True";  ?>" data-responce="<?php echo $all_json[$number[$i]]["answers"][$keys[$j]]; ?>">True</button>
                <button id="<?php echo $i."_".$keys[$j]."_False"; ?>" data-responce="<?php echo $all_json[$number[$i]]["answers"][$keys[$j]]; ?>">False</button>
              </li>
            <?php }?>
            </ul>
          <?php } ?>
        </div>
      <?php } ?>

      <button id="next-btn" class="button">Next Question</button>
    </section>

    <footer>
      <p>&copy; 2025 Patent AI Project</p>
    </footer>

    <script src="script2.js"></script>
  </body>
</html>
