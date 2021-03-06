<?php


 function getNRandomQuestions($n)
 {
     // Not using db-lib here to keep everything in uebung10 folder
    $user = get_current_user();
    $myCnf = parse_ini_file("/home/$user/.my.cnf");

    $host = $myCnf['host'];
    $user = $myCnf['user'];
    $password = $myCnf['password'];
    $database = $myCnf['database'];
    $connection = new mysqli($host, $user, $password, $database);

    $statement = $connection->prepare("SELECT * FROM questions ORDER BY RAND() LIMIT ?");
    $statement->bind_param("i", $n);
    $statement->execute();
    $statement->bind_result($id, $question, $answer0, $answer1, $answer2, $solution);
    while ($statement->fetch()){
        $result[] = array("question" => $question,
                        array(
                        "answer0" => $answer0,
                        "answer1" => $answer1,
                        "answer2" => $answer2),
                        "solution" => $solution,
    );
    }
    return $result;
}

// Check for parameter and set it according
if(!$_GET) $n = 10; elseif (!$_GET["n"]) $n=10; else $n=$_GET["n"];
// Get questions and encode to json 
$questions = getNRandomQuestions($n);
header('Content-Type: application/json');
echo json_encode($questions);
?>