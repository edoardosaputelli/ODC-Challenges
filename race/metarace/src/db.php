<?php
class DB{
    private $mysqli;

    function __construct(){
        $dbhost = $_ENV["DBHOST"];
        $dbuser = $_ENV["DBUSER"];
        $dbpass = $_ENV["DBPASS"];
        $db = $_ENV["DBNAME"];
        $this->mysqli = new mysqli($dbhost, $dbuser, $dbpass,$db) or die("Connect failed: %s\n".  $this->mysqli -> error);
    }

    



    function __destruct()
    {
        $this->mysqli -> close();
    }
    






    function create_user($name, $password){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("INSERT INTO users(name, password) VALUES (?, ?)"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
            die();
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("ss", $name, $password)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            die();
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            die();
        }

    }






    function fix_user($idusers){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("UPDATE users SET isadmin = 0 WHERE idusers = ?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("i", $idusers)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

    }







    function login($name, $password){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT idusers FROM users WHERE name=? and password=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("ss", $name, $password)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();

        $userid = $info['idusers'];
        $res->close();
        return $userid;
    }





    function get_username($id){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT name FROM users WHERE idusers=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("i", $id)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();

        $name = $info['name'];
        $res->close();
        return $name;
    }





    function get_idusers($name){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT idusers FROM users WHERE name=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("s", $name)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        
        $info = $res->fetch_assoc();

        $id = $info['idusers'];
        $res->close();
        return $id;
    }





    function get_admin($id){
        /* Prepared statement, stage 1: prepare */
        if (!($stmt = $this->mysqli->prepare("SELECT isadmin FROM users WHERE idusers=?"))) {
            echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
        }

        /* Prepared statement, stage 2: bind and execute */
        if (!$stmt->bind_param("i", $id)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $info = $res->fetch_assoc();
        $isadmin = $info['isadmin'] == 1;
        $res->close();
        return $isadmin;
    }




    function get_challenges($id, $isadmin){
        if ($isadmin){
            /* Prepared statement, stage 1: prepare */
            if (!($stmt = $this->mysqli->prepare("SELECT name, descriptions, points FROM challenges"))) {
                echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
            }
        }
        else{
            /* Prepared statement, stage 1: prepare */
            if (!($stmt = $this->mysqli->prepare("SELECT name, descriptions, points FROM challenges WHERE isenabled=true"))) {
                echo "Prepare failed: (" . $this->mysqli->errno . ") " . $this->mysqli->error;
            }

        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }

        if (!($res = $stmt->get_result())) {
            echo "Getting result set failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        $challenges = array();

        while ($info = $res->fetch_assoc()){
            array_push($challenges, $info);
        }
        $res->close();
        return $challenges;
    }

}
?>